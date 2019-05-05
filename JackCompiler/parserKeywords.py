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


    if lexer.peekNextToken()[1]==")":   # Check if function has no arguments
        lexer.getNextToken()            # Consume the token

    else:
        ## Check syntax of function arguments
        expectedTypeList = ["keyword","id","symbol"]
        expectedTypePointer = 0
        while token[1]!=")":
            token = lexer.getNextToken()
            print(token)
            
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


    # expr = []               # Stores list of tokens in expression
    # while token[1]!=";":    # Create a list of tokens which comprise the expression
    #     expr.append(token)
    #     token = lexer.getNextToken()

    # if len(expr) == 1:
    #     text("push constant "+str(expr[0][1]))


    # expr = []               # Stores list of tokens in expression
    # while token[1]!=";":    # Create a list of tokens which comprise the expression
    #     expr.append(token)
    #     token = lexer.getNextToken()

    # if len(expr) == 1:
    #     text("push constant "+str(expr[0][1]))
    # else: # Handle expression

    #     '''
    #     # First check expression has correct syntax
        
    #     expectedTypePointer  - Handel's switching between operator and id/number
    #     expressionCounter    - Counts number of operands encountered.
    #                            After encountering 2 the operator is handled and the counter is reset.
    #     '''
    #     expectedTypePointer = 0 
    #     expressionCounter = 0   
    #     operator = []
    #     for token in expr:
    #         if expectedTypePointer:
    #             if token[0] != "operator":
    #                 return [0, "Syntax Error: Invalid type in expression. 'operator' expected"]
    #             expectedTypePointer = 0
    #             operator=token

    #         else:
                
    #             if not token[0] in ["id","number"]:
    #                 if token[0] == "operator" and token[1] == "-":
    #                     expressionCounter = 1
    #                     operator = "neg"
    #                 else:
    #                     return [0, "Syntax Error: Invalid type in expression. 'id' or 'number' expected"]
    #             else:
    #                 expectedTypePointer = 1
    #                 expressionCounter+=1

    #                 pushData = pushPop(token)
    #                 text("push "+pushData[0]+" "+str(pushData[1]))
    
    #                 if expressionCounter>=2:
    #                     # expressionCounter = 0
    #                     if operator!="neg":
    #                         operatorToCode(operator)
    #                     else:
    #                         text("neg")


    #     if not expectedTypePointer:
    #         return [0, "Syntax Error: Expression ends in 'operator'. 'id' or 'number' expected"]









def static(token):
    return [1]

    return [0, "'' expected"]

def field(token):
    return [1]

    return [0, "'' expected"]







'''
function Main.main 4

"How many numbers? "

push constant 18                        call String.new 1
push constant 72                        call String.appendChar 2
push constant 111                       call String.appendChar 2
push constant 119                       call String.appendChar 2
push constant 32                        call String.appendChar 2
push constant 109                       call String.appendChar 2
push constant 97                        call String.appendChar 2
push constant 110                       call String.appendChar 2
push constant 121                       call String.appendChar 2
push constant 32                        call String.appendChar 2
push constant 110                       call String.appendChar 2
push constant 117                       call String.appendChar 2
push constant 109                       call String.appendChar 2
push constant 98                        call String.appendChar 2
push constant 101                       call String.appendChar 2
push constant 114                       call String.appendChar 2
push constant 115                       call String.appendChar 2
push constant 63                        call String.appendChar 2
push constant 32                        call String.appendChar 2


call Keyboard.readInt 1                 pop local 1
push constant 0
return

'''


def let(token):

    token = lexer.getNextToken()
    if token[0]!="id":
        return [0, "'id' expected"]

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
    return [1]

    return [0, "'' expected"]

def If(token):
    token = lexer.getNextToken()

    newLabel()
    text("label "+labelStack[-1][0])    # While
    orderExpr("if")                     # (Generate expression code)
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
    text("if-goto "+labelStack[-1][0])

    return [1]







def Return(token):

    token = lexer.getNextToken()

    if token[1]==";":
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


