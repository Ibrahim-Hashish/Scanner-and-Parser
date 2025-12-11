## Scanner-and-Parser
# Overview
This project implements a scanner (lexer) and parser for a simplified subset of C++ using Python. Users can input C++ code, the scanner tokenizes it, and the parser validates the syntax.

# The tool supports:
- Variable declarations and assignments
- Arithmetic, comparison, and logical operations
- if / else statements
- while and for loops
- int main() function with optional return statement
The parser prints “Code accepted” if the input is syntactically correct or provides a syntax error message otherwise. Tokens are displayed before parsing.

# The grammar rules:
PROGRAM         -> MAIN_FUNCTION | STATEMENTS
MAIN_FUNCTION   -> int main() BLOCK
STATEMENTS      -> STATEMENT STATEMENTS | ε
STATEMENT       -> DECLARATION
                 | ASSIGNMENT
                 | IF_STATEMENT
                 | WHILE_LOOP
                 | FOR_LOOP
                 | RETURN_STATEMENT
DECLARATION     -> TYPE IDENTIFIER ;
                 | TYPE IDENTIFIER = EXPRESSION ;
ASSIGNMENT      -> IDENTIFIER = EXPRESSION ;
IF_STATEMENT    -> if ( EXPRESSION ) BLOCK [ else BLOCK ]
WHILE_LOOP      -> while ( EXPRESSION ) BLOCK
FOR_LOOP        -> for ( DECLARATION EXPRESSION ; ASSIGNMENT ) BLOCK
RETURN_STATEMENT -> return EXPRESSION ;
BLOCK           -> { STATEMENTS }
TYPE            -> int | float | double | bool
EXPRESSION      -> TERM { BINARY_OP TERM }
TERM            -> IDENTIFIER
                 | NUMBER
                 | true
                 | false
                 | ( EXPRESSION )
BINARY_OP       -> + | - | * | / | %
                 | == | != | < | <= | > | >=
                 | && | ||
IDENTIFIER      -> letter { letter | digit | _ }
NUMBER          -> digit { digit } [ . digit { digit } ]
LETTER          -> A..Z | a..z | _
DIGIT           -> 0..9

# Usage
1- Run the program
2- Enter your C++ code line by line.
3- Type END to finish input.
4- The program will display tokens and either:
      - Code accepted. if the code is syntactically correct.
      - Syntax error: ... if there is a syntax error





DIGIT           -> 0..9
