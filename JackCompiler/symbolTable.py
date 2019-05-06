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


    print("             symbolIndexList: ",symbolIndexList)


def resetSymbolIndexList():
    print("\n\n\n")
    global symbolIndexList
    print(symbolIndexList)
    symbolIndexList = [[],[]]




def pushPop(token):
    if token[0]=="number":
        return ["constant", token[1]]
    else:
        # Get data for popping    
        if token[1] in symbolTable[1]:
            symbolIndex = symbolTable[1].index(token[1])
            varIndex = symbolTable[2][symbolIndex]
            varType  = symbolTable[0][symbolIndex]
            return [varType, varIndex]
        else:
            Error(token,"use of undeclared variable")
            exit()

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
        text("call Math.multiply 2")

    elif token[1] == "/":
        text("call Math.divide 2")



def expressionToCode(expr):

    exprLen = len(expr)    # Get the length of the expression


    # Check what type the expression starts with
    if expr[0][0] == "operator":
        exprSwitch=1
    elif expr[0][0] in ["id","number","array"]:
        exprSwitch=0

    elif expr[0][0] in ["string_literal"]:
        text("push constant "+str(len(expr[0][1])))         # Push length of string
        text("call String.new 1")                           # Call string function
        for item in expr[0][1]:                             # Create string
            text("push constant "+str(ord(item)))
            text("call String.appendChar 2")
        return

    elif expr[0][0] in ["function"]:


        # Get a parameter from the function and run the expression to
        # generate it's code
        funcParam = []
        for item in expr[0][1][1]:
            if item[1]==",":
                runExpr(funcParam) # run expr
                funcParam = []
            else:
                funcParam.append(item)


        runExpr(funcParam) # run expr
        # exit()

        text("call "+expr[0][1][0][1]+" 1")
        return


    operator = ""
    pos=0
    for token in expr:
        pos+=1
        if exprSwitch:
            exprSwitch = 0

            if token[0] != "operator":
                return [0, "Syntax Error: Invalid type in expression. 'operator' expected"]
            operator=token
            if pos==len(expr):          # if end of expression is reached 
                operatorToCode(token)   # output token

        else:            
            exprSwitch = 1

            if token[0]=="array":


                for item in [token[1][0],token[1][1],["operator","+",token[2]]]:
                    expressionToCode([item])
                '''
                push local 2
                push local 0
                add

                pop pointer 1
                push that 0
                '''
                text("pop pointer 1")
                text("push that 0")
                # exit()
            else:
                pushData = pushPop(token)
                text("push "+pushData[0]+" "+str(pushData[1]))

            if pos>1:
                # if operator!="neg":
                operatorToCode(operator)
                # else:
                #     text("neg")



import copy
def orderExpr(exprType):
    ''' Obtains a list of tokens which comprise an expression '''




    if exprType in ["if","while"]:
        ending = "{"
    elif exprType in ["let","do"]:
        ending = ";"

    # Perform checks on the expression and wrap it up into a list
    bracketOpenCount = 0
    expr = [] # Stores list of tokens in expression

    token = lexer.peekNextToken()
    while token[1]!=ending:
        
        token = lexer.getNextToken()    # Consume token
        if token[0] == "EOF":
            return [0, "unexpected EOF, ')' expected"]


        expr.append(token)
        # print(">>>>>>>",token)


        # Insure matching number of parenthesis
        if token[1]=="(":
            bracketOpenCount+=1
        elif token[1]==")":
            bracketOpenCount-=1

        if bracketOpenCount==-1:
            return [0, "mismatched number of parenthesis"]
        
        lastToken = token
        token = lexer.peekNextToken()
        # Check if next token implies the current token is a function call
        if lastToken[0]=="id" and token[1]=="(":
            lexer.getNextToken() # consume token
            expr[-1][0]="function"
            expr[-1][1] = [expr[-1].copy(), []] # store function with arguments
            bCount = 1
            while bCount:   # Exit on obtaining all parameters
                token = lexer.getNextToken()
                if token[1]=="(":
                    bCount+=1
                elif token[1]==")":
                    bCount-=1

                if bCount:
                    expr[-1][1][1].append(token)
                    # print(">>>>>>>",token)

            token = lexer.peekNextToken() # Revert peek

        # Check if next token implies the current token is array
        elif token[1]=="[":
            lexer.getNextToken() # consume token
            expr[-1][1] = [expr[-1].copy(), lexer.getNextToken()] # store array with index
            expr[-1][0]="array"
            if lexer.getNextToken()[1]!="]":
                return [0, "']' expected"]

            token = lexer.peekNextToken() # Revert peek

    print(expr, bracketOpenCount)
    return runExpr(expr)



def runExpr(expr):
    ''' Generates code for a given expression '''

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
    counter = 0
    curPos = pos
    for item in result:
        counter+=1
        if item[0]==[]:
            removeStack.append(item)
            if counter>=curPos:     # Shift pos back if item removal will cause shifts
                pos-=1


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
            # print("     >",result[pos])
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


    return [1]



#                 {  (  [
bracketPointer = [1, 1, 1]
labelCounter = 0    # Increment counter as new labels are created
labelStack = []     # Close loops as they are created
def newLabel(labelType):
    global labelCounter

    if labelType=="if":
        labelStack.append([str(labelCounter), bracketPointer[0], labelType]) # Store label name, scope, type (if or while)
    else:
        labelStack.append(["l"+str(labelCounter), bracketPointer[0], labelType]) # Store label name, scope, type (if or while)

    labelCounter+=1
    






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