import lexer

output = ""
tokenStack = []


def text(dialogue):
    global output
    output += dialogue + "\n"


#             type, symbol, declared flag, scope
symbolTable = [[],    [],        [],        []]

def addSymbol(*args,**kwargs):
    symbolTable[0].append(kwargs.get("type",0))
    symbolTable[1].append(kwargs.get("symbol",0))
    symbolTable[2].append(kwargs.get("flag",0))
    symbolTable[3].append(kwargs.get("scope",0))

    if kwargs.get("type",0) in ["function","class"]: # if function or class add to function stack
        global semicolon
        functionStack[0].append(kwargs.get("symbol",0))
        functionStack[1].append(0)


# Store list of identifiers as they are pushed to memorySegment
memorySegment = []









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
    print(token)
    token = lexer.getNextToken()
    print(token)
    token = lexer.getNextToken()
    print(token)


    text("function "+token[1]+" 1")
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


'''
In place of memorySegment we can write any of the following 8 keywords:

static:       - used to access static (class level) variables
argument:     - used to access the arguments (params) of the currently executing function
local:        - used to access the local variables of the currently executing function
this:         - used to access the current object (the object in which the current function resides)
that:         - used to access another object.
pointer:      - used to access a two location segment containing the ‘this’ (pointer[0]) and the ‘that’ (pointer[1]) pointers.
temp:         - used to access an 8 location segment for storing temporary values (a register file)
const:        - used to push a constant value into the stack.
'''


def var(token):
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void"]:
        return [0, "'' expected"]

    token = lexer.getNextToken()
    if token[1].isdigit():
        print(token)
        return [0, "identifier expected"]
    else:
        memorySegment.append(token[1])
        text("push constant 0")

    # print("\n",token)
    # while token[1]!=";":
    #     token = lexer.peekNextToken()
    #     tokenStack.append(token) 
    #     print(tokenStack[-1])

    return [1]


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
            # print(token)


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
