import lexer, Parser, semanticAnalyser, symbolTable, codeGen, parserKeywords


import sys, os, getopt

def loadFile(filename):

    ''' load the file '''
    lexer.file = open(filename, "r").read()+" " # Loads the test file
    lexer.fileLen = len(lexer.file)
    # print(filename)
    # print(lexer.file)
    # exit()


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

    #                 {  (  [
    symbolTable.bracketPointer = [1, 1, 1]
    #                 if, else, while
    symbolTable.labelCounter   = [ 0,    0,    0]       # Increment counter as new labels are created
    symbolTable.labelStack = []                         # Close loops as they are created


    codeGen.output = ""

    parserKeywords.objectType = ""


def main(args):
    print(args)



    for file in os.listdir(args[0]):
        if file.endswith(".jack"):
            # print(os.path.join(args[0], file), file)

            print("\n",args[0]+"\\"+os.path.splitext(file)[0]+".vm")
            
            print(args[0])
            loadFile(os.path.join(args[0], file))
            Parser.parseFile()

            # File Creation
            f = open(args[0]+"\\"+os.path.splitext(file)[0]+".vm", "w")
            f.write(codeGen.output)
            f.close()







    # loadFile(args[0])
    # semanticAnalyser.analyseSemantic()

    # loadFile(args[0])
    '''
    compile code and generate file
    '''

main(["test//List!!!"]) # Compiler test




# # # Code to run the program from command line 
# # if __name__ == "__main__":
# #     main(sys.argv[1:])



# # Code to auto-compile all sets for testing
# for file in os.listdir("test"):
#     # print()
#     main(["test\\"+file]) # Compiler test