import lexer, Parser, semanticAnalyser


import sys, getopt

def loadFile(filename):
    lexer.file = open(filename, "r").read()+" " # Loads the test file
    lexer.fileLen = len(lexer.file)
    lexer.pos = -1
    lexer.lineNum = 0
    lexer.peekFlag = 0
    lexer.posTemp = 0
    lexer.lineNum=1

def main(args):
    print(args)


    loadFile(args[0])
    Parser.parseFile()

    # loadFile(args[0])
    # semanticAnalyser.analyseSemantic()

    # loadFile(args[0])
    '''
    compile code and generate file
    '''

main(["source.jack"]) # Compiler test

# # Code to run the program from command line 
# if __name__ == "__main__":
#     main(sys.argv[1:])