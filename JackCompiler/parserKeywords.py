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
        return [0, "unexpected function type"]

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
    if not token[1] in ["int", "boolean", "char", "void", symbolTable.className]: # Class name can be used in constructors
        return [0, "unexpected method type"]
    if token[0] != "keyword":
        return [0, "'keyword' expected"]

    attribute = token[1]

    setObjectName()

    # Push argument
    text("push argument 0")
    text("pop pointer 0")

    return setObjectArgs(attribute)


def function(token): # function int mult
    global objectType
    objectType = "function"

    # Check function is of correct type
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void"]:
        return [0, "unexpected function type"]
    if token[0] != "keyword":
        return [0, "'keyword' expected"]

    attribute = token[1]

    setObjectName()
    return setObjectArgs(attribute)


objectName = ""
functionCounter = 0
def setObjectName():
    # Check function has appropriate type and name
    token = lexer.getNextToken()
    if token[0] != "id":
        Error(token, "'id' expected")

    global objectName,functionCounter
    objectName = token[1]
    text("function "+symbolTable.className+"."+objectName+" "+str(functionCounter))
    functionCounter+=1

    # Add retroactive call list 


def setObjectArgs(attribute):
    
    symbolTable.resetSymbolIndexList() # Reset symbolIndexList on creation of new object

    token = lexer.getNextToken()
    if token[1]!="(":
        return [0, "'(' expected"]


    if lexer.peekNextToken()[1]==")":   # Check if function has no arguments
        lexer.getNextToken()            # Consume the token

    else:
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
                    symbolTable.addSymbol(type="argument",attribute=attribute, symbol=token[1], scope="")

            elif token[0] == "symbol":
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
    print("             ",lexer.peekNextToken())
    return createVar(token)

def boolean(token):
    print("             ",lexer.peekNextToken())
    return createVar(token)

def char(token):
    print("             ",lexer.peekNextToken())
    return createVar(token)

def void(token):
    print("             ",lexer.peekNextToken())
    return createVar(token)




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
                        symbolTable.addSymbol(type="this", attribute=attribute, symbol=token[1], scope=objectName)
                    else:
                        symbolTable.addSymbol(type="local", attribute=attribute, symbol=token[1], scope=objectName)

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










def static(token):
    return [1]

    return [0, "'' expected"]

def field(token):
    return [1]

    return [0, "'' expected"]











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
    if lexer.peekNextToken()[1]=="{":
        return [1]
    else:
        return [0, "'{' expected"]





def While(token):
    symbolTable.newLabel("while")
    
    text("label "+symbolTable.labelStack[-1][0])   
    symbolTable.orderExpr("while")                      # Generate expression code

    # Go to end of loop if condition is false 
    text("not")
    text("if-goto "+symbolTable.labelStack[-1][0])

    return [1]







def Return(token):

    token = lexer.getNextToken()

    if token[1]==";":
        # No value to be returned, just push const 0
        text("push constant 0")
        if lexer.peekNextToken()[1]!="}":
            return [0, "Semantic Error: Unreachable code"]
        


    elif token[0] in ["id","number"]:                  # Validate token type
        '''
        This section may require further tweaking to make 
        returning multiple values possible.
        '''
        pushData = symbolTable.pushPop(token)                      # Push Result
        text("push "+pushData[0]+" "+str(pushData[1]))

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
                        text("goto "+item[0])
                        text(item[0]+" end")
                        symbolTable.labelStack.pop()
                    elif item[2] == "if":
                        text("label IF_FALSE"+item[0])



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


