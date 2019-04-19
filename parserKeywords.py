import lexer
from symbolTable import *
from codeGen import *

tokenStack = []







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
    if not token[1] in ["int", "boolean", "char", "void"]:
        return [0, "'' expected"]


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










#             type, symbol, index, scope
def let(token):

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




    expr = []               # Stores list of tokens in expression
    while token[1]!=";":    # Create a list of tokens which comprise the expression
        expr.append(token)
        token = lexer.getNextToken()

    if len(expr) == 1:
        text("push constant "+str(expr[0][1]))
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
        for token in expr:
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




    text("pop "+popData[0]+" "+str(popData[1]))


    return [1]












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
    if lexer.peekNextToken()[1]=="{":
        return [1]
    else:
        return [0, "'{' expected"]





labelCounter = 0    # Increment counter as new labels are created
labelStack = []     # Close loops as they are created
def While(token):
    global labelCounter
    labelCounter+=1
    labelStack.append(["l"+str(labelCounter), bracketPointer[0]]) # Store label name and scope
    
    text("label "+labelStack[-1][0])

    expr = [] # Stores list of tokens in expression
    while lexer.peekNextToken()[1]!="{":
        expr.append(lexer.getNextToken())

    orderExpr(expr)

    return [1]

    # return [0, "'' expected"]





def Return(token):

    token = lexer.getNextToken()
    if token[1]==";":
        if lexer.peekNextToken()[1]!="}":
            return [0, "Semantic Error: Unreachable code"]

    elif token[0] in ["id"]:        # Validate token type
        pushData = pushPop(token)   # Push Result
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


#                 {  (  [
bracketPointer = [1, 1, 1]
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

    # for item in bracketPointer:
    #     if not item:
    #         print("wowee")
    #         return [0, "mismatched parenthesis."]

    return[1]


