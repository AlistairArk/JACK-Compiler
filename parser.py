
import lexer as MyLexer
'''
note:
    token[0] = type
    token[1] = lexeme
'''


def Error(*args):
    print(args)



def stmt():
    token = MyLexer.PeekNextToken()
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
        Error(t, "unknown keyword")




def varDeclar():
    token = MyLexer.getNextToken()

    if (token[1] == "given"):
        OK(token) # be happy
    else:
        Error(token, "'given' expected")
    
    token = MyLexer.getNextToken()


    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy
    else:
        Error(token, "an identifier is expected")




def printStmt():
    token = MyLexer.GetNextToken()
    if (token[1] == "print"):
        OK(token)  # be happy
    else:
        Error(token, "'print' expected")
    expr()






def assignStmt():
    token = MyLexer.GetNextToken()
    if (token[1] == "assign"):
        OK(token) # be happy
    else:
        Error(token, "'assign' expected")
        
    expr()

    token = MyLexer.GetNextToken()
    if (token[1] == "to"):
        OK(token) # be happy
    else:
        Error(token, "'to' expected")

    token = MyLexer.GetNextToken()
    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy
    else:
        Error(token, "an identifier is expected")


def repeatStmt():
    pass

def banStmt():
    pass
