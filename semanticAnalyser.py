
import lexer

#             type, symbol, declared flag, scope

symbolTable = [[],    [],        [],        []]


# JACK - Standard Library (Built in functions)
stdlib = [ "Math",          "init","abs","multiply","divide","min","max","sqrt",
           "String",        "dispose","length","charAt","setCharAt","appendChar","eraseLastChar","intValue","setInt","backSpace","doubleQuote","newLine",
           "Array",         "new","dispose",
           "Output",        "moveCursor","printChar","printString","printInt","println","backSpace",
           "Screen",        "clearScreen","setColor","drawPixel","drawLine","drawRectangle","drawCircle",
           "Memory",        "peek","poke","alloc","deAlloc",
           "Keyboard",      "keyPressed","readChar","readLine","readInt",
           "Sys",           "halt","error","wait"]


varType = ["int","str"]




def banProg():

    token = lexer.peekNextToken()
    while (token[0] != "EOF"):

        token = lexer.getNextToken()
        main(token)
        token = lexer.peekNextToken()






def addSymbol(*args,**kwargs):
    symbolTable[0].append(kwargs.get("type",0))
    symbolTable[1].append(kwargs.get("symbol",0))
    symbolTable[2].append(kwargs.get("flag",0))
    symbolTable[3].append(kwargs.get("scope",0))

def idExists(token):
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
functionStack[]

def main(token):
    global classFlag, function, parentheses, semicolon
    stack.append(token)




    if token[0] == "{": 
        semicolon += 1

    elif token[0] == "}": 
        semicolon -= 1
        if semicolon==-1:
            Error(token, "mismatched number of semicolons")


    elif token[0] == "(": 
        parentheses += 1
    elif token[0] == ")": 
        parentheses -= 1
        if semicolon==-1:
            Error(token, "mismatched number of parentheses")





    elif token[0] == "id":

        
        # Correct usage of variables
        #     - A variable has been declared before being used
        #         // As a variable is declared add it to a list of known variables

        #     - A variable has been initialized before being used in an expression
        #         // each time a variable is initialized, raise flag to indicated it has been initialized

        #     - Scope resolution (as in nested scopes or local variables)



        # First perform a check to ignore the following:
        #     - library functions
            
        
        if token[1] in stdlib or (stack[-2][1]=="method" or stack[-2][1]=="constructor"):
            pass
        else:
            if stack[-2][1] == "class":
                if classFlag:
                    Error(token, "cannot nest class inside a class")
                else:
                    classFlag = 1
                    varType.append(token[1])
                    addSymbol(type="class", symbol=token[1], flag=1)

            elif stack[-2][1] == "do": # ???
                addSymbol(type="do", symbol=token[1], flag=1)




            # Function Calling
            #     - A function cannot be called if it has not been declared
            #         // Store a list of functions each time one is declared
            #         // (check list of do's in symbol table and compare them to the function list)

            #     - The called function has the same number and type of parameters as its declaration
            #         // store parameters paired with the functions declaration

            #     - The function returns a value compatible with the type of the function
            #         // check current function type before returning values
          
          

            elif stack[-3][1] == "method" or stack[-3][1] == "constructor": # Store a list of functions each time one is declared
                function = 1
                
                addSymbol(type="function", symbol=token[1], flag=1)


            elif idExists(token):
                # Check scope of variable

                # If variable is being used outside scope log error
                pass



            else:
                print(token)
                alternate = 0
                for i in range( len(stack)): # loop till type is discerned
                    item = stack[-(i+1)]
                    print(item)

                    # var, comma, var, comma, var, 
                    if (item[1] in varType):
                        # if not alternate:
                            addSymbol(type="var", symbol=token[1], flag=1)
                            break
                        # else:
                        #     Error(token,"invalid alt 1")
                        
                    elif item[1]==",":
                        print("comma")
                        # if alternate:
                        #     alternate = 0
                        # else:
                        #     Error(token,"invalid alt 2")

                    elif item[0] == "id" or item[1]==".":
                        print("id")
                        # if not alternate:
                        #     alternate = 1
                        # else:
                        #     Error(token,"invalid alt 3")
                    else:
                        Error(token, "use of undeclared variable")

                print("\n")
                return



    

    # Type checking
    #     - The RHS of an assignment statement is type compatible with the LHS

    #     - Coercion, ie. converting one type to another, for example in assignment parameter passing
        
    #     - Expressions used in array indices's have an integer value
    



    




    # Other
    #     - Unreachable Code (eg. following a non-conditional return in the body of the function)
    elif token[1] == "return":


        #     - All paths return a value
        #         // Detect function closing, ensure a return takes place somewhere before the end of the function or at the end of a function.
        #         // some tricks form "unreachable code" may be required
            
        while token[1]!=";":                        # Loop to the end of the return statement
            token = lexer.peekNextToken()
            print(token)

        # Ensure the next token is the end of a function or condition
        if lexer.peekNextToken()[1] != "}":
            Error(token, "unreachable code")


    

    










