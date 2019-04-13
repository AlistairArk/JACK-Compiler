import lexer, Parser, semanticAnalyser


import sys, getopt

def loadFile(filename):
    lexer.file = open(filename, "r").read()+" " # Loads the test file
    lexer.fileLen = len(lexer.file)
    lexer.pos = -1
    lexer.lineNum = 0

def main(args):
    print(args)


    loadFile(args[0])
    Parser.parseFile()

    loadFile(args[0])
    semanticAnalyser.analyseSemantic()

main(["source.jack"])
# if __name__ == "__main__":
#     main(sys.argv[1:])