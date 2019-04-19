'''
Assignment: Milestone 2. The Parser

So far, I have created a lexer and parser. The two components have been conected together and function properly with one another. 
The program does not crash or become unstable if the source file contains any kind of lexical errors, and if there are any the parser succesfully flags them where necessary. 

Both the lexer and parser have been tested using the provided JACK source files and are shown to function properly without any issues. 
'''

import lexer, parserKeywords, codeGen

'''
note:
    token[0] = type
    token[1] = lexeme
    token[2] = line number
'''


 

def Error(*args):
    print("Error in line " + str(args[0][2]) + " at or near " + str(args[0][1])+ ", " + str(args[1]));




def Init(file_name):
    pass





def OK(token):
    pass



def parseFile():

    token = lexer.getNextToken()
    while (token[0] != "EOF"):
        stmt(token)
        token = lexer.getNextToken()

    # print("\n===== ===== ===== ===== ===== ===== ===== =====\n")
    # print(codeGen.output)





def stmt(token):

    if token[0] == "keyword":        
        if token[0] in lexer.keywords:
            data = keywords[token[0]](token)
            
        elif token[1] in lexer.keywords:        
            data = keywords[token[1]](token)
        else:
            Error(token, "unknown keyword")

        if data[0]:
            OK(token) # Accept the token
        else:
            Error(token, data[1])


    elif token[0] in "symbol":
        if token[1] in lexer.symbols:        
            data = parserKeywords.symbol(token) 
            if data[0]:
                OK(token) # Accept the token
            else:
                Error(token, data[1])
        else:
            Error(token, "unknown symbol")


    elif token[0] in "operator":        
        if token[1] in lexer.operators:        
            OK(token) # be happy
        else:
            Error(token, "unknown operator")
  
    elif token[0] in "id": 
        OK(token) # be happy



    elif token[0] in "number":        
        OK(token) # be happy

    elif token[0] in "string_literal":        
        OK(token) # be happy



    else:
        Error(token, "unknown token")






# Program Components
keywords = {"class":parserKeywords.Class , 
            "constructor":parserKeywords.constructor , 
            "method":parserKeywords.method , 
            "function":parserKeywords.function,  

            # Primitive Types
            "int":parserKeywords.int,
            "boolean":parserKeywords.boolean,
            "char":parserKeywords.char,
            "void":parserKeywords.void,  

            # Variable Declarations
            "var":parserKeywords.var,
            "static":parserKeywords.static,
            "field":parserKeywords.field,                                 
            
            # Statements
            "let":parserKeywords.let,
            "do":parserKeywords.do, 
            "if":parserKeywords.If, 
            "else":parserKeywords.Else, 
            "while":parserKeywords.While, 
            "return":parserKeywords.Return, 
           
            # Constant Values
            "true":parserKeywords.true,
            "false":parserKeywords.false,
            "null":parserKeywords.null,                       
           
            # Objective Reference 
            "this":parserKeywords.this                    
            }


parseFile()