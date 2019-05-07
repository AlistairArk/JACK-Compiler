import lexer, symbolTable
# from symbolTable import *
from codeGen import *

tokenStack = []







def Class(token):
    token = lexer.getNextToken()


    if token[0]!="id":
        return [0, "'id' expected"]
    else:

        symbolTable.className = token[1]

    if lexer.peekNextToken()[1]!="{":
        return [0, "'{' expected"]

    return [1]




objectType = ""
def constructor(token):     # Check function is of correct type
    global objectType
    objectType = "constructor"

    token = lexer.getNextToken()
    if not token[1] == symbolTable.className:
        return [0, "Invalid method declaration of type "+str(token[1])]
        # return [0, "unexpected function type"]

    attribute = token[1]

    setObjectName()
    text("push constant "+str(constructorPushConstant))

    # Alloc memory
    text("call Memory.alloc 1")
    text("pop pointer 0")

    return setObjectArgs(attribute)


def method(token):          # Check method is of correct type
    global objectType
    objectType = "method"

    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void", symbolTable.className] and token[0] != "keyword": # Class name can be used in constructors
        return [0, "Invalid method declaration of type "+str(token[1])]
    # if token[0] != "keyword":
    #     print(symbolTable.className)

    attribute = token[1]

    setObjectName()

    # Push argument
    text("push argument 0")
    text("pop pointer 0")

    # exit()

    return setObjectArgs(attribute)


def function(token): # function int mult
    global objectType
    objectType = "function"

    # Check function is of correct type
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void", symbolTable.className] and token[0] != "keyword": # Class name can be used in constructors
        return [0, "Invalid method declaration of type "+str(token[1])]

    attribute = token[1]

    setObjectName()
    return setObjectArgs(attribute)



# functionCounter = 0
def setObjectName():
    # Check function has appropriate type and name
    token = lexer.getNextToken()
    if token[0] != "id":
        Error(token, "'id' expected")

    symbolTable.objectName = token[1]

    # Get number of declared variables in function
    while (token[1]!="{"): # loop to start of function
        token = lexer.peekNextToken()
        eof(token)

    # Loop to end of the function
    # Incriment variable counter each time one is encountered
    bCount=1
    varCount=0
    while bCount:
        token = lexer.peekNextToken()
        # print(token)
        if token[1] == "var":
            token = lexer.peekNextToken() # Consume data type

            # Check syntax of variables and add them to the symbol table
            tokenSwitch = 1 # Switch between checking for id and symbol with each loop
            while token[1]!=";":
                token = lexer.peekNextToken()
                # print(token)
                if token[1]!=";":
                    if tokenSwitch:
                        if token[0]!="id":
                            Error(token,"Syntax Error: Identifier expected")
                        else:
                            varCount+=1
                        tokenSwitch = 0
                    else:        
                        if token[0]!="symbol" and token[1]!="," :
                            Error(token,"Syntax Error: Symbol expected")
                        else:
                            tokenSwitch = 1
                eof(token)

        if token[1]=="{":
            bCount+=1
        elif token[1]=="}":
            bCount-=1

        eof(token)

    text("function "+symbolTable.className+"."+symbolTable.objectName+" "+str(varCount))

    # functionCounter+=1

    # Add retroactive call list 


def setObjectArgs(attribute):
    
    symbolTable.symbolIndexList = [[],[]] # Reset symbolIndexList on creation of new object

    token = lexer.getNextToken()
    if token[1]!="(":
        return [0, "'(' expected"]


    if lexer.peekNextToken()[1]==")":   # Check if function has no arguments
        lexer.getNextToken()            # Consume the token

    else:
        ## Check syntax of function arguments
        expectedTypeList = [["keyword","id"],["id"],["symbol"]]
        expectedTypePointer = 0
        while token[1]!=")":
            token = lexer.getNextToken()

            
            if token[0] not in expectedTypeList[expectedTypePointer]:
                exit()
                return [0, "'"+expectedTypeList[expectedTypePointer][0]+"' expected"]
            
            elif expectedTypePointer == 0:
                pass
                # if not token[1] in ["int", "boolean", "char"]: 
                #     return [0, "unexpected keyword type"]
            
            elif expectedTypePointer == 1: # add variable to symbol table
                    symbolTable.addSymbol(type="argument",attribute=attribute, symbol=token[1], scope="")

            elif expectedTypePointer == 2:
                if not token[1] in [",", ")"]: 
                    return [0, "unexpected symbol type"]

            # incriment pointer
            expectedTypePointer+=1
            if expectedTypePointer == 3:
                expectedTypePointer = 0


    token = lexer.peekNextToken()
    if token[1]!="{":
        return [0, "'{' expected"]

    return [1]




def int(token):
    lexer.getNextToken()
    return createVar(token,"int")

def boolean(token):
    lexer.getNextToken()
    return createVar(token,"boolean")

def char(token):
    lexer.getNextToken()
    return createVar(token,"char")

def void(token):
    lexer.getNextToken()
    return createVar(token,"void")

def static(token):
    lexer.getNextToken()
    return createVar(token,"static")

def field(token):
    lexer.getNextToken()
    return createVar(token,"field")








def var(token):
    token = lexer.getNextToken()

    if not token[1] in ["int", "boolean", "char", "void", "Array"] and token[0]!="id":
        return [0, "declared variable is of invalid type"]
    attribute = token[1]

    return createVar(token, attribute)


