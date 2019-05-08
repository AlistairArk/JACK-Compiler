import lexer
from codeGen import *
import copy


#             type, symbol, index, scope, attribute (data type)
symbolTable = [[],    [],    [],    [],     []]
symbolIndexList = [[],[]]
staticVarCount = 0
methodList = []
className = ""
objectName = ""

#                 {  (  [
bracketPointer = [1, 1, 1]
#                 if, else, while
labelCounter   = [ 0,    0,    0]       # Increment counter as new labels are created
labelStack = []                         # Close loops as they are created

def addSymbol(*args,**kwargs):

    symbolType = kwargs.get("type",0)
    # Check context the symbol is being mentioned in 
    if objectName == "":                            # if referenced from static context
        if kwargs.get("type",0) not in ["static", "argument", "local", "this", "that", "pointer", "temp", "const"]:     # if declared as static
            global staticVarCount
            staticVarCount+=1



    # Add new type to list of indexes as encountered
    if not symbolType in symbolIndexList[0]:
        symbolIndexList[0].append(symbolType)
        symbolIndexList[1].append(-1)
        # if kwargs.get("type",0)=="argument":
        #     symbolIndexList[1].append(0)        # Function args start from index 1
        # else:
        #     symbolIndexList[1].append(-1)       # All other args start at index 0


    symbolIndex = symbolIndexList[0].index(symbolType)
    symbolIndexList[1][symbolIndex] += 1 # Incriment index

    symbolTable[0].append(symbolType)
    symbolTable[1].append(kwargs.get("symbol",0))
    symbolTable[2].append(kwargs.get("index",symbolIndexList[1][symbolIndex]))
    symbolTable[3].append(objectName) # scope            # kwargs.get("scope",0))
    symbolTable[4].append(kwargs.get("attribute",0))

    if symbolType in ["function","class"]: # if function or class add to function stack
        global semicolon
        functionStack[0].append(kwargs.get("symbol",0))
        functionStack[1].append(0)




def resetSymbolIndexList():
    symbolIndexList = [[],[]]




def pushPop(token):

    if token[0]=="number":
        return ["constant", token[1]]
    else:
        # Get data for popping    
        if token[1] in symbolTable[1]:

            # Prioritize symbols declared within scope
            symbolFound = 0
            for i in range(len(symbolTable[0])):
                # if symbol found, and, symbol is in scope 
                if symbolTable[1][i]==token[1] and symbolTable[3][i]==objectName:
                    symbolFound = 1
                    # print("found!!")
                    varIndex = symbolTable[2][i]
                    varType  = symbolTable[0][i]

            # if token[1]=="size":
            #     print("\n\n",varIndex,varType,symbolTable)
            #     exit()


            if not symbolFound: # if symbol could not be found within current scope, default to last declaration OR THROW ERROR
                symbolIndex = symbolTable[1].index(token[1])
                varIndex = symbolTable[2][symbolIndex]
                varType  = symbolTable[0][symbolIndex]


            if varType not in ["static", "argument", "local", "this", "that", "pointer", "temp", "const"]:
                varType = "this"

            # # Check context the symbol is being mentioned in 
            # if symbolTable[3][symbolIndex] == "":           # if static context
            #     if symbolTable[4][symbolIndex]=="static":   # if declared as static

            return [varType, varIndex]
        else:
            # print(symbolTable)
            Error(token,"use of undeclared variable")


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


