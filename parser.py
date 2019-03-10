
import lexer
from parserData import keywords as parserKeywords

'''
note:
    token[0] = type
    token[1] = lexeme
'''




def Error(*args):
    print("Error in line " + str(args[0][2]) + " at or near " + str(args[0][1])+ ", " + str(args[1]));




def Init(file_name):
    pass

    # if (!lexer.Init(file_name)):
    #     print("Unable to init the lexer")
    # else:
    #     print("Parser Initialized ")



def OK(token):
    print(token[1] + ": OK " )
        
    token = lexer.peekNextToken()
    while (token[0] != "EOF"):
        stmt()
        token = lexer.peekNextToken()
        


def banProg():

    token = lexer.peekNextToken ()
    while (token[0] != "EOF"):
        stmt()
        token = lexer.peekNextToken()









def stmt():
    
    token = lexer.getNextToken()
    

    if token[0] in "keyword":        
        if token[1] in lexer.keywords:        
            OK(token) # be happy
        else:
            Error(token, "unknown keyword")

    elif token[0] in "symbol":        
        if token[1] in lexer.symbols:        
            OK(token) # be happy
        else:
            Error(token, "unknown symbol")

    elif token[0] in "operator":        
        if token[1] in lexer.operators:        
            OK(token) # be happy
        else:
            Error(token, "unknown operator")
  
    elif token[0] in "id":        
        OK(token) # be happy
        # if token[1] in lexer.operators:        
        #     OK(token) # be happy
        # else:
        #     Error(token, "unknown operator")
    elif token[0] in "number":        
        OK(token) # be happy

    elif token[0] in "string_literal":        
        OK(token) # be happy

    elif token[0] in lexer.keywords:
        data = call_dict[token[0]](token)
        if data[0]:
            OK(token) # Accept the token
        else:
            Error(token, data[1])


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


banProg()
