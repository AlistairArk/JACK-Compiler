'''
note:
    token[0] = type
    token[1] = lexeme
    token[2] = line number

'''
import lexer, parserKeywords, symbolTable
from codeGen import *



def parseFile():
    # Generate a list of methods to later be used in function calls
    token = lexer.peekNextToken()
    while (token[0] != "EOF"):
        if token[1]=="method":
            lexer.peekNextToken() # consume
            symbolTable.methodList.append(lexer.peekNextToken()[1])
        token = lexer.peekNextToken()



    # Begin main parsing of file
    token = lexer.getNextToken()
    while (token[0] != "EOF"):
        stmt(token)
        token = lexer.getNextToken()



def stmt(token):

    if token[0] == "keyword":        
        if token[0] in lexer.keywords:
            data = keywords[token[0]](token)
            
        elif token[1] in lexer.keywords:        
            data = keywords[token[1]](token)
        else:
            Error(token, "unknown keyword")

        if not data[0]:
            Error(token, data[1])


    elif token[0] in "symbol":
        if token[1] in lexer.symbols:        
            data = parserKeywords.symbol(token) 
            if not data[0]:
                Error(token, data[1])
        else:
            Error(token, "unknown symbol")


    elif token[0] in "operator":        
        if token[1] in lexer.operators:
            pass

        else:
            Error(token, "unknown operator")
  
    elif token[0] in ["id","number","string_literal"]:        
        pass


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