constructorPushConstant = 0
def createVar(token, attribute):

    # Check syntax of variables and add them to the symbol table
    tokenSwitch = 1 # Switch between checking for id and symbol with each loop
    
    while token[1]!=";":
        token = lexer.getNextToken()

        if token[1]!=";":
            if tokenSwitch:
                if token[0]!="id":
                    return [0, "Syntax Error: Identifier expected"]
                else:
                    if objectType == "":
                        symbolTable.addSymbol(type="this", attribute=attribute, symbol=token[1], scope=symbolTable.objectName)
                    else:
                        symbolTable.addSymbol(type="local", attribute=attribute, symbol=token[1], scope=symbolTable.objectName)

                    if objectType == "":
                        global constructorPushConstant
                        constructorPushConstant+=1
                        
                tokenSwitch = 0
            else:        
                if token[0]!="symbol" and token[1]!="," :
                    return [0, "Syntax Error: Symbol expected"]
                else:
                    tokenSwitch = 1

    return [1]















def let(token):

    token = lexer.getNextToken()
    if token[0]!="id":
        return [0, "'id' expected"]



    if lexer.peekNextToken()[1]=="[": # Check if array
        lexer.getNextToken() # consume token

        for item in [lexer.getNextToken(),token,["operator","+",token[2]]]:

            symbolTable.expressionToCode([item])

        popData = symbolTable.pushPop(token)


        if lexer.getNextToken()[1]!="]":
            return [0, "']' expected"]

        if lexer.getNextToken()[1]!="=":
            return [0, "'=' expected"]

        returnData = symbolTable.orderExpr("let")
        if not returnData[0]:
            return returnData
        # text("pop "+popData[0]+" "+str(popData[1]))
        text("pop temp 0")
        text("pop pointer 1")
        text("push temp 0")
        text("pop that 0")
        # text("push constant 0")

    else:
        popData = symbolTable.pushPop(token)

        if lexer.getNextToken()[1]!="=":
            return [0, "'=' expected"]

        returnData = symbolTable.orderExpr("let")
        if not returnData[0]:
            return returnData
        text("pop "+popData[0]+" "+str(popData[1]))

    return [1]



    # expr = []               # Stores list of tokens in expression
    # while token[1]!=";":    # Create a list of tokens which comprise the expression
    #     expr.append(token)
    #     token = lexer.getNextToken()

    # if len(expr) == 1:
    #     text("push constant "+str(expr[0][1]))






def do(token):

    returnData = symbolTable.orderExpr("do")
    text("pop temp 0")
    if not returnData[0]:
        return returnData

    return [1]



def If(token):

    symbolTable.newLabel("if")                      
    symbolTable.orderExpr("if")                     # (Generate expression code)

    text("if-goto IF_TRUE"+symbolTable.labelStack[-1][0])
    text("goto IF_FALSE"+symbolTable.labelStack[-1][0])
    text("label IF_TRUE"+symbolTable.labelStack[-1][0])

    return [1]



def Else(token):

    if lexer.peekNextToken()[1]!="{":
        return [0, "'{' expected"]
    
    return [1]




def While(token):
    symbolTable.newLabel("while")
    
    text("label WHILE_EXP"+symbolTable.labelStack[-1][0])   
    symbolTable.orderExpr("while")                      # Generate expression code

    # Go to end of loop if condition is false 
    text("not")
    text("if-goto WHILE_END"+symbolTable.labelStack[-1][0])

    return [1]







def Return(token):

    token = lexer.peekNextToken()

    if token[1]==";":
        lexer.getNextToken() # consume the token
        # No value to be returned, just push const 0
        text("push constant 0")
        if lexer.peekNextToken()[1]!="}":
            return [0, "Semantic Error: Unreachable code"]
        


    elif token[0] in ["id","number"]: # or token[1] in ["this"]:                  # Validate token type
        '''
        This section may require further tweaking to make 
        returning multiple values possible.
        '''

        ## Simply returns a given identifier - note this requires modificaton to return expressions
        # pushData = symbolTable.pushPop(token)                      # Push Result
        # text("push "+pushData[0]+" "+str(pushData[1]))

        # Return expression
        returnData = symbolTable.orderExpr("return")
        if not returnData[0]:
            return returnData

    elif token[1] == "this":
        # text("pop this 0")
        text("push pointer 0")

    else:
        return [0, "Syntax Error: Unexpected token of type '"+token[0]+"' cannot be returned."]

    text("return")
    return [1]




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



def symbol(token):

    if token[1]=="{":
        symbolTable.bracketPointer[0]+=1
    if token[1]=="}":
        symbolTable.bracketPointer[0]-=1
        if not symbolTable.bracketPointer[0]:
            return [0, "Semantic Error: mismatched number of braces"]
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

    if token[1]=="(":
        symbolTable.bracketPointer[1]+=1
    if token[1]==")":
        symbolTable.bracketPointer[1]-=1
        if not symbolTable.bracketPointer[1]:
            return [0, "Semantic Error: mismatched number of parenthesis"]

    if token[1]=="[":
        symbolTable.bracketPointer[2]+=1
    if token[1]=="]":
        symbolTable.bracketPointer[2]-=1
        if not symbolTable.bracketPointer[2]:
            return [0, "Semantic Error: mismatched number of square brackets"]



    return[1]