arrayDepth  = 0
arraySwitch = 0
arrayLetSwitch = 0
def expressionToCode(expr):

    exprLen = len(expr)    # Get the length of the expression


    # Check what type the expression starts with
    if expr[0][0] == "operator":
        exprSwitch=1

    elif expr[0][0] in ["string_literal"]:
        text("push constant "+str(len(expr[0][1])))         # Push length of string
        text("call String.new 1")                           # Call string function
        for item in expr[0][1]:                             # Create string
            text("push constant "+str(ord(item)))
            text("call String.appendChar 2")
        return

    elif expr[0][0] in ["id","number","array","function"] or expr[0][1] in ["this","true","false","null"]:
        exprSwitch=0
    
    # print(expr)

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
                print("pass")

                global arrayLetSwitch

                if arrayLetSwitch:

                    popPushSwitch = 0
                    for item in token[1][1]:
                        # print(item[1], "==", "[")
                        if item[1]=="[":

                            popPushSwitch = 1
                            print(popPushSwitch)
                    print("\n\nSwitch state: ",popPushSwitch)

                    # exprArrayHandler(token)

                    expr = token
                    
                    counter = 0

                    exprFunctionRunParam(expr[1][1])
                    pushData = pushPop(expr[1][0])
                    print(popPushSwitch)


                    if popPushSwitch: # Ensure this only runs on bottommost depth of 
                        text("pop pointer 1")
                        text("push that 0")
                        text("push "+pushData[0]+" "+str(pushData[1]))
                        text("add")

                    else:
                        text("push "+pushData[0]+" "+str(pushData[1]))
                        text("add")

                    print("\n\n")
                    # print("Switch state: ",popPushSwitch)
                    # print("fin")



                else:
                    # popPushSwitch = 1
                    # for item in token[1][1]:
                        # print(item[1], "==", "[")
                        # if item[1]=="[":
                            # print("ahh")
                            # popPushSwitch = 0
                            # print(popPushSwitch)


                    # exprArrayHandler(token)
                    expr = token


                    print(expr)
                    # expr = []
                    counter = 0

                    exprFunctionRunParam(expr[1][1])
                    pushData = pushPop(expr[1][0])
                    text("push "+pushData[0]+" "+str(pushData[1]))
                    text("add")



                    # if popPushSwitch: # Ensure this only runs on bottommost depth of 
                    text("pop pointer 1")
                    text("push that 0")

                    print("WOWEE")


            elif token[0]=="function":
                exprFunctionHandler(token)

            elif token[1]=="this":
                text("push pointer 0")

            elif token[1] in ["true","false"]:
                text("push constant 0")
                if token[1]=="true":
                    text("not")
            
            elif token[1]=="null":
                text("push constant 0")

            else:
 
                pushData = pushPop(token)
                text("push "+pushData[0]+" "+str(pushData[1]))

            if pos>1:
                # if operator!="neg":
                operatorToCode(operator)
                # else:
                #     text("neg")


def exprFunctionRunParam(funcParam):

    '''
    Every time this function is called, stacked functions and arrays must be identified before
    generating code for the expression.
    '''
    expr = []
    counter = 0

    # While counter != number of parameter, and, there is more than one parameter
    while counter!=len(funcParam):
        expr.append(funcParam[counter])

        counter+=1
        if counter!=len(funcParam):

            # Check if next token implies the current token is a function call
            if funcParam[counter-1][0]=="id" and funcParam[counter][1]=="(" and funcParam[counter][0]=="symbol":
                expr[-1][0]="function"
                expr[-1][1] = [expr[-1].copy(), []] # store function with arguments
                bCount = 1
                print(">>>>>",funcParam)
                while bCount: #and counter!=len(funcParam):   # Exit on obtaining all content in brackets 
                    counter+=1

                    if funcParam[counter][1]=="(":
                        bCount+=1
                    elif funcParam[counter][1]==")":
                        bCount-=1

                    if bCount:
                        expr[-1][1][1].append(funcParam[counter])

            # Check if next token implies the current token is array
            elif funcParam[counter-1][0]=="id" and funcParam[counter][1]=="[" and funcParam[counter][0]=="symbol":
                expr[-1][0]="array"
                expr[-1][1] = [expr[-1].copy(), []] # store function with arguments
                bCount = 1
                while bCount: #and counter!=len(funcParam):   # Exit on obtaining all content in brackets 
                    counter+=1

                    if funcParam[counter][1]=="[":
                        bCount+=1
                    elif funcParam[counter][1]=="]":
                        bCount-=1

                    if bCount:
                        expr[-1][1][1].append(funcParam[counter])




    runExpr(expr) # run expr

