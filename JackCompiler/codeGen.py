
output = ""

def text(dialogue):
    global output
    output += dialogue + "\n"
    # print("        >",dialogue)


'''
Use Example:
    Error(token, "Error info")
'''
def Error(*args):
    print("Error in line " + str(args[0][2]) + " at or near '" + str(args[0][1])+ "', " + str(args[1]));
    exit()
