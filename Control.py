from Utilities import *
from RegSet import *
from Register import *

class Control():

    """
        Gives control signals to other components.
    """

    def __init__(self):

        self.__decode = {
            
           Opcode.ADDI.value      : [ALUOp.ADDI.value for i in range(11)],    # Change these control signals
           Opcode.ADDIU.value     : [ALUOp.ADDIU.value for i in range(11)],
           Opcode.BEQ.value       : [ALUOp.BEQ.value for i in range(11)],
           Opcode.BNE.value       : [ALUOp.BNE.value for i in range(11)],
           Opcode.LUI.value       : [ALUOp.LUI.value for i in range(11)],
           Opcode.LW.value        : [ALUOp.LW.value for i in range(11)],
           Opcode.ORI.value       : [ALUOp.ORI.value for i in range(11)],
           Opcode.SLTI.value      : [ALUOp.SLTI.value for i in range(11)],
           Opcode.SW.value        : [ALUOp.SW.value for i in range(11)],
           Opcode.R_FORMAT.value  : [ALUOp.R_FORMAT.value for i in range(11)],
           Opcode.J.value         : [ALUOp.J.value for i in range(11)],
           Opcode.JAL.value       : [ALUOp.JAL.value for i in range(11)],
           Opcode.MUL.value       : [ALUOp.MUL.value for i in range(11)]

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
