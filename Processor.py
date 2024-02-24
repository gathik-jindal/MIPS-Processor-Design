from ALU import *
from ALU_Control import *
from Control import *
from Memory import *
from Multiplexer import *
from RegSet import *
from Register import *
from Utilities import *


class Processor():
    
    """
        A processor that understands the MIPS ISA.
    """

    def __init__(self):

        """
            Creates a processor.
        """

        #Creating the objects and setting up the data path
        
        PC = Register(32, 0x400000)
        Controller = Control()

        InstructionMemory = InstructionMemory(input("Enter instruction file name (Has to be in memory folder): "))
        DataMemory = DataMemory(input("Enter instruction file name (Has to be in memory folder): "))
        
        
        ALUController = ALUControl(Controller.getALUOp, Controller.setpcSelect)
        ALU = ALU()
        #### more ALU connections
        
        RegisterFile = RegSet(readPortCount = 2, writePortCount = 1, count = 32, size = 32, defaultVal = 0)
        RegisterFile.writeEnable(Controller.getRegWrite)
        RegisterFile.readEnable(Controller.getRegRead)

        RegDstMux = Multiplexer(3, Controller.getRegDst)
        ALUSrcMux = Multiplexer(3, Controller.getALUSrc)
        WriteBackMux = Multiplexer(3, Controller.getWB)
        BranchSelect = Multiplexer(2, Controller.getBranchSelect)
        PCSelect = Multiplexer(4, Controller.getpcSelect)

        #Creating Data path


    def __signExtend():
        pass

    def __branchGate():
        pass

    def __shiftLeft():
        pass

    def __adder():
        pass


    def run(mode = 0, untill = None):

        pass

