
import lexer

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






keywords = {"keyword":func,
            "operator":func,
            "symbol":func}




def stmt():
    
    token = lexer.peekNextToken()
    
    if token[1] in lexer.keywords:
        if (token[1] == "given"):
            varDeclar()
        elif (token[1] == "print"):
            printStmt()
        elif (token[1] == "assign"):
            assignStmt()
        elif (token[1] == "repeat"):
            repeatStmt()
        elif (token[1] == "banana"):
            banStmt()
        else:
            Error(token, "keyword not implimented")
    else:
        Error(token, "unknown keyword")




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