def exprFunctionHandler(expr):


    def handleParams(expr):
        # Get num of args (to be used when calling the function)
        if expr[1][1]==[]:
            argCount = 0
        else:
            argCount = 1


        # Get a parameter from the function and run the expression to generate it's code
        funcParam = []
        bCount= 0
        for item in expr[1][1]:

            if item[1]=="(":
                bCount+=1
            elif item[1]==")":
                bCount-=1

            if item[1]=="," and not bCount:
                exprFunctionRunParam(funcParam) # run expr
                funcParam = []
                argCount+=1
            else:
                funcParam.append(item)

        exprFunctionRunParam(funcParam) # run final expr


        return argCount



    # Check if method exists in current file      
    if expr[1][0][1] in methodList:
        global className
        text("push pointer 0 ")
        argCount = handleParams(expr)
        text("call "+className+"."+expr[1][0][1]+" "+str(argCount+1))
    else:
        # Assume method exists as lib or external function
        callSplit = expr[1][0][1].split(".")
        for i in range(len(symbolTable[0])):

            # if calling an object, and object is in scope
            if callSplit[0]==symbolTable[1][i]: # and callSplit[0]==symbolTable[3][i] :
                # argCount+=1

                pushData = pushPop([expr[1][0][0],callSplit[0],expr[1][0][2]])
                text("push "+pushData[0]+" "+str(pushData[1]))                  # <<< DOUBLE CHECK + 1 IS RIGHT

                argCount = handleParams(expr)
                    
                if len(callSplit)==2:
                    text("call "+symbolTable[4][i]+"."+callSplit[1]+" "+str(argCount+1))# <<< DOUBLE CHECK + 1 IS RIGHT
                else:
                    text("call "+symbolTable[4][i]+" "+str(argCount+1))

                # if symbolTable[4][i]=="field":
                #     print("pushData: ",pushData)
                #     print(callSplit)
                #     exit()
                # if (symbolTable[4][i]+"."+callSplit[1]) == "Fraction.getNumerator":
                #     exit()
                return


        argCount = handleParams(expr)

        text("call "+expr[1][0][1]+" "+str(argCount))

    return


def exprArrayHandler(expr):
    global arrayDepth
    arrayDepth+=1
    print(expr)
    # expr = []
    counter = 0

    exprFunctionRunParam(expr[1][1])
    pushData = pushPop(expr[1][0])
    text("push "+pushData[0]+" "+str(pushData[1]))
    text("add")
    arrayDepth-=1
    return

    # def handleParams(expr):
    #     # Get num of args (to be used when calling the function)
    #     if expr[1][1]==[]:
    #         argCount = 0
    #     else:
    #         argCount = 1


    #     # Get a parameter from the function and run the expression to generate it's code
    #     funcParam = []
    #     for item in expr[1][1]:
    #         if item[1]==",":
    #             exprFunctionRunParam(funcParam) # run expr
    #             funcParam = []
    #             argCount+=1
    #         else:
    #             funcParam.append(item)

    #     exprFunctionRunParam(funcParam) # run final expr


    #     return argCount



    # # Check if method exists in current file      
    # if expr[1][0][1] in methodList:
    #     global className
    #     text("push pointer 0 ")
    #     argCount = handleParams(expr)
    #     text("call "+className+"."+expr[1][0][1]+" "+str(argCount+1))
    # else:
    #     # Assume method exists as lib or external function
    #     callSplit = expr[1][0][1].split(".")
    #     for i in range(len(symbolTable[0])):

    #         # if calling an object, and object is in scope
    #         if callSplit[0]==symbolTable[1][i]: # and callSplit[0]==symbolTable[3][i] :
    #             # argCount+=1

    #             pushData = pushPop([expr[1][0][0],callSplit[0],expr[1][0][2]])
    #             text("push "+pushData[0]+" "+str(pushData[1]))                  # <<< DOUBLE CHECK + 1 IS RIGHT

    #             argCount = handleParams(expr)
                    
    #             if len(callSplit)==2:
    #                 text("call "+symbolTable[4][i]+"."+callSplit[1]+" "+str(argCount+1))# <<< DOUBLE CHECK + 1 IS RIGHT
    #             else:
    #                 text("call "+symbolTable[4][i]+" "+str(argCount+1))

    #             return


    #     argCount = handleParams(expr)

    #     text("call "+expr[1][0][1]+" "+str(argCount))






