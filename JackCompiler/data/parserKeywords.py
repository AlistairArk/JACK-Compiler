'''




'''
from . import lexer, symbolTable
from . codeGen import *
import copy

objectType = ""
returnList = []


def Class(token):
    token = lexer.getNextToken()

    if token[0]!="id":
        Error(token, "Expected 'id'")
    else:
        symbolTable.className = token[1]

    if lexer.peekNextToken()[1]!="{":
        Error(token, "Expected '{'")

    return[1]



def constructor(token):     # Check function is of correct type
    global objectType
    objectType = "constructor"

    token = lexer.getNextToken()
    if not token[1] == symbolTable.className:
        return [0, "Invalid method declaration of type "+str(token[1])]

    attribute = token[1]

    setObjectName()
    text("push constant "+str(symbolTable.staticVarCount))

    # Alloc memory
    text("call Memory.alloc 1")
    text("pop pointer 0")

    return setObjectArgs(attribute)


def method(token):          

    # Check method is of correct type
    global objectType
    objectType = "method"

    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void", symbolTable.className] and token[0] != "keyword": # Class name can be used in constructors
        return [0, "Invalid method declaration of type "+str(token[1])]


    attribute = token[1]
    setObjectName()

    symbolTable.symbolIndexList = [[],[]] # Reset symbolIndexList on creation of new object

    #Function header is the first argument to be added to the symbol table
    symbolTable.addSymbol(type="argument", attribute=attribute, symbol=symbolTable.className+"."+symbolTable.objectName, scope=symbolTable.objectName)

    # Push argument
    text("push argument 0")
    text("pop pointer 0")

    return setObjectArgs(attribute)


def function(token):
    global objectType
    objectType = "function"

    symbolTable.symbolIndexList = [[],[]] # Reset symbolIndexList on creation of new object

    # Check function is of correct type
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void", symbolTable.className] and token[0] != "keyword": # Class name can be used in constructors
        return [0, "Invalid method declaration of type "+str(token[1])]

    attribute = token[1]

    setObjectName()
    return setObjectArgs(attribute)



def setObjectName():
    # Check function has appropriate type and name
    token = lexer.getNextToken()
    if token[0] != "id":
        Error(token, "Expected 'id'")

    # Reset counter and set new name on entry to new object
    symbolTable.objectName = token[1]
    symbolTable.labelCounter = [0,0,0]

    # Get number of declared variables in function
    while (token[1]!="{"): # loop to start of function
        token = lexer.peekNextToken()
        if token[0] == "EOF":
            Error(token, "Unexpected EOF")

    # Loop to end of the function
    # Incriment variable counter each time one is encountered
    bCount=1
    varCount=0
    while bCount:
        token = lexer.peekNextToken()

        if token[1] == "var":
            token = lexer.peekNextToken() # Consume data type

            # Check syntax of variables and add them to the symbol table
            tokenSwitch = 1 # Switch between checking for id and symbol with each loop
            while token[1]!=";":
                token = lexer.peekNextToken()

                if token[1]!=";":
                    if tokenSwitch:
                        if token[0]!="id":
                            Error(token,"Expected token of type 'identifier'")
                        else:
                            varCount+=1
                        tokenSwitch = 0
                    else:
                        if token[0]!="symbol" and token[1]!="," :
                            Error(token,"Expected ','")
                        else:
                            tokenSwitch = 1
                
                if token[0] == "EOF":
                    Error(token, "Unexpected EOF")

        if token[1]=="{":
            bCount+=1
        elif token[1]=="}":
            bCount-=1

        if token[0] == "EOF":
            Error(token, "Unexpected EOF")

    text("function "+symbolTable.className+"."+symbolTable.objectName+" "+str(varCount))


