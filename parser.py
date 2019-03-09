
import lexer as MyLexer






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
    token = MyLexer.getNextToken();

    if (token[1] == "given")
        OK(token); # be happy
    else
        Error(token, "'given' expected")
    
    token = MyLexer.getNextToken()


    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy
    else:
        Error(token, "an identifier is expected")




def printStmt():
    pass

def assignStmt():
    pass

def repeatStmt():
    pass

def banStmt():
    pass
