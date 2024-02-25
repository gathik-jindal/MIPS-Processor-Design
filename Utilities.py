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
    DIV = "011010"
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
    MUL = "101"
    J = "001"
    JAL = "001"
    DEF = "001"


class Operation(Enum):
    NOP = "00000"
    ADD = "00001"
    SLL = "00010"
    SRA = "00011"
    SUB = "00100"
    COMP = "00101"
    OR = "00110"
    XOR = "00111"
    DIV = "01000"
    MUL = "01001"
    RET = "01010"
    MAG = "01111"
    LUI = "10000"


def typeCheck(typeMap: dict) -> bool:
    '''
    'typeMap' must be a dictionary with key-value pairs as data and its type.
    The function returns true if all the keys match their dataTypes. It prints
    an error and exits otherwise.
    '''
    if (not isinstance(typeMap, dict)):
        printErrorandExit(f"{typeMap} is not of type {type({})}")

    else:
        for key in typeMap:
            if (key == None or not isinstance(key, typeMap[key])):
                printErrorandExit(f"{key} is not of type {typeMap[key]}")
        return True


def printErrorandExit(message: str) -> None:
    '''
    This function is for printing an error message and exiting.
    The message must be a string.
    '''
    if (not isinstance(message, str)):
        print(f"{message} is not of type {type('')}")
        sys.exit(1)
    print(message)
    print("Program terminated.")
    sys.exit(1)


if __name__ == '__main__':
    dic = {1: int, 2: int, 3: int, 4: Callable}
    print(typeCheck(dic))
    print(typeCheck.__doc__)
    printErrorandExit(45)
