from Utilities import *
from RegSet import *
from Register import *

class Control():

    """
        Gives control signals to other components.
    """

    def __init__(self):

        self.__decode = {
            # RegDst, Branch, MemRead, MemWrite, WB, ALUOP, ALUSRC, RegWrite, RegRead, BranchSelect, pcSelect
           Opcode.ADDI.value      : [0, 0, 0, 0, 0, ALUOp.ADDI, 1, 1, 1, 0, 0],    # Change these control signals
           Opcode.ADDIU.value     : [0, 0, 0, 0, 0, ALUOp.ADDIU, 1, 1, 1, 0, 0],
           Opcode.BEQ.value       : [0, 1, 0, 0, 0, ALUOp.BEQ, 0, 0, 1, 0, 1],
           Opcode.BNE.value       : [0, 1, 0, 0, 0, ALUOp.BNE, 0, 0, 1, 1, 1],
           Opcode.LUI.value       : [0, 0, 0, 0, 0, ALUOp.LUI, 1, 1, 0, 0, 0],
           Opcode.LW.value        : [0, 0, 1, 0, 1, ALUOp.LW, 1, 1, 1, 0, 0],
           Opcode.ORI.value       : [0, 0, 0, 0, 0, ALUOp.ORI, 1, 1, 1, 0, 0],
           Opcode.SLTI.value      : [0, 0, 0, 0, 0, ALUOp.SLTI, 1, 1, 1, 0, 0],
           Opcode.SW.value        : [0, 0, 0, 1, 0, ALUOp.ADDI, 1, 0, 1, 0, 0],
           Opcode.R_FORMAT.value  : [1, 0, 0, 0, 0, ALUOp.R_FORMAT, 0, 1, 1, 0, 0],
           Opcode.J.value         : [0, 0, 0, 0, 0, ALUOp.J, 0, 0, 0, 0, 2],
           Opcode.JAL.value       : [3, 0, 0, 0, 2, ALUOp.JAL, 0, 1, 0, 0, 2],
           Opcode.MUL.value       : [1, 0, 0, 0, 0, ALUOp.MUL, 0, 1, 1, 0, 0 ]

           }

        self.__state = [0,0,0,0,0,0,0,0,0,0,0]
        

    def run(self, opcode):

        """
            Runs the processor commands and generates the correct control signals.
        """
           
        self.__state = self.__decode[opcode]
        self.dump(opcode)
        

    def getRegDest(self):

        """
            Provides the control line for RegDest Mux.
        """

        return self.__state[0]

    def getBranch(self):

        """
            Provides the control line for Branch Signal.
        """

        return self.__state[1]

    def getMemRead(self):

        """
            Provides the control line for MemRead Signal.
        """

        return self.__state[2]

    def getMemWrite(self):

        """
            Provides the control line for MemWrite Signal.
        """

        return self.__state[3]

    def getWB(self):

        """
            Provides the control line for WB Mux.
        """

        return self.__state[4]

    def getALUOp(self):

        """
            Provides the control line for the ALUOp Signal.
        """

        return self.__state[5]

    def getALUSrc(self):

        """
            Provides the control line for ALUSrc Mux.
        """

        return self.__state[6]

    def getRegWrite(self):

        """
            Provides the control line for RegWrite Signal.
        """

        return self.__state[7]

    def getRegRead(self):

        """
            Provides the control line for RegRead Signal.
        """

        return self.__state[8]

    def getBranchSelect(self):

        """
            Provides the control line for BranchSelect Mux.
        """

        return self.__state[9]

    def getpcSelect(self):

        """
            Provides the control line for RegDest Mux.
        """

        return self.__state[10]

    def setpcSelect(self, val:int ):

        """
            Sets the pcSelect control line.
        """
        typeCheck({val : int})
        self.__state[10] = val
        self.__state[7] = 0

    def dump(self, opcode):

        """
            Prints the current control signals.
        """
        
        print(f"The control signals generated for Instruction '{Opcode(opcode).name} ({opcode})' are:\n\
            RegDest Mux: {self.__state[0]}\n\
            Branch Signal: {self.__state[1]}\n\
            MemRead Signal: {self.__state[2]}\n\
            MemWrite Signal: {self.__state[3]}\n\
            WB Mux: {self.__state[4]}\n\
            ALUOp Signal: {self.__state[5]}\n\
            ALUSrc Mux: {self.__state[6]}\n\
            RegWrite Signal: {self.__state[7]}\n\
            RegRead Signal: {self.__state[8]}\n\
            BranchSelect Mux: {self.__state[9]}\n\
            pcSelect Mux: {self.__state[10]}\n")



if __name__ == "__main__":

    C = Control()
    
    while True:
        C.run(input("Enter the opcode: "))
        print(C.getRegDest())
        print(C.getBranch())
        print(C.getMemRead())
        print(C.getMemWrite())
        print(C.getWB())
        print(C.getALUOp())
        print(C.getALUSrc())
        print(C.getRegWrite())
        print(C.getRegRead())
        print(C.getBranchSelect())
        print(C.getpcSelect())