def setObjectArgs(attribute):

    # Log bracket count when entering a function so you can later tell when the function is exited
    #                       function name,           bracket pointer,    value returned
    returnList.append([symbolTable.objectName, symbolTable.bracketPointer[0], 0])


    token = lexer.getNextToken()
    if token[1]!="(" and token[0]!="symbol":
        Error(token, "Expected '('")

    peekToken = lexer.peekNextToken()
    if peekToken[1]==")" and peekToken[0]=="symbol":   # Check if function has no arguments
        lexer.getNextToken()            # Consume the token

    else:
        # Check syntax of function arguments
        expectedTypeList = [["keyword","id"],["id"],["symbol"]]
        expectedTypePointer = 0
        while token[1]!=")":
            token = lexer.getNextToken()


            if token[0] not in expectedTypeList[expectedTypePointer]:

                Error(token, "Expected a type followed by a variable name")

            elif expectedTypePointer == 0:
                pass


            elif expectedTypePointer == 1: # add variable to symbol table
                    symbolTable.addSymbol(type="argument",attribute=attribute, symbol=token[1], scope="")

            elif expectedTypePointer == 2:
                if not token[1] in [",", ")"]:
                    Error(token, "Expected ')' or ',' in parameters list")

            # incriment pointer
            expectedTypePointer+=1
            if expectedTypePointer == 3:
                expectedTypePointer = 0


    token = lexer.peekNextToken()
    if token[1]!="{" and token[0]!="symbol":
        Error(token, "Expected '{'")

    return [1]




def int(token):
    token = lexer.getNextToken()
    attribute = token[1]
    return createVar(token,attribute,"int")

def boolean(token):
    token = lexer.getNextToken()
    attribute = token[1]
    return createVar(token,attribute,"boolean")

def char(token):
    token = lexer.getNextToken()
    attribute = token[1]
    return createVar(token,attribute,"char")

def void(token):
    token = lexer.getNextToken()
    attribute = token[1]
    return createVar(token,attribute,"void")

def static(token):
    token = lexer.getNextToken()
    attribute = token[1]
    return createVar(token,attribute,"static")

def field(token):
    token = lexer.getNextToken()
    attribute = token[1]
    return createVar(token,attribute,"field")



def var(token):
    token = lexer.getNextToken()

    if not token[1] in ["int", "boolean", "char", "void", "Array"] and token[0]!="id":
        return [0, "declared variable is of invalid type"]

    attribute = token[1]
    return createVar(token, attribute, 0)



def createVar(token, attribute, context):

    # Check syntax of variables and add them to the symbol table
    tokenSwitch = 1 # Switch between checking for id and symbol with each loop

    while token[1]!=";":
        token = lexer.getNextToken()
        if token[1]!=";":
            if tokenSwitch:
                if token[0]!="id":
                    Error(token, "Identifier expected")
                else:
                    if objectType == "": # If refrenced from static context
                        symbolTable.addSymbol(type=context, attribute=attribute, symbol=token[1], scope=symbolTable.objectName)
                    else:
                        symbolTable.addSymbol(type="local", attribute=attribute, symbol=token[1], scope=symbolTable.objectName)

                tokenSwitch = 0
            else:
                if token[0]!="symbol" and token[1]!="," :
                    Error(token, "Symbol expected")
                else:
                    tokenSwitch = 1

    return [1]



def let(token):

    token = lexer.getNextToken()
    if token[0]!="id":
        return [0, "Expected 'id'"]


    peekToken = lexer.peekNextToken()
    if peekToken[1]=="[" and peekToken[0]=="symbol": # Check if array

        expr = [token]                          # Stores list of tokens in expression
        lexer.getNextToken()                    # consume token
        expr[-1][0]="array"
        expr[-1][1] = [copy.copy(expr[-1]), []] # store function with arguments
        bCount = 1
        while bCount:                           # Exit on obtaining all parameters
            token = lexer.getNextToken()

            if token[1]=="[" and token[0]=="symbol":
                bCount+=1
            elif token[1]=="]" and token[0]=="symbol":
                bCount-=1

            if bCount:
                expr[-1][1][1].append(token)

        token = lexer.peekNextToken() # Revert peek

        symbolTable.arrayLetSwitch = 1
        symbolTable.expressionToCode(expr)
        symbolTable.arrayLetSwitch = 0


        getToken = lexer.getNextToken()
        if getToken[1]!="=" and getToken[0]!="operator":
            return [0, "Expected '='"]

        returnData = symbolTable.orderExpr("let")
        if not returnData[0]:
            return returnData

        text("pop temp 0")
        text("pop pointer 1")
        text("push temp 0")
        text("pop that 0")


    else:
        popData = symbolTable.pushPop(token)

        getToken = lexer.getNextToken()
        if getToken[1]!="=" and getToken[0]!="operator":
            return [0, "Expected '='"]

        returnData = symbolTable.orderExpr("let")
        if not returnData[0]:
            return returnData
        text("pop "+popData[0]+" "+str(popData[1]))

    return [1]