'''
EVERYTHING BELOW THIS LINE IS INTENDED TO BE USED IN TESTING THE SEMANTIC ANALYSER 

The following will take a list of tokens and input them into the semantic analyser.

'''

# tokens = [['operator', '/', 10], ['keyword', 'class', 12], ['id', 'Fraction', 12], ['symbol', '{', 12], ['keyword', 'field', 14], ['keyword', 'int', 14], ['id', 'numerator', 14], ['symbol', ',', 14], ['id', 'denominator', 14], ['symbol', ';', 14], ['operator', '/', 18], ['keyword', 'constructor', 20], ['id', 'Fraction', 20], ['id', 'new', 20], ['symbol', '(', 20], ['keyword', 'int', 20], ['id', 'x', 20], ['symbol', ',', 20], ['keyword', 'int', 20], ['id', 'y', 20], ['symbol', ')', 20], ['symbol', '{', 20], ['keyword', 'let', 22], ['id', 'numerator', 22], ['symbol', '=', 22], ['id', 'x', 22], ['symbol', ';', 22], ['keyword', 'let', 24], ['id', 'denominator', 24], ['symbol', '=', 24], ['id', 'y', 24], ['symbol', ';', 24], ['keyword', 'do', 26], ['id', 'reduce', 26], ['symbol', '(', 26], ['symbol', ')', 26], ['symbol', ';', 26], ['keyword', 'return', 28], ['keyword', 'this', 28], ['symbol', ';', 28], ['symbol', '}', 30], ['keyword', 'method', 36], ['keyword', 'void', 36], ['id', 'reduce', 36], ['symbol', '(', 36], ['symbol', ')', 36], ['symbol', '{', 36], ['keyword', 'var', 38], ['keyword', 'int', 38], ['id', 'g', 38], ['symbol', ';', 38], ['keyword', 'let', 40], ['id', 'g', 40], ['symbol', '=', 40], ['id', 'Fraction', 40], ['symbol', '.', 40], ['id', 'gcd', 40], ['symbol', '(', 40], ['id', 'numerator', 40], ['symbol', ',', 40], ['id', 'denominator', 40], ['symbol', ')', 40], ['symbol', ';', 40], ['keyword', 'if', 42], ['symbol', '(', 42], ['id', 'g', 42], ['operator', '>', 42], ['number', '1', 42], ['symbol', ')', 42], ['symbol', '{', 42], ['keyword', 'let', 44], ['id', 'numerator', 44], ['symbol', '=', 44], ['id', 'numerator', 44], ['operator', '/', 44], ['id', 'g', 44], ['symbol', ';', 44], ['keyword', 'let', 46], ['id', 'denominator', 46], ['symbol', '=', 46], ['id', 'denominator', 46], ['operator', '/', 46], ['id', 'g', 46], ['symbol', ';', 46], ['symbol', '}', 48], ['keyword', 'else', 48], ['symbol', '{', 48], ['symbol', '}', 52], ['keyword', 'return', 54], ['symbol', ';', 54], ['symbol', '}', 56], ['operator', '/', 60], ['keyword', 'method', 62], ['keyword', 'int', 62], ['id', 'getNumerator', 62], ['symbol', '(', 62], ['symbol', ')', 62], ['symbol', '{', 62], ['keyword', 'return', 62], ['id', 'numerator', 62], ['symbol', ';', 62], ['symbol', '}', 62], ['keyword', 'method', 64], ['keyword', 'int', 64], ['id', 'getDenominator', 64], ['symbol', '(', 64], ['symbol', ')', 64], ['symbol', '{', 64], ['keyword', 'return', 64], ['id', 'denominator', 64], ['symbol', ';', 64], ['symbol', '}', 64], ['operator', '/', 68], ['keyword', 'method', 70], ['id', 'Fraction', 70], ['id', 'plus', 70], ['symbol', '(', 70], ['id', 'Fraction', 70], ['id', 'other', 70], ['symbol', ')', 70], ['symbol', '{', 70], ['keyword', 'var', 72], ['keyword', 'int', 72], ['id', 'sum', 72], ['symbol', ';', 72], ['keyword', 'let', 74], ['id', 'sum', 74], ['symbol', '=', 74], ['symbol', '(', 74], ['id', 'numerator', 74], ['operator', '*', 74], ['id', 'other', 74], ['symbol', '.', 74], ['id', 'getDenominator', 74], ['symbol', '(', 74], ['symbol', ')', 74], ['symbol', ')', 74], ['operator', '+', 74], ['symbol', '(', 74], ['id', 'other', 74], ['symbol', '.', 74], ['id', 'getNumerator', 74], ['symbol', '(', 74], ['symbol', ')', 74], ['operator', '*', 74], ['id', 'denominator', 74], ['symbol', ')', 74], ['symbol', ';', 74], ['keyword', 'return', 76], ['id', 'Fraction', 76], ['symbol', '.', 76], ['id', 'new', 76], ['symbol', '(', 76], ['id', 'sum', 76], ['symbol', ',', 76], ['id', 'denominator', 76], ['operator', '*', 76], ['id', 'other', 76], ['symbol', '.', 76], ['id', 'getDenominator', 76], ['symbol', '(', 76], ['symbol', ')', 76], ['symbol', ')', 76], ['symbol', ';', 76], ['symbol', '}', 78], ['operator', '/', 86], ['keyword', 'method', 88], ['keyword', 'void', 88], ['id', 'dispose', 88], ['symbol', '(', 88], ['symbol', ')', 88], ['symbol', '{', 88], ['keyword', 'do', 90], ['id', 'Memory', 90], ['symbol', '.', 90], ['id', 'deAlloc', 90], ['symbol', '(', 90], ['keyword', 'this', 90], ['symbol', ')', 90], ['symbol', ';', 90], ['keyword', 'return', 92], ['symbol', ';', 92], ['symbol', '}', 94], ['operator', '/', 98], ['keyword', 'method', 100], ['keyword', 'void', 100], ['id', 'print', 100], ['symbol', '(', 100], ['symbol', ')', 100], ['symbol', '{', 100], ['keyword', 'do', 102], ['id', 'Output', 102], ['symbol', '.', 102], ['id', 'printInt', 102], ['symbol', '(', 102], ['id', 'numerator', 102], ['symbol', ')', 102], ['symbol', ';', 102], ['keyword', 'do', 104], ['id', 'Output', 104], ['symbol', '.', 104], ['id', 'printString', 104], ['symbol', '(', 104], ['string_literal', '/', 104], ['symbol', ')', 104], ['symbol', ';', 104], ['keyword', 'do', 106], ['id', 'Output', 106], ['symbol', '.', 106], ['id', 'printInt', 106], ['symbol', '(', 106], ['id', 'denominator', 106], ['symbol', ')', 106], ['symbol', ';', 106], ['keyword', 'return', 108], ['symbol', ';', 108], ['symbol', '}', 110], ['keyword', 'function', 116], ['keyword', 'int', 116], ['id', 'gcd', 116], ['symbol', '(', 116], ['keyword', 'int', 116], ['id', 'a', 116], ['symbol', ',', 116], ['keyword', 'int', 116], ['id', 'b', 116], ['symbol', ')', 116], ['symbol', '{', 116], ['keyword', 'var', 118], ['keyword', 'int', 118], ['id', 'r', 118], ['symbol', ';', 118], ['keyword', 'while', 120], ['symbol', '(', 120], ['operator', '~', 120], ['symbol', '(', 120], ['id', 'b', 120], ['symbol', '=', 120], ['number', '0', 120], ['symbol', ')', 120], ['symbol', ')', 120], ['symbol', '{', 120], ['keyword', 'let', 122], ['id', 'r', 122], ['symbol', '=', 122], ['id', 'a', 122], ['operator', '-', 122], ['symbol', '(', 122], ['id', 'b', 122], ['operator', '*', 122], ['symbol', '(', 122], ['id', 'a', 122], ['operator', '/', 122], ['id', 'b', 122], ['symbol', ')', 122], ['symbol', ')', 122], ['symbol', ';', 122], ['keyword', 'let', 124], ['id', 'a', 124], ['symbol', '=', 124], ['id', 'b', 124], ['symbol', ';', 124], ['keyword', 'let', 124], ['id', 'b', 124], ['symbol', '=', 124], ['id', 'r', 124], ['symbol', ';', 124], ['symbol', '}', 126], ['keyword', 'return', 128], ['id', 'a', 128], ['symbol', ';', 128], ['symbol', '}', 130], ['symbol', '}', 132] ]

# for item in tokens:
#     main(item)

banProg()