
import lexer
from parserData import keywords as parserKeywords

'''
note:
    token[0] = type
    token[1] = lexeme
'''




def Error(*args):
    print(args)




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
    
    if token[0] in lexer.keywords:

        data = call_dict[token[0]](token)

        if data[0]:
            OK(token) # Accept the token
        else:
            Error(token, data[1])

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
  



        # if (token[1] == "given"):
        #     varDeclar()
        # elif (token[1] == "print"):
        #     printStmt()
        # elif (token[1] == "assign"):
        #     assignStmt()
        # elif (token[1] == "repeat"):
        #     repeatStmt()
        # elif (token[1] == "banana"):
        #     banStmt()


        # elif (token[1] == "keyword"):
        #     keyword()
        # elif (token[1] == "operator"):
        #     operator()
        # elif (token[1] == "symbol"):
        #     symbol()
        # else:
        #     Error(token, "keyword not implimented")
    else:
        Error(token, "unknown token")




# keywords = {"keyword":keyword,
#             "operator":operator,
#             "symbol":symbol}


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


def varDeclar():
    token = lexer.getNextToken()

    if (token[1] == "given"):
        OK(token) # be happy
    else:
        Error(token, "'given' expected")
    
    token = lexer.getNextToken()


    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy
    else:
        Error(token, "an identifier is expected")




def printStmt():
    token = lexer.getNextToken()
    if (token[1] == "print"):
        OK(token)  # be happy
    else:
        Error(token, "'print' expected")
    expr()






def assignStmt():
    token = lexer.getNextToken()
    if (token[1] == "assign"):
        OK(token) # be happy
    else:
        Error(token, "'assign' expected")

    expr()

    token = lexer.getNextToken()
    if (token[1] == "to"):
        OK(token) # be happy
    else:
        Error(token, "'to' expected")

    token = lexer.getNextToken()
    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy
    else:
        Error(token, "an identifier is expected")


def repeatStmt():
    token = lexer.getNextToken()
    if (token[1] == "repeat"):
        OK(token) # be happy
    else:
        Error(token, "'repeat' expected")

    expr()

    token = lexer.getNextToken()
    if (token[1] == "times"):
        OK(token) # be happy
    else:
        Error(token, "'times' expected")

    token = lexer.peekNextToken()
    while (token[1] != ""):
        stmt()
        token = lexer.peekNextToken()

    lexer.getNextToken() # consume the 




def banStmt():
    token = lexer.getNextToken()
    if (token[1] == "banana"):
        OK(token) # be happy
    else:
        Error(token, "'banana' expected")






# expr --> term { (+|-) term }
def expr():
    term()
    token = lexer.peekNextToken()
    while (token[1] == "+" or token[1] == "-"):
        lexer.getNextToken() # consume the + or -
        term()
        token = lexer.peekNextToken()


# // term --> factor { (*|/) factor}
def term():
    factor()
    token = lexer.peekNextToken()
    while (token[1] == "*" or token[1] == "/"):
        lexer.getNextToken() # consume the * or /
        factor()
        token = lexer.peekNextToken()


# factor -> int | id | ( expr )
def factor():
    token = lexer.getNextToken()
    if (token[0] == "keyword"): # token[0] == Token.TokenTypes.Identifier
        OK(token) # be happy


banProg()
