import lexer

output = ""
tokenStack = []


def text(dialogue):
    global output
    output += dialogue + "\n"


#             type, symbol, index, scope
symbolTable = [[],    [],        [],        []]

symbolIndexList = [[],[]]
def addSymbol(*args,**kwargs):

    # Add new type to list of indexes as encountered
    if not kwargs.get("type",0) in symbolIndexList[0]:
        symbolIndexList[0].append(kwargs.get("type",0)) 
        symbolIndexList[1].append(-1)

    symbolIndex = symbolIndexList[0].index(kwargs.get("type",0))
    symbolIndexList[1][symbolIndex] += 1 # Incriment index

    symbolTable[0].append(kwargs.get("type",0))
    symbolTable[1].append(kwargs.get("symbol",0))
    symbolTable[2].append(kwargs.get("index",symbolIndexList[1][symbolIndex]))
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



def function(token): # function int mult

    # Check function is of proper type
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void"]:
        return [0, "unexpected function type"]
    if token[0] != "keyword":
        return [0, "'keyword' expected"]


    # Check function has appropriate type and name
    token = lexer.getNextToken()
    print(token)
    if token[0] != "id":
        return [0, "'id' expected"]

    text("function "+token[1]+" 1")


    token = lexer.getNextToken()
    if token[1]!="(":
        return [0, "'(' expected"]

    ## Check syntax of function arguments
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
                addSymbol(type="argument", symbol=token[1], scope="")

        elif token[0] == "symbol":
            if not token[1] in [",", ")"]: 
                return [0, "unexpected symbol type"]

        # incriment pointer
        expectedTypePointer+=1
        if expectedTypePointer == 3:
            expectedTypePointer = 0


    token = lexer.getNextToken()
    if token[1]!="{":
        return [0, "'{' expected"]

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








// Declaring a var doesn't generate code
// It simply adds some entries to the symbol table
var int length;         // simply add a local variable to the table of local variables for this fucntion
var int i, sum;         // This line doens't generate any code as well.

let length = 12;
let i = 0;
let sum = 0;
while (i < length){
    let sum = sum + i;
    let i = i + 1;
}







'''







def var(token):
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void"]:
        return [0, "'' expected"]
                # addSymbol(type="argument", symbol=token[1], scope="")

    token = lexer.getNextToken()
    if token[0]=="number":
        print(token)
        return [0, "identifier expected"]
    else:
        addSymbol(type="local", symbol=token[1], scope="")


    while token[1]!=";":
        token = lexer.peekNextToken()
        tokenStack.append(token) 
        print(tokenStack[-1])

    return [1]


def static(token):
    return [1]

    return [0, "'' expected"]

def field(token):
    return [1]

    return [0, "'' expected"]

















#             type, symbol, index, scope

def let(token):
    calcList = [] # Stores list of tokens in calculation


    def pushPop(token):
        if token[0]=="number":
            return ["constant", token[1]]
        else:
            # Get data for popping    
            symbolIndex = symbolTable[1].index(token[1])
            varIndex = symbolTable[2][symbolIndex]
            varType  = symbolTable[0][symbolIndex]
            return [varType, varIndex]

    def operatorToCode(token):
        # ["+","-","*","/","&","|","~","<",">"]
        
        if token[1] == "+":
            text("add")
        elif token[1] == "-":
            text("sub")
        elif token[1] == ">":
            text("gt")
        elif token[1] == "<":
            text("lt")
        elif token[1] == "&": # token[1] == "And"
            text("and")
        elif token[1] == "|": # token[1] == "Or"
            text("or")

        elif token[1] == "*":
            text("call mult 2")

        elif token[1] == "/":
            text("call div 2")

        # (commands neg and not are handled interdependently)

    token = lexer.getNextToken()

    if token[0]!="id":
        return [0, "'id' expected"]

    popData = pushPop(token)


    token = lexer.getNextToken()
    if token[0]!="symbol":
        return [0, "'id' expected"]
    elif token[1]!="=":
        return [0, "'=' expected"]


    token = lexer.getNextToken()
    if token[1]==";":
        return [0, "expression expected"]




    while token[1]!=";":
        calcList.append(token)
        token = lexer.getNextToken()

    print(calcList)
    if len(calcList) == 1:
        text("push constant "+str(calcList[0][1]))
    else: # Handle expression

        '''
        # First check expression has correct syntax
        
        expectedTypePointer  - Handel's switching between operator and id/number
        expressionCounter    - Counts number of operands encountered.
                               After encountering 2 the operator is handled and the counter is reset.
        '''
        expectedTypePointer = 0 
        expressionCounter = 0   
        operator = []
        for token in calcList:
            print(token)
            if expectedTypePointer:
                if token[0] != "operator":
                    return [0, "Syntax Error: Invalid type in expression. 'operator' expected"]
                expectedTypePointer = 0
                operator=token

            else:
                
                if not token[0] in ["id","number"]:
                    if token[0] == "operator" and token[1] == "-":
                        expressionCounter = 1
                        operator = "neg"
                    else:
                        return [0, "Syntax Error: Invalid type in expression. 'id' or 'number' expected"]
                else:
                    expectedTypePointer = 1
                    expressionCounter+=1

                    pushData = pushPop(token)
                    text("push "+pushData[0]+" "+str(pushData[1]))
    
                    if expressionCounter>=2:
                        # expressionCounter = 0
                        if operator!="neg":
                            operatorToCode(operator)
                        else:
                            text("neg")


        if not expectedTypePointer:
            return [0, "Syntax Error: Expression ends in 'operator'. 'id' or 'number' expected"]

        # handle calculation of expression

        # text("push ??? ")
    


    text("pop "+popData[0]+" "+str(popData[1]))








    return [1]
    # token = lexer.getNextToken()
    # print(token)

    # token = lexer.getNextToken()
    # print(token)
    

    # symbolIndex = symbolTable[1].index(token[1])
    
    # varType     = str(symbolTable[1].index(token[1]))
    # print("   ",symbolTable)
    # text("pop local "+varIndex)


    # return [0, "'' expected"]














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
