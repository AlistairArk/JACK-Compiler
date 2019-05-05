
import lexer

#             type, symbol, declared flag, scope

symbolTable = [[],    [],        [],        []]


# JACK - Standard Library (Built in functions)
stdlib = [  ["Math",
            "String",
            "Array",
            "Output",
            "Screen",
            "Memory",
            "Keyboard",
            "Sys"],

            [["init","abs","multiply","divide","min","max","sqrt"],
            ["dispose","length","charAt","setCharAt","appendChar","eraseLastChar","intValue","setInt","backSpace","doubleQuote","newLine"],
            ["new","dispose"],
            ["moveCursor","printChar","printString","printInt","println","backSpace"],
            ["clearScreen","setColor","drawPixel","drawLine","drawRectangle","drawCircle"],
            ["peek","poke","alloc","deAlloc"],
            ["keyPressed","readChar","readLine","readInt"],
            ["halt","error","wait"]]
         ]



varType = ["int","str"]




def analyseSemantic():

    token = lexer.peekNextToken()
    while (token[0] != "EOF"):

        token = lexer.getNextToken()
        main(token)
        token = lexer.peekNextToken()

    # Function Calling
    #     - A function cannot be called if it has not been declared
    #         // Store a list of functions each time one is declared
    #         // (check list of do's in symbol table and compare them to the function list)







def addSymbol(*args,**kwargs):
    symbolTable[0].append(kwargs.get("type",0))
    symbolTable[1].append(kwargs.get("symbol",0))
    symbolTable[2].append(kwargs.get("flag",0))
    symbolTable[3].append(kwargs.get("scope",0))

    if kwargs.get("type",0) in ["function","class"]: # if function or class add to function stack
        global semicolon
        functionStack[0].append(kwargs.get("symbol",0))
        functionStack[1].append(0)


def idExists(token):
    #     - A variable has been declared before being used
    #         // As a variable is declared add it to a list of known variables
    if token[1] in symbolTable[1]:
        return 1
    else:
        return 0




def Error(*args):
    print("Error in line " + str(args[0][2]) + " at or near " + str(args[0][1])+ ", " + str(args[1]));
    exit()


classFlag = 0    # Detects when the program is in a class
function  = 0    # Detects when the program is in a function
parentheses = 0  # 
semicolon = 0    # 

conditionalFlag = 0

stack = []
#               function , level
functionStack = [[0],[0]]

