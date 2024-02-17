import sys
from math import log2, ceil
from enum import Enum

class Opcode(Enum):
    ADDI = "001000"
    ADDIU = "001001"
    BEQ = "000100"
    BNE = "000101"
    LUI = "001111"
    LW = "100011"
    ORI = "001101"
    SLTI = "001010"
    SW = "101011"
    R_FORMAT = "000000"
    J = "000010"
    JAL = "000011"
    JR = "000000"
    DIV = "000000"
    MFLO = "000000"
    MFHI = "000000"
    BREAK = "000000"
    MUL = "011100"

class Funct(Enum):
    SLL = "000000"
    SRA = "000011"
    XOR = "100110"
    SUBU = "100011"
    ADDU = "100001"
    ADD = "100000"
    SUB = "100010"
    SLT = "101010"
    SLTU = "101011"
    JR = "001000"
    BREAK = "001101"
    SYSCALL = "001100"
    MFHI = "010000"
    MFLO = "010010"
    
def typeCheck(typeMap: dict):
    '''
    'typeMap' must be a dictionary with key-value pairs as data and its type.
    The function returns true if all the keys match their dataTypes. It prints
    an error and exits otherwise.
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
    This function is for printing an error message and exiting.
    The message must be a string.
    '''
    if(not isinstance(message, str)):
        print(f"{message} is not of type {type('')}")
        sys.exit(1)
    print(message)
    print("Program terminated.")
    sys.exit(1)

if __name__=='__main__':
    dic = {1: int, 2: int, 3: int}
    print(typeCheck(dic))
    print(typeCheck.__doc__)
    printErrorandExit(45)
