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
    print(args)
    print("Error in line " + str(args[0][2]) + " at or near '" + str(args[0][1])+ "', " + str(args[1]));
    exit()


def eof(token):
    ''' Quick EOF check'''

    if token[0] == "EOF":
        print("unexpected EOF")
