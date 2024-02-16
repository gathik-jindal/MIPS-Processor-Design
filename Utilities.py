import sys

def typeCheck(typeMap: dict):
    '''
    'typeMap' must be a dictionary with key-value pairs as data and its type.
    The function returns true if all the keys match their dataTypes. It prints
    an error message and exits otherwise.
    '''
    if(not isinstance(typeMap, dict)):
        printErrorandExit(f"{typeMap} is not of type {type({})}")

    else:
        for key in typeMap:
            if(key == None or not isinstance(key, typeMap[key])):
                printErrorandExit(f"{key} is not of type {typeMap[key]}")
        return True

def printErrorandExit(message:str):
    '''
    This function is for printing an error message and exit.
    The message must be a string.
    '''
    if(not isinstance(message, str)):
        print(f"{message} is not of type {type('')}")
        sys.exit(1)
    print(message)
    sys.exit(1)

if __name__=='__main__':
    dic = {1: int, 2: int, 3: int}
    print(typeCheck(dic))
    print(typeCheck.__doc__)
    printErrorandExit(45)
