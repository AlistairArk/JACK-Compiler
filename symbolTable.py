import lexer
from codeGen import *



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
    elif token[1] == "neg":
        text("neg")
    elif token[1] == ">":
        text("gt")
    elif token[1] == "<":
        text("lt")
    elif token[1] == "=":
        text("eq")
    elif token[1] == "~":
        text("not")
    elif token[1] == "&": # token[1] == "And"
        text("and")
    elif token[1] == "|": # token[1] == "Or"
        text("or")

    elif token[1] == "*":
        text("call mult 2")

    elif token[1] == "/":
        text("call div 2")



def expressionToCode(expr):
    exprLen = len(expr)    # Get the length of the expression


    # Check what type the expression starts with
    if expr[0][0] == "operator":
        exprSwitch=1
    elif expr[0][0] in ["id","number"]:
        exprSwitch=0



    operator = ""
    pos=0
    for token in expr:
        pos+=1
        if exprSwitch:
            exprSwitch = 0
            print
            if token[0] != "operator":
                return [0, "Syntax Error: Invalid type in expression. 'operator' expected"]
            operator=token
            if pos==len(expr):          # if end of expression is reached 
                operatorToCode(token)   # output token

        else:            
            exprSwitch = 1

            pushData = pushPop(token)
            text("push "+pushData[0]+" "+str(pushData[1]))

            if pos>1:
                # if operator!="neg":
                operatorToCode(operator)
                # else:
                #     text("neg")



import copy
def orderExpr(exprType):
    if exprType in ["if","while"]:
        ending = "{"
    elif exprType in ["let"]:
        ending = ";"

    # Perform checks on the expression and wrap it up into a list
    bracketOpenCount = 0
    expr = [] # Stores list of tokens in expression
    while lexer.peekNextToken()[1]!=ending:
        if lexer.peekNextToken()[0] == "EOF":
            return [0, "unexpected EOF, ')' expected"]
        
        token = lexer.getNextToken()
        expr.append(token)

        # Insure matching number of parenthesis
        if token[1]=="(":
            bracketOpenCount+=1
        elif token[1]==")":
            bracketOpenCount-=1


    # print(expr)




    # Discern sub between neg and overwrite token
    neg = 1 # While true convert all '-' to 'neg'
    for i in range(len(expr)):
        if neg and expr[i][1] == "-":           # Set neg if neg enabled
                expr[i][1] = "neg"
                neg = 0

        elif expr[i][0] in ["id","number"]:     # Disable neg if number
            neg = 0

        elif expr[i][1] == "=":                 # Enable neg if equal
            neg = 1

    #     print(expr[i][1])


    # print(expr)
    # print()




    '''
    Calculates depth of parenthesized expressions 
    in order to handle them in the correct order. 
    '''

    result = [[[],0]]
    depth = 0
    pos = 0
    # pos = 0
    for token in expr:
        if token[1]=="(":
            depth+=1
            pos+=1
            result.append([[],depth])

        elif token[1]==")":
            depth-=1
            pos+=1
            result.append([[],depth])

        else:
            result[pos][0].append(token)

    # Remove empty lists
    removeStack = []
    for item in result:
        if item[0]==[]:
            removeStack.append(item)


    for item in removeStack:
        result.remove(item)



    # Get order of bracketed expressions
    exprOrder = []
    depth = 0

    # Check for starting potential depths
    count = -1
    for item in result:
        count+=1
        if result[count][1]>depth:
            depth = result[count][1]
            pos = count

    while len(result):
        if pos==len(result)-1 or result[pos+1][1]<=depth:

            # Generate code in order of expressions 
            # print(">",result[pos])
            expressionToCode(result[pos][0])
            result.remove(result[pos])

            if len(result):
                if pos:
                    pos -= 1    # Switch to next item

                depth = result[pos][1] # set new depth

                # Check for higher potential depths
                count = -1
                for item in result:
                    count+=1
                    if result[count][1]>depth:
                        depth = result[count][1]
                        pos = count

        else: 
            pos+=1





#                 {  (  [
bracketPointer = [1, 1, 1]
labelCounter = 0    # Increment counter as new labels are created
labelStack = []     # Close loops as they are created
def newLabel():
    global labelCounter
    labelCounter+=1
    labelStack.append(["l"+str(labelCounter), bracketPointer[0]]) # Store label name and scope
    



# orderExpr([['operator', '~', 4], ['symbol', '(', 4], ['id', 'x', 4], ['symbol', '=', 4], ['symbol', '(', 4], ['number', '0', 4], ['operator', '+', 4], ['number', '1', 4], ['symbol', ')', 4], ['symbol', ')', 4]])
# orderExpr([['operator', '~', 4], ['symbol', '(', 4],  ['id', 'x', 4],['id', '-', 4],['id', 'x', 4], ['symbol', '=', 4], ['symbol', '-', 4], ['symbol', '(', 4], ['number', '0', 4], ['operator', '+', 4], ['number', '1', 4], ['symbol', ')', 4], ['symbol', ')', 4]])

# print(orderExpr([['operator', '~', 4], ['symbol', '(', 4], ['id', 'x', 4], ['symbol', '=', 4], ['symbol', '(', 4], ['number', '0', 4], ['operator', '+', 4], ['symbol', '(', 4], ['number', '1', 4], ['operator', '*', 4], ['number', '5', 4], ['symbol', ')', 4], ['symbol', ')', 4], ['operator', '+', 4], ['symbol', '(', 4], ['number', '4', 4], ['operator', '*', 4], ['number', '6', 4], ['symbol', ')', 4], ['symbol', ')', 4]]))
# print("\n\n")
# print(output)




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


push constant 12
pop local 0

push constant 0
pop local 1

push constant 0
pop local 2

push local 1
push local 0
it




'''