def main(token):
    global classFlag, function, parentheses, semicolon
    stack.append(token)

    # print("     ",token)
    if token[1] == "{":
        semicolon += 1

        if len(functionStack[0]) and not functionStack[1][-1]:     # if function stack is not empty, and item depth on stack has not been set
            functionStack[1][-1] = semicolon                       # Add function level onto the function stack


    elif token[1] == "}": 

        if len(functionStack[0]) and semicolon == functionStack[1][-1]: # If exiting from current function depth.
            functionStack[0].pop()
            functionStack[1].pop()

        
        semicolon -= 1
        if semicolon==-1:
            Error(token, "mismatched number of braces")




    elif token[1] == "(": 
        parentheses += 1
    elif token[1] == ")": 
        parentheses -= 1
        if semicolon==-1:
            Error(token, "mismatched number of parentheses")





    elif token[0] == "id":



 
        
        libFunction = 0
        if token[1] in stdlib[0]:
            # Perform a check to ignore the following library functions

            stdlibIndex = stdlib[0].index(token[1]) # Get index of token
            token = lexer.peekNextToken()
            if token[1] == ".":
                token = lexer.peekNextToken()
                if token[1] in stdlib[1][stdlibIndex]:
                    libFunction = 1

                    # Consume Tokens
                    lexer.getNextToken()
                    lexer.getNextToken()





        elif (stack[-2][1]=="method" or stack[-2][1]=="constructor"):
            # Perform a check to ignore method & constructor keywords
            libFunction = 1

        if not libFunction:
            if stack[-2][1] == "class":
                if classFlag:
                    Error(token, "cannot nest class inside a class")
                else:
                    classFlag = 1
                    varType.append(token[1])
                    addSymbol(type="class", symbol=token[1], flag=1, scope=functionStack[0][-1])

            elif stack[-2][1] == "do": # ???
                addSymbol(type="do", symbol=token[1], flag=1, scope=functionStack[0][-1])


          

            elif stack[-3][1] == "method" or stack[-3][1] == "constructor": # Store a list of functions each time one is declared
                # Function Calling

                functionReturnType = stack[-2][1]
                addSymbol(type="function", symbol=token[1], flag=1, scope=functionStack[0][-1])



                #     - The called function has the same number and type of parameters as its declaration
                #         // store parameters paired with the functions declaration
                
                functionDepth = 0
                while not functionDepth: # loop to the start of the function
                    token = lexer.peekNextToken()

                    if token[1] == "{": 
                        functionDepth = 1

                returnFound = 0
                token = lexer.peekNextToken()
                while functionDepth: # ensures a return occurs before the end of a function


                    if token[1] == "{": 
                        functionDepth += 1

                    elif token[1] == "}": 
                        functionDepth -= 1

                    if functionDepth==1 and token[1]=="return": # If return statement on the function level
                        returnFound = 1
                        

                    if token[1]=="return":
                        #     - The function returns a value compatible with the type of the function
                        #         // check current function type before returning values
                        token = lexer.peekNextToken()


                        if functionReturnType =="void":
                            if token[1]!=";":
                                Error(token,"function is void but value was returned")

                        elif token[1]==";" or token[0]=="keyword":
                            pass

                        else:     
                            if token[1] in symbolTable[1]:

                                if symbolTable[0][symbolTable[1].index(token[1])] == "class":       # if return type is class
                                    pass
                                elif symbolTable[0][symbolTable[1].index(token[1])] == "function":  # if items index in symbol table is a function
                                    pass
                                elif symbolTable[0][symbolTable[1].index(token[1])] == functionReturnType:
                                    pass
                                else:
                                    print(symbolTable)
                                    Error(stack[-1],"function type and return don't match")

                            else:                            
                                print("not found",token)
                    else:
                        token = lexer.peekNextToken()





                #     - All paths return a value
                #         // Detect function closing, ensure a return takes place somewhere before the end of the function or at the end of a function.
                #         // some tricks form "unreachable code" may be required
                if not returnFound:
                    Error(token, "function has no return statement")


                




            else:
        
                # Correct usage of variables


                #     - A variable has been initialized before being used in an expression
                #         // each time a variable is initialized, raise flag to indicated it has been initialized


                alternate = 0
                for i in range( len(stack)): # loop till type is discerned
                    item = stack[-(i+1)]


                    # var, comma, var, comma, var, 
                    if (item[1] in varType):
                        # if not alternate:
                            addSymbol(type=item[1], symbol=token[1], flag=1, scope=functionStack[0][-1])
                            break
                        # else:
                        #     Error(token,"invalid alt 1")
                        
                    elif item[1]==",":
                        pass
                        # print("comma")
                        # if alternate:
                        #     alternate = 0
                        # else:
                        #     Error(token,"invalid alt 2")

                    elif item[0] == "id" or item[1]==".":
                        pass
                        # print("id")
                        # if not alternate:
                        #     alternate = 1
                        # else:
                        #     Error(token,"invalid alt 3")
                        
                    else:

                        # Check if variable already exists
                        if idExists(token):
                            #     - Scope resolution (as in nested scopes or local variables)
                            # Check scope of variable

                            varScope = symbolTable[3][symbolTable[1].index(token[1])] # get variable scope in symbol table 
                            if varScope in functionStack[0]:
                                return # Variable in scope
                            else:
                                print(symbolTable)
                                print(token)
                                Error(token,"variable used outside scope")                # If variable is being used outside scope log error

                        else:
                            Error(token, "use of undeclared variable")

                return



    
    elif token[0] == "keyword":

        if token[1] == "let":

            # Type checking
            #     - The RHS of an assignment statement is type compatible with the LHS
            #     - Coercion, ie. converting one type to another, for example in assignment parameter passing
            #     - Expressions used in array indices's have an integer value

            if lexer.peekNextToken()[0] != "id":
                Error(token,"")
            else:
                pass # Check ID in type in symbol table

            if lexer.peekNextToken()[0] != "symbol":
                Error(token,"")


    
    # Other
    #     - Unreachable Code (eg. following a non-conditional return in the body of the function)
    elif token[1] == "return":

        while token[1]!=";":                        # Loop to the end of the return statement
            token = lexer.peekNextToken()

        # Ensure the next token is the end of a function or condition
        if lexer.peekNextToken()[1] != "}":
            Error(token, "unreachable code")




    









'''
EVERYTHING BELOW THIS LINE IS INTENDED TO BE USED IN TESTING THE SEMANTIC ANALYSER 

The following will take a list of tokens and input them into the semantic analyser.

'''


