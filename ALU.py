from Utilities import *
from ALU_Control import *


class ALU():

    """
      It is the ALU of a processor and can perform functions like addition, subtraction, etc.
    """

    def __init__(self, control=None, inpPortCount=3, outPortCount=2):
        """
          This is a constructor that creates an ALU for a processor. The created ALU variable number of input and output ports.
        """

        if (control == None):
            control = self._ground

        typeCheck({control: Callable, inpPortCount: int, outPortCount: int})

        self.__control = control
        self.__iPC = inpPortCount
        self.__oPC = outPortCount

        # Index 0: RD1; Index 1: ALUSrcMux; Index 2: shamt
        self.__inpPorts = [self._ground for i in range(self.__iPC)]
        # Index 0: Zero Flag; Index 1: ALUresult
        self.__outPorts = [self._ground() for i in range(self.__oPC)]

        self.__operation = {
            Operation.NOP:           self.__nop,
            Operation.ADD:           self.__add,
            Operation.SLL:           self.__sll,
            Operation.SRA:           self.__sra,
            Operation.SUB:           self.__sub,
            Operation.LUI:           self.__lui,
            Operation.COMP:           self.__comp,
            Operation.UNSIGNED_COMP:  self.__unsigned_comp,
            Operation.OR:           self.__or,
            Operation.XOR:           self.__xor,
            Operation.DIV:           self.__div,
            Operation.MUL:           self.__mul,
            Operation.RET:           self.__ret,
            Operation.MAG1:           self.__mag1,
            Operation.MAG2:           self.__mag2,
            Operation.MAG3:           self.__mag3
        }

    def _ground(self):
        """
            Used for grounding control signals
        """

        return 0

    def run(self):
        """
            This method executes the operation based on the current control value.
        """
        return self.__operation[self.__control()]()

    def __nop(self):
        """
            This method executes a NOP(does nothing).
        """
        return Status.CONTINUE

    def __add(self):
        """
            Method for add operation.
        """
        self.__outPorts[1] = self.__inpPorts[0](0)()+self.__inpPorts[1]()(1)()
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __sll(self):
        """
            Method for shift left logical operation.
        """
        self.__outPorts[1] = self.__inpPorts[1]()(1)() << self.__inpPorts[2]()
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __sra(self):
        """
            Method for shift right arithmetic operation.
        """
        self.__outPorts[1] = self.__inpPorts[0](0)() >> self.__inpPorts[2]()
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __sub(self):
        """
            Method for sub operation.
        """
        self.__outPorts[1] = self.__inpPorts[0](0)()-self.__inpPorts[1]()(1)()
        self.__outPorts[0] = int(not(self.__outPorts[1]))
        return Status.CONTINUE

    def __comp(self):
        """
            Method for algebraic comparison of inputs.
        """
        self.__outPorts[1] = int(self.__inpPorts[0](0)() < self.__inpPorts[1]()(1)())
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE
    
    def __unsigned_comp(self):
        """
            Method for algebraic comparison of inputs.
        """
        self.__outPorts[1] = int(abs(self.__inpPorts[0](0)()) < abs(self.__inpPorts[1]()(1)()))
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __or(self):
        """
            Method for bitwise or operation.
        """
        print(self.__inpPorts[0](0)(),self.__inpPorts[1]()(1)())
        self.__outPorts[1] = self.__inpPorts[0](0)() ^ self.__inpPorts[1]()(1)()
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __xor(self):
        """
            Method for bitwise xor operation.
        """
        self.__outPorts[1] = self.__inpPorts[0](0)() ^ self.__inpPorts[1]()(1)()
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __div(self):
        """

        """

        return Status.DIV

    def __mul(self):
        """
        """

        return Status.MUL

    def __ret(self):
        """
            Terminates the program.
        """
        print("Break instruction encountered.\nProgram Terminated.")
        return Status.EXIT

    def __lui(self):
        '''
            Special operation to right shift immediate value by 16
        '''
        self.__outPorts[1] = self.__inpPorts[1]()(1)() << 16
        self.__outPorts[0] = ((self.__outPorts[1] and 1)+1) % 2
        return Status.CONTINUE

    def __mag1(self):
        """
            This method handles all the syscall instructions.
        """
        return Status.MAGIC1

    def __mag2(self):
        """
            This method handles all the mfhi instructions.
        """
        return Status.MAGIC2

    def __mag3(self):
        """
            This method handles all the mflo instructions.
        """
        return Status.MAGIC3

    def setInputConnection(self, portID: int, portConnection: Callable):
        typeCheck({portID: int, portConnection: Callable})
        if (portID >= self.__iPC):
            printErrorandExit(f"Invalid portID for an ALU with {self.__iPC} input ports.")
        self.__inpPorts[portID] = portConnection

    def getOutput(self, portID=1):
        '''
            This method can be used to get output from anyone of the output ports of the ALU.
            It is set to return output of port 1 by default.
        '''
        typeCheck({portID: int})
        if (portID >= self.__oPC):
            printErrorandExit(f"Invalid portID for an ALU with {self.__oPC} output ports.")
        return self.__outPorts[portID]

    def getZeroFlag(self):
        '''
            Method to get the zero flag from ALU. 
        '''
        return self.__outPorts[0]
