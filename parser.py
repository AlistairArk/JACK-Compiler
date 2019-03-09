










def stmt():
    Token t = MyLexer.PeekNextToken()
    if (t.Lexeme == "given"):
        varDeclar()
    elif (t.Lexeme == "print"):
        printStmt()
    elif (t.Lexeme == "assign"):
        assignStmt()
    elif (t.Lexeme == "repeat"):
        repeatStmt()
    elif (t.Lexeme == "banana"):
        banStmt()
    else:
        Error(t, "unknown keyword")




def varDeclar():
    pass
    
def printStmt():
    pass
    
def assignStmt():
    pass
    
def repeatStmt():
    pass
    
def banStmt():
    pass
    