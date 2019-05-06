import lexer
from symbolTable import *
from codeGen import *

tokenStack = []






className = ""
def Class(token):
    token = lexer.getNextToken()
    print(">>>>",token)

    if token[0]!="id":
        return [0, "'id' expected"]
    else:
        global className
        className = token[1]

    if lexer.peekNextToken()[1]!="{":
        return [0, "'{' expected"]

    return [1]


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
    if token[0] != "id":
        return [0, "'id' expected"]

    text("function "+className+"."+token[1]+" 1")


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
                    addSymbol(type="argument", symbol=token[1], scope="")

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
    token = lexer.getNextToken()
    if not token[1] in ["int", "boolean", "char", "void", "Array"]:
        return [0, "declared variable is of invalid type"]


    # Check syntax of variables and add them to the symbol table
    tokenSwitch = 1 # Switch between checking for id and symbol with each loop
    while token[1]!=";":
        token = lexer.getNextToken()

        if token[1]!=";":
            if tokenSwitch:
                if token[0]!="id":
                    return [0, "Syntax Error: Identifier expected"]
                else:
                    addSymbol(type="local", symbol=token[1], scope="")
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

            expressionToCode([item])

        popData = pushPop(token)


        if lexer.getNextToken()[1]!="]":
            return [0, "']' expected"]

        if lexer.getNextToken()[1]!="=":
            return [0, "'=' expected"]

        returnData = orderExpr("let")
        if not returnData[0]:
            return returnData
        # text("pop "+popData[0]+" "+str(popData[1]))
        text("pop temp 0")
        text("pop pointer 1")
        text("push temp 0")
        text("pop that 0")
        # text("push constant 0")

    else:
        popData = pushPop(token)

        if lexer.getNextToken()[1]!="=":
            return [0, "'=' expected"]

        returnData = orderExpr("let")
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

    returnData = orderExpr("do")
    text("pop temp 0")
    if not returnData[0]:
        return returnData

    return [1]

    # return [0, "'' expected"]

def If(token):
    token = lexer.getNextToken()

    newLabel()
    text("label "+labelStack[-1][0])    # While
    orderExpr("if")                     # (Generate expression code)

    # Go to end of statement if condition is false 
    text("not")
    text("if-goto "+labelStack[-1][0])  # {

    return [1]



def Else(token):
    if lexer.peekNextToken()[1]=="{":
        return [1]
    else:
        return [0, "'{' expected"]





def While(token):
    newLabel()
    
    text("label "+labelStack[-1][0])   
    orderExpr("while")                      # Generate expression code

    # Go to end of loop if condition is false 
    text("not")
    text("if-goto "+labelStack[-1][0])

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
        pushData = pushPop(token)                      # Push Result
        text("push "+pushData[0]+" "+str(pushData[1]))


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
        bracketPointer[0]+=1
    if token[1]=="}":
        bracketPointer[0]-=1
        if not bracketPointer[0]:
            return [0, "Semantic Error: mismatched number of braces"]
        else:
            # Check stack to detect closing of if or while loop
            for item in labelStack:
                if item[1]==bracketPointer[0]:
                    text("goto "+item[0])
                    text(item[0]+" end")
                    labelStack.pop()

    if token[1]=="(":
        bracketPointer[1]+=1
    if token[1]==")":
        bracketPointer[1]-=1
        if not bracketPointer[1]:
            return [0, "Semantic Error: mismatched number of parenthesis"]

    if token[1]=="[":
        bracketPointer[2]+=1
    if token[1]=="]":
        bracketPointer[2]-=1
        if not bracketPointer[2]:
            return [0, "Semantic Error: mismatched number of square brackets"]



    return[1]


