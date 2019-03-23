
import lexer, semanticAnalyser

def Class(token):
    return [1]

    return [0, "'' expected"]

def constructor(token):
    return [1]

    return [0, "'' expected"]

def method(token):
    return [1]

    return [0, "'' expected"]

def function(token):
    return [1]

    return [0, "'' expected"]

def int(token):
    return [1]

    return [0, "'' expected"]

def boolean(token):
    return [1]

    return [0, "'' expected"]

def char(token):
    return [1]

    return [0, "'' expected"]

def void(token):
    return [1]

    return [0, "'' expected"]

def var(token):
    return [1]

    return [0, "'' expected"]

def static(token):
    return [1]

    return [0, "'' expected"]

def field(token):
    return [1]

    return [0, "'' expected"]

def let(token):
    return [1]

    return [0, "'' expected"]

def do(token):
    return [1]

    return [0, "'' expected"]

def If(token):
    token = lexer.getNextToken()
    bracketOpenCount = 0

    if token[1]=="(":
        bracketOpenCount+=1 # Insure same number of bracket opens as closes


        while bracketOpenCount:
            token = lexer.getNextToken()
            print(token)


            if token[1]=="(":
                bracketOpenCount+=1
            elif token[1]==")":
                bracketOpenCount-=1

            if lexer.peekNextToken()[0] == "EOF":
                return [0, "unexpected EOF, ')' expected"]

        return [1]

    else:
        return [0, "'(' expected"]

def Else(token):
    if lexer.getNextToken()[1]=="{":
        return [1]
    else:
        return [0, "'{' expected"]

def While(token):
    return [1]

    return [0, "'' expected"]

def Return(token):
    return [1]

    return [0, "'' expected"]

def true(token):
    return [1]

    return [0, "'' expected"]

def false(token):
    return [1]

    return [0, "'' expected"]

def null(token):
    return [1]

    return [0, "'' expected"]

def this(token):
    return [1, token]

    return [0, "'' expected"]
