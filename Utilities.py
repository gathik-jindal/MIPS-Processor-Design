import sys
from math import log2, ceil
from enum import Enum
from typing import Callable

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
    DEF = "111111"

class ALUOp(Enum):
    ADDI = "010"
    ADDIU = "010"
    BEQ = "100"
    BNE = "100"
    LUI = "011"
    LW = "010"
    ORI = "111"
    SLTI = "100"
    SW = "010"
    R_FORMAT = "000"
    DIV = "110"
    MUL = "101"
    J = "001"
    JAL = "001"
    DEF = "001"


class Operation(Enum):
    NOP = "0000"
    ADD = "0001"
    SLL = "0010"
    SRA = "0011"
    SUB = "0100"
    COMP = "0101"
    OR = "0110"
    XOR = "0111"
    DIV = "1000"
    MUL = "1001"
    RET = "1010"
    MAG = "1111"

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

def convertToInt(word:str, base=16):
    '''
    This function converts the word to base 10.
    '''

    if not typeCheck({word: str, base: int}):
        printErrorandExit(f"Data provided is not of type {word} -> str or {base} -> int")
    
    value = 0
    pow = 1
    word = word[::-1]

    for x in word:
        x = x.lower()
        if x in "abcdefghijklmnopqrstuvwxyz" and base > 9:
            x = ord(x) - ord("a") + 10
        elif x in "abcdefghijklmnopqrstuvwxyz" and base <= 9:
            printErrorandExit(f"{word} has letters but base ({base} <= 9)")
        else:
            x = pow*(int(x))

        value += x
        pow *= base
    
    return value


if __name__=='__main__':
    print(convertToInt("1A"))
    dic = {1: int, 2: int, 3: int, 4: Callable}
    print(typeCheck(dic))
    print(typeCheck.__doc__)
    printErrorandExit(45)