def orderExpr(exprType):
    ''' Obtains a list of tokens which comprise an expression '''


    # Perform checks on the expression and wrap it up into a list
    bracketOpenCount = 0
    expr = [] # Stores list of tokens in expression
    token = lexer.peekNextToken()


    if exprType in ["if","while"]:
        ending = "{"
    elif exprType in ["let","do"]:
        ending = ";"
    elif exprType in ["return"]:
        ending = ";"
        token = [token[0],"return",token[2]]
        

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
        elif lastToken[0]=="id" and token[1]=="[":
            lexer.getNextToken() # consume token
            expr[-1][0]="array"
            expr[-1][1] = [expr[-1].copy(), []] # store function with arguments
            bCount = 1
            while bCount:   # Exit on obtaining all parameters
                token = lexer.getNextToken()
                if token[1]=="[":
                    bCount+=1
                elif token[1]=="]":
                    bCount-=1

                if bCount:
                    expr[-1][1][1].append(token)
                    # print(">>>>>>>",token)

            token = lexer.peekNextToken() # Revert peek

    # print("<><><><><><><>", expr, bracketOpenCount)

    return runExpr(expr)



def runExpr(expr):
    ''' Generates code for a given expression '''



    # Discern sub between neg and overwrite token
    neg = 1 # While true convert all '-' to 'neg'
    for i in range(len(expr)):
        if neg and expr[i][1] == "-":           # Set neg if neg enabled
                print("\n\n",expr)
                print(i)

                expr[i][1] = "neg"
                neg = 0

        elif expr[i][0] in ["id","number","function","array"] or (expr[i][0]=="symbol" and expr[i][1] in [")","]","}"]):     # Disable neg if number
            neg = 0

        elif expr[i][0]=="operator" or (expr[i][0]=="symbol" and expr[i][1] in ["(","[","{"]) : 
            # Enable neg if operator or symbol is encountered
            neg = 1




    '''
    # Check for divisions
    The following will ensure expressions RHS of a '/' take president
    over the LHS as the order of code generation is important 
    '''
    counter = 0
    lastBracketOpen = 0
    while counter!=len(expr):# Loop through expression. 
  
        # if '/' or '-' encountered bracket LHS items so they take precedent
        if expr[counter][0]=="operator":
            if (expr[counter][1]=="/" or expr[counter][1]=="-"):

                expr.insert( counter, ['symbol', ')', expr[counter][0]])
                expr.insert( counter, ['symbol', ')', expr[counter][0]])
                expr.insert( lastBracketOpen, ['symbol', '(', expr[lastBracketOpen][0]])
                expr.insert( lastBracketOpen, ['symbol', '(', expr[lastBracketOpen][0]])

                counter+=4
        elif expr[counter][1]=="(":
            lastBracketOpen=counter

        counter+=1

    # May want to add a later pass that does a LHS to RHS sweep and gives RHS an arbitrarily high depth if '-' or '/' are encountered






    print(expr)
    # exit()



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
            if counter>=curPos:     # Shift pos back if item removal will cause shifts (MAY BE UNNECCESARY BECAUSE OF LATER CHECK)
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
        if result[count][1]>=depth:
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




def newLabel(labelType):
    global labelCounter

    if labelType=="if":
        labelStack.append([str(labelCounter[0]), bracketPointer[0], labelType]) # Store label name, scope, type (if or while)
        labelCounter[0]+=1
    elif labelType=="else":
        labelStack.append([str(labelCounter[1]), bracketPointer[0], labelType]) # Store label name, scope, type (if or while)
        labelCounter[1]+=1
    elif labelType=="while":
        labelStack.append([str(labelCounter[2]), bracketPointer[0], labelType]) # Store label name, scope, type (if or while)
        labelCounter[2]+=1

    






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