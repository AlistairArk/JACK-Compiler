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

varList = []







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
    token = lexer.getNextToken()
    print(token)
    if token[1]!="(":
        return [0, "'(' expected"]

    ## ADD CHECKS FOR FUNCTION
    expectedTypeList = ["keyword","id","symbol"]
    expectedTypePointer = 0
    while token[1]!=")":
        token = lexer.getNextToken()
        
        if token[0]!=expectedTypeList[expectedTypePointer]:
            return [0, "'"+expectedTypeList[expectedTypePointer]+"' expected"]
        
        elif token[0] == "keyword":
            if not token[1] in ["int", "boolean", "char"]: 
                return [0, "unexpected keyword type"]
        
        elif token[0] == "id": # add variable to symbol table
                addSymbol(type="var", symbol=token[1], scope="argument")

        elif token[0] == "symbol":
            if not token[1] in [",", ")"]: 
                return [0, "unexpected symbol type"]

        print("  ",token)
        # incriment pointer
        expectedTypePointer+=1
        if expectedTypePointer == 3:
            expectedTypePointer = 0

        # tokenStack.append(token) 
    token = lexer.getNextToken()
    print(token)
    if token[1]!="{":
        return [0, "'{' expected"]

    text("function "+token[1]+" 1")
    return [1]


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





 





function int mult (int x, int y) {
    var int result;
    let result = 0;
    while ~(x = 0) {
        let result = result + y;
        let x = x - 1;
    }
    return result;
}



function mult 1           // function int mult
    push constant 0       // var int result;
    pop local 0           // 
label loop                // while
    push argument 0       // x
    push constant 0       // 0
    eq                    // =
    if-goto end           // 
    push argument 1       // 
    push local 0          // 
    add                   // 
    pop local 0           // 
    push argument 0       // 
    push constant 1       // 
    sub                   // 
    pop argument 0        // 
    goto loop             // 
label end                 // }

    push local 0          // return result
    return                // 

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
        varList.append(token[1])
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
    token = lexer.getNextToken()
    print(token)
    varIndex = str(varList.index(token[1]))
    text("pop local "+varIndex)

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
