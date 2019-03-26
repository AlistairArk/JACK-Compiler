Assignment: Milestone 3. Symbol Table

As of now, I have created the Lexer, Parser and Semantic Analyzer. Both the Lexer and Parser have been connected together and function properly with one another. The Semantic Analyzer and other components have yet to be combined under a single system.

The Semantic Analyzer successfully parses code to generate a symbol table and flag any errors as encountered. The Semantic Analyzer carries out a number of checks for types, correct usage of variables, function calling & unreachable code. While the majority of Semantic Analysis checks have been implemented and tested, a small number still have yet to be implemented. 

The program does not crash or become unstable if the source file contains any kind of lexical or semantic errors, and if there are any the parser successfully flags them where necessary. 

All components have been tested using the provided JACK source files and are shown to function properly without any issues. 