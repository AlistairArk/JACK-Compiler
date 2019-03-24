''' 
Assignment: Milestone 1. Lexical Analysis

So far, I have created a lexer which successfully removes white space and comments from the input file 
and correctly extracts all the tokens of the source code. It does not crash or become unstable if the 
source file contains any kind of lexical errors. 

The lexer has been tested using the provided JACK source files and is shown to function 
properly without any issues. 
'''



# # file = list(shlex.shlex(open("source.jack", "r").read())) # Loads the test file
file = open("source.jack", "r").read()+" " # Loads the test file
fileLen = len(file)
pos = -1
lineNum = 0


tokenType = ["keyword","operator","symbol"] # ,"integer_number","identifier","punctuator"]

keywords = ["class", "constructor", "method", "function",  # Program Components
            "int", "boolean", "char", "void",              # Primitive Types
            "var", "static", "field",                      # Variable Declarations
            "let", "do", "if", "else", "while", "return",  # Statements
            "true", "false", "null",                       # Constant Values
            "this"                                         # Objective Reference 
            ]

symbols =  ["(",")",   # Used for grouping arethmetic expressions and enclosing parameter-lists and argument-lists
            "[","]",   # Used for array indexing
            "{","}",   # Used for grouping program units and statements
            ",",       # Variable list seperatior
            ";",       # Statement terminator
            "=",       # Assignment and comparison operator
            "."        # Class membership
            ]

# JACK - Standard Library
stdlib = ["Math","String","Array","Output","Screen","Memory","Keyboard","Sys"]

operators = ["+","-","*","/","&","|","~","<",">"]

tokens = [
        keywords,       # Keywords
        operators,      # Operators
        symbols         # Symbol
        ]


def getNextToken():
    global pos, peekFlag, posTemp
    if peekFlag:
        pos = posTemp               # Revert Pointer state 
        peekFlag = 0

    token = consumeToken()
    # semanticAnalyser.main(token) # Peform semantic analysis while consuming tokens
    # print(token)
    return token


def consumeToken():
    ''' Token GetNextToken(). Whenever this function is called it will return the next available token from the input stream, and the token is removed from the input (i.e. consumed).'''
    global pos,lineNum


    # Skip any white space characters until you hit the first non-whitespace character (call it C).
    while file[pos]==" ":
        pos+=1 # Incriment pointer
        if pos >= fileLen:
            # If the integer code for C = -1, then it is the end of file symbol, hence return an EOF token. 
            C = -1
            return ["EOF"]
    C = file[pos]


    # If C is the start symbol of a comment then skip all the characters in the body of the comment
    if C == "/" and file[pos+1]=="/": # comment out //
        string = ""
        while file[pos]!="\n":
            string+=file[pos]
            pos+=1
            if file[pos] == "\n":
                lineNum+=1
        pos+=1 # Jump 1 to remove newline (\n)
        return consumeToken() # go back to 1.
    
    if C == "/" and file[pos+1]=="*":# comment out /**
        pos+=1
        while file[pos]!="*" or file[pos+1]!="/":
            pos+=1
        pos+=1 # Jump 1 to remove end character (*/)
        return consumeToken() # go back to 1. 


    # If C is a quote ("), it may be the start of a literal string, then:
    #       - Keep reading more characters, putting them into a string, until you hit the closing quote.
    #       - Put the resulting string (lexeme) in a lexeme, of type string_literal, and return the token.
    if C == '"':
        lexeme = ""
        pos+=1
        while file[pos]!='"':
            lexeme+=file[pos]
            pos+=1
        pos+=1 # Jump 1 to remove " character
        return ["string_literal",lexeme,lineNum]


    # If C is a letter, it may be the first letter in a keyword or identifier, then: 
    #       - Keep reading more letters and/or digits, putting them into a string, until you hit a character that is neither a letter nor a digit
    #       - Try to find the resulting string in a list of keywords. If the string is found then the token is a keyword, otherwise it is an identifier. 
    #       - Put the string (lexeme) in a token with the proper token type (keyword or id) and return the token.
    if C.isalpha():
        lexeme = ""
        while file[pos].isalpha():
            lexeme+=file[pos]
            pos+=1

        if lexeme in tokens[tokenType.index("keyword")]:
            return ["keyword",lexeme,lineNum]
        else:
            return ["id",lexeme,lineNum]


    # If C is a digit, it may be the first digit in a number, then:
    #       - Keep reading more digits, putting them into a string, until you hit a character that is not a digit. 
    #       - put the resulting string in a token, of type number, and return the token.
    if C.isdigit():
        lexeme = ""
        while file[pos].isdigit():
            lexeme+=file[pos]
            pos+=1
        return ["number",lexeme,lineNum] 

    
    # C must be a symbol (since it is not a letter nor digit), tokenize it and return the token
    pos+=1
    for i in range(len(tokenType)):

        if C in tokens[i]:
            return [tokenType[i],C,lineNum] 

    if C == "\n":
        lineNum+=1 # incriment line counter
        return consumeToken() # Get next token
    else:
        return ["symbol",C,lineNum]
        
    

peekFlag = 0
posTemp = 0
def peekNextToken():
    '''When this function is called it will return the next available token in the input stream, but the token is not consumed (i.e. it will stay in the input). So, the next time the parser calls GetNextToken, or PeekNextToken, it gets this same token.'''
    global pos, peekFlag, posTemp

    if not peekFlag:
        peekFlag = 1
        posTemp = pos               # Save Current State of Pointer   

    nextToken = consumeToken()  # Get Next Token
    return nextToken            # Return Token



def main():
    ''' Lexer Test function '''
    
    token = getNextToken()
    while (token[0] != "EOF"):

        print("".join(str(word).ljust(20) for word in token)) # print token
        token = getNextToken()

# main()