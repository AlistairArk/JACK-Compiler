
import lexer

#             type, symbol, declared flag, true

symbolTable = [[], [], [], []]



def addSymbol(*args,**kwargs):
    pass

def main(token):
    
    print(token)
    '''
    Correct usage of variables
    - A variable has been declared before being used
        // As a variable is declared add it to a list of known variables

    - A variable has been initialized before being used in an expression
        // each time a variable is initialized, raise flag to indicated it has been initialized

    - Scope resolution (as in nested scopes or local variables)


    Type checking
    - The RHS of an assignment statement is type compatible with the LHS

    - Coercion, ie. converting one type to another, for example in assignment parameter passing
    
    - Expressions used in array indices's have an integer value


    Function Calling
    - A function cannot be called if it has not been declared
        // Store a list of functions each time one is declared

    - The called function has the same number and type of parameters as its declaration
        // store parameters paired with the functions declaration

    - The function returns a value compatible with the type of the function
        // check current function type before returning values


    Function Calling
    - All paths return a value
        // Detect function closing, ensure a return takes place somewhere before the end of the function or at the end o a function.
        // some tricks form "unreachable code" may be required

    Other
    - Unreachable Code (eg. following a non-conditional return in the body of the function)

    '''