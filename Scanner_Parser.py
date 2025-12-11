import re
from typing import List, Tuple, Optional

# ---------------- Scanner ----------------
class Scanner:
    """
    Scanner (Lexer) for a simplified C++ subset.

    Attributes:
        code (str): The source code to tokenize.
        tokens (List[Tuple[str, str]]): List of generated tokens.
        keywords (set): Set of recognized keywords.
        token_specification (List[Tuple[str, str]]): Regex patterns for token types.
    """
    
    def __init__(self, code: str) -> None:
        self.code: str = code
        self.tokens: List[Tuple[str, str]] = []
        self.keywords: set = {
            'int', 'float', 'double', 'bool', 'if', 'else', 'while', 
            'for', 'true', 'false', 'return', 'main'
        }
        self.token_specification: List[Tuple[str, str]] = [
            ('NUMBER', r'\d+(\.\d*)?'),
            ('ID', r'[A-Za-z_]\w*'),
            ('OP', r'==|!=|<=|>=|&&|\|\||\+\+|--|[+\-*/%=<>]'),
            ('SEMI', r';'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('SKIP', r'[ \t]+'),
            ('NEWLINE', r'\n'),
        ]
        self.token_regex: str = '|'.join(
            f'(?P<{name}>{regex})' for name, regex in self.token_specification
        )

    def tokenize(self) -> List[Tuple[str, str]]:
        """
        Tokenize the source code into a list of tokens.
        
        Returns:
            List of tuples (token_type, token_value)
        """
        for mo in re.finditer(self.token_regex, self.code):
            kind: str = mo.lastgroup
            value: str = mo.group()
            if kind == 'ID' and value in self.keywords:
                kind = 'KEYWORD'
            elif kind in {'SKIP', 'NEWLINE'}:
                continue
            self.tokens.append((kind, value))
        return self.tokens


# ---------------- Parser ----------------
class Parser:
    """
    Recursive descent parser for the simplified C++ subset.

    Attributes:
        tokens (List[Tuple[str, str]]): List of tokens from the scanner.
        pos (int): Current position in the tokens list.
    """
    
    def __init__(self, tokens: List[Tuple[str, str]]) -> None:
        self.tokens: List[Tuple[str, str]] = tokens
        self.pos: int = 0

    def peek(self) -> Tuple[str, str]:
        """Return the current token or ('EOF', '') if at the end."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def advance(self) -> None:
        """Move to the next token."""
        self.pos += 1

    def match(self, expected_type: str, expected_value: Optional[str] = None) -> bool:
        """
        Match the current token against expected type and optionally value.
        
        Returns:
            True if matched and advances, False otherwise.
        """
        tok_type, tok_val = self.peek()
        if tok_type == expected_type and (expected_value is None or tok_val == expected_value):
            self.advance()
            return True
        return False

    def parse(self) -> None:
        """
        Parse the token list. Prints "Code accepted." if successful,
        otherwise prints syntax error.
        """
        try:
            # Optional main function
            if self.match('KEYWORD', 'int') and self.match('KEYWORD', 'main') and self.match('LPAREN') and self.match('RPAREN'):
                if not self.block():
                    raise SyntaxError("Missing block after main()")
            while self.pos < len(self.tokens):
                if not self.statement():
                    raise SyntaxError(f"Unexpected token: {self.peek()}")
            print("Code accepted.")
        except SyntaxError as e:
            print("Syntax error:", e)

    # ---------------- Grammar rules ----------------
    def statement(self) -> bool:
        """Parse a single statement."""
        tok_type, tok_val = self.peek()
        if tok_type == 'KEYWORD' and tok_val in {'int', 'float', 'double', 'bool'}:
            return self.declaration()
        elif tok_type == 'ID':
            return self.assignment()
        elif tok_type == 'KEYWORD' and tok_val == 'if':
            return self.if_statement()
        elif tok_type == 'KEYWORD' and tok_val == 'while':
            return self.while_loop()
        elif tok_type == 'KEYWORD' and tok_val == 'for':
            return self.for_loop()
        elif tok_type == 'KEYWORD' and tok_val == 'return':
            return self.return_statement()
        return False

    def declaration(self) -> bool:
        """Parse a variable declaration with optional initialization."""
        self.advance()  # skip type
        if self.match('ID'):
            if self.match('OP', '='):
                self.expression()
            if self.match('SEMI'):
                return True
        return False

    def assignment(self) -> bool:
        """Parse an assignment statement."""
        self.advance()  # skip identifier
        if self.match('OP', '='):
            self.expression()
            if self.match('SEMI'):
                return True
        return False

    def expression(self) -> None:
        """Parse a simple expression (arithmetic, comparison, or logic)."""
        self.term()
        while self.match('OP') and self.tokens[self.pos - 1][1] in {
            '+', '-', '*', '/', '%', '||', '&&', '==', '!=', '<', '<=', '>', '>='
        }:
            self.term()

    def term(self) -> None:
        """Parse a term (identifier, number, boolean, or parenthesized expression)."""
        tok_type, _ = self.peek()
        if tok_type in {'NUMBER', 'ID', 'KEYWORD'}:
            self.advance()
        elif self.match('LPAREN'):
            self.expression()
            if not self.match('RPAREN'):
                raise SyntaxError("Missing closing parenthesis")
        else:
            raise SyntaxError(f"Unexpected token in term: {self.peek()}")

    def if_statement(self) -> bool:
        """Parse an if or if-else statement."""
        self.advance()  # skip 'if'
        if not self.match('LPAREN'):
            raise SyntaxError("Missing '(' after if")
        self.expression()
        if not self.match('RPAREN'):
            raise SyntaxError("Missing ')' after if condition")
        if not self.block():
            raise SyntaxError("Missing block after if")
        if self.match('KEYWORD', 'else'):
            if not self.block():
                raise SyntaxError("Missing block after else")
        return True

    def while_loop(self) -> bool:
        """Parse a while loop."""
        self.advance()  # skip 'while'
        if not self.match('LPAREN'):
            raise SyntaxError("Missing '(' after while")
        self.expression()
        if not self.match('RPAREN'):
            raise SyntaxError("Missing ')' after while condition")
        if not self.block():
            raise SyntaxError("Missing block after while")
        return True

    def for_loop(self) -> bool:
        """Parse a for loop."""
        self.advance()  # skip 'for'
        if not self.match('LPAREN'):
            raise SyntaxError("Missing '(' after for")
        self.statement()  # initialization
        self.expression()  # condition
        self.match('SEMI')
        self.assignment()  # increment
        if not self.match('RPAREN'):
            raise SyntaxError("Missing ')' after for loop")
        if not self.block():
            raise SyntaxError("Missing block after for")
        return True

    def return_statement(self) -> bool:
        """Parse a return statement."""
        self.advance()  # skip 'return'
        self.expression()
        if not self.match('SEMI'):
            raise SyntaxError("Missing ';' after return")
        return True

    def block(self) -> bool:
        """Parse a block of statements enclosed in braces."""
        if self.match('LBRACE'):
            while not self.match('RBRACE'):
                if not self.statement():
                    raise SyntaxError(f"Invalid statement in block: {self.peek()}")
            return True
        return False


# ---------------- Main Program ----------------
if __name__ == "__main__":
    print("Enter your C++ code line by line. Type END to finish input:")
    lines: List[str] = []
    while True:
        line: str = input()
        if line.strip() == "END":
            break
        lines.append(line)
    code: str = "\n".join(lines)

    # Scan tokens
    scanner: Scanner = Scanner(code)
    tokens: List[Tuple[str, str]] = scanner.tokenize()
    
    print("\nTokens:")
    for token in tokens:
        print(token)

    # Parse tokens
    parser: Parser = Parser(tokens)
    parser.parse()
