
import lexer as MyLexer
'''
note:
    token[0] = type
    token[1] = lexeme
'''




def Error(*args):
    print(args)




def Init(file_name):
    pass

    # if (!MyLexer.Init(file_name)):
    #     print("Unable to init the lexer")
    # else:
    #     print("Parser Initialized ")



def OK(token):
    print(token[1] + ": OK " )
        
    token = MyLexer.peekNextToken()
    while (token[0] != "EOF"):
        stmt()
        token = MyLexer.peekNextToken()
        


def banProg():

    token = MyLexer.peekNextToken ()
    while (token[0] != "EOF"):
        stmt()
        token = MyLexer.peekNextToken()




def stmt():
    token = MyLexer.peekNextToken()
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
        Error(token, "unknown keyword")




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
    token = MyLexer.getNextToken()
    if (token[1] == "print"):
        OK(token)  # be happy
    else:
        Error(token, "'print' expected")
    expr()






def assignStmt():
    token = MyLexer.getNextToken()
    if (token[1] == "assign"):
        OK(token) # be happy
    else:
        Error(token, "'assign' expected")

    expr()

    token = MyLexer.getNextToken()
    if (token[1] == "to"):
        OK(token) # be happy
    else:
        Error(token, "'to' expected")

    token = MyLexer.getNextToken()
    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy
    else:
        Error(token, "an identifier is expected")


def repeatStmt():
    token = MyLexer.getNextToken()
    if (token[1] == "repeat"):
        OK(token) # be happy
    else:
        Error(token, "'repeat' expected")

    expr()

    token = MyLexer.getNextToken()
    if (token[1] == "times"):
        OK(token) # be happy
    else:
        Error(token, "'times' expected")

    token = MyLexer.peekNextToken()
    while (token[1] != ""):
        stmt()
        token = MyLexer.peekNextToken()

    MyLexer.getNextToken() # consume the 




def banStmt():
    token = MyLexer.getNextToken()
    if (token[1] == "banana"):
        OK(token) # be happy
    else:
        Error(token, "'banana' expected")






# expr --> term { (+|-) term }
def expr():
    term()
    token = MyLexer.peekNextToken()
    while (token[1] == "+" or token[1] == "-"):
        MyLexer.GetNextToken() # consume the + or -
        term()
        token = MyLexer.peekNextToken()


# // term --> factor { (*|/) factor}
def term():
    factor()
    token = MyLexer.peekNextToken()
    while (token[1] == "*" or token[1] == "/"):
        MyLexer.GetNextToken() # consume the * or /
        factor()
        token = MyLexer.peekNextToken()


# factor -> int | id | ( expr )
def factor():
    token = MyLexer.GetNextToken()
    if (token[0] == Token.TokenTypes.Identifier):
        OK(token) # be happy


banProg()
