'''




'''
import lexer, Parser, symbolTable, codeGen, parserKeywords
import sys, os, getopt

def loadFile(filename):
    ''' load the file '''
    lexer.file = open(filename, "r").read()+" " # Loads the test file
    lexer.fileLen = len(lexer.file)


    ''' Reset Global Vars '''
    lexer.pos = -1
    lexer.lineNum = 1
    lexer.peekFlag = 0
    lexer.posTemp = 0
    lexer.lineNumTemp=0

    #             type, symbol, index, scope, attribute (data type)
    symbolTable.symbolTable = [[],    [],    [],    [],     []]
    symbolTable.symbolIndexList = [[],[]]
    symbolTable.staticVarCount = 0
    symbolTable.methodList = []
    symbolTable.className = ""
    symbolTable.objectName = ""
    symbolTable.arrayLetSwitch

    #                 {  (  [
    symbolTable.bracketPointer = [1, 1, 1]
    #                 if, else, while
    symbolTable.labelCounter   = [ 0,    0,    0]       # Increment counter as new labels are created
    symbolTable.labelStack = []                         # Close loops as they are created

    codeGen.output = ""
    parserKeywords.objectType = ""
    parserKeywords.returnList = []

def main(args):

    if not len(args):
        print("Error: No arguments supplied to compiler")
        
    elif not os.path.isdir(args[0]) and not os.path.isfile(args[0]): # If file not found
        print("Error: The system cannot find the path specified: '"+args[0]+"'")

    else:
        if os.path.isdir(args[0]):
            print("Compiling files in '"+args[0]+"'")
            for file in os.listdir(args[0]):
                if file.endswith(".jack"):
                    print("     Now compiling '"+file+"'")

                    # Compile file
                    loadFile(os.path.join(args[0], file))
                    Parser.parseFile()

                    # File Creation
                    f = open(args[0]+"//"+os.path.splitext(file)[0]+".vm", "w")
                    f.write(codeGen.output)
                    f.close()

        elif os.path.isfile(args[0]):
            print("Compiling '"+args[0]+"'")

            # Compile file
            loadFile(args[0])
            Parser.parseFile()

            # File Creation
            f = open(os.path.splitext(args[0])[0]+".vm", "w")
            f.write(codeGen.output)
            f.close()


# Code to run the program from command line
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print("Compiler Error: File failed to compile")


# main(["JackPrograms//ArrayTest//Main.jack"]) # Compiler test

# # Code to auto-compile all sets for testing
# for file in os.listdir("JackPrograms"):
#     main(["JackPrograms//"+file]) # Compiler test