def do(token):
    returnData = symbolTable.orderExpr("do")
    text("pop temp 0")
    if not returnData[0]:
        return returnData

    return [1]



def If(token):
    symbolTable.newLabel("if")
    symbolTable.orderExpr("if")         # (Generate expression code)

    text("if-goto IF_TRUE"+symbolTable.labelStack[-1][0])
    text("goto IF_FALSE"+symbolTable.labelStack[-1][0])
    text("label IF_TRUE"+symbolTable.labelStack[-1][0])

    return [1]



def Else(token):

    peekToken = lexer.peekNextToken()
    if peekToken[1]!="{" and peekToken[0]!="symbol":
        Error(token, "Expected '{'")

    return [1]



def While(token):
    symbolTable.newLabel("while")

    text("label WHILE_EXP"+symbolTable.labelStack[-1][0])
    symbolTable.orderExpr("while")      # Generate expression code

    # Go to end of loop if condition is false
    text("not")
    text("if-goto WHILE_END"+symbolTable.labelStack[-1][0])

    return [1]



def Return(token):

    if len(returnList):
        returnList[-1][2]=1

    token = lexer.peekNextToken()
    if token[1]==";" and token[0]=="symbol":
        lexer.getNextToken() # consume the token
        # No value to be returned, just push const 0
        text("push constant 0")
        if lexer.peekNextToken()[1]!="}":
            Error(token, "Unreachable code")


    elif token[0] in ["id","number"]:
        # Return expression
        returnData = symbolTable.orderExpr("return")
        if not returnData[0]:
            return returnData

    elif token[1] == "this":
        text("push pointer 0")

    else:
        Error(token, "Unexpected token of type '"+token[0]+"' cannot be returned.")

    text("return")
    return [1]


def true(token):
    return [1]

def false(token):
    return [1]

def null(token):
    return [1]

def this(token):
    return [1, token]



def symbol(token):

    if token[1]=="{" and token[0]=="symbol":
        symbolTable.bracketPointer[0]+=1
    if token[1]=="}" and token[0]=="symbol":
        symbolTable.bracketPointer[0]-=1

        # Verify last function exited has a return
        if len(returnList) and (symbolTable.bracketPointer[0]==returnList[-1][1]):
            if not returnList[-1][2]:
                Error(token, "In subroutine '"+returnList[-1][0]+"': Program flow may reach end of subroutine without 'return'")


        if not symbolTable.bracketPointer[0]:
            Error(token, "Mismatched number of braces")
        else:
            # Check stack to detect closing of if or while loop
            for item in symbolTable.labelStack:
                if item[1]==symbolTable.bracketPointer[0]:

                    # Check type
                    if item[2] == "while":
                        text("goto WHILE_EXP"+item[0])
                        text("label WHILE_END"+item[0])
                        symbolTable.labelStack.pop()
                    elif item[2] == "if":
                        symbolTable.labelStack.pop()

                        peekToken = lexer.peekNextToken()
                        if peekToken[1]=="else":
                            symbolTable.newLabel("else")
                            text("goto IF_END"+symbolTable.labelStack[-1][0])

                        text("label IF_FALSE"+item[0])

                    elif item[2] == "else":
                        text("label IF_END"+item[0])
                        symbolTable.labelStack.pop()

                    elif item[2] == "retun":
                        text("label IF_END"+item[0])
                        symbolTable.labelStack.pop()

    if token[1]=="(" and token[0]=="symbol":
        symbolTable.bracketPointer[1]+=1
    if token[1]==")" and token[0]=="symbol":
        symbolTable.bracketPointer[1]-=1
        if not symbolTable.bracketPointer[1]:
            Error(token, "Mismatched number of parenthesis")

    if token[1]=="[" and token[0]=="symbol":
        symbolTable.bracketPointer[2]+=1
    if token[1]=="]" and token[0]=="symbol":
        symbolTable.bracketPointer[2]-=1
        if not symbolTable.bracketPointer[2]:
            Error(token, "Mismatched number of square brackets")

    return[1]
