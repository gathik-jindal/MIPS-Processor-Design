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


class Status(Enum):
    EXIT = 0
    CONTINUE = 1
    MAGIC1 = 2
    MUL = 3
    DIV = 4
    MAGIC2 = 5
    MAGIC3 = 6


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
    ADDI = "0010"
    ADDIU = "0010"
    BEQ = "1100"
    BNE = "1100"
    LUI = "0011"
    LW = "0010"
    ORI = "0111"
    SLTI = "0100"
    SW = "0010"
    R_FORMAT = "0000"
    MUL = "0101"
    J = "0001"
    JAL = "0001"
    DEF = "0001"


class Operation(Enum):
    NOP = "00000"
    ADD = "00001"
    SLL = "00010"
    SRA = "00011"
    SUB = "00100"
    COMP = "00101"
    UNSIGNED_COMP = "10101"
    OR = "00110"
    XOR = "00111"
    DIV = "01000"
    MUL = "01001"
    RET = "01010"
    MAG1 = "01111"
    MAG2 = "10001"
    MAG3 = "10010"
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
