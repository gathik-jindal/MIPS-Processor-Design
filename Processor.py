from ALU import *
from ALU_Control import *
from Control import *
from Memory import *
from Multiplexer import *
from RegSet import *
from Register import *
from Utilities import *
from Splitter import *


class Processor():
    
    """
        A processor that understands the MIPS ISA.
    """

    def __init__(self):

        """
            Creates a processor.
        """

        #Creating the objects and setting up the data path
        
        self.PC = Register(32, 0x400000)
        self.Controller = Control()

        self.InstructionMemory = InstructionMemory(input("Enter instruction file name (Has to be in memory folder): "))
        self.DataMemory = DataMemory(input("Enter instruction file name (Has to be in memory folder): "))

        self.splitter = Splitter(InstructionMemory.loadWord())
        
        self.ALUController = ALUControl(self.Controller.getALUOp, self.Controller.setpcSelect)
        self.ALU = ALU()
        #### more ALU connections
        
        self.RegisterFile = RegSet(readPortCount = 2, writePortCount = 1, count = 32, size = 32, defaultVal = 0)
        self.RegisterFile.writeEnable(self.Controller.getRegWrite)
        self.RegisterFile.readEnable(self.Controller.getRegRead)

        self.RegDstMux = Multiplexer(3, self.Controller.getRegDst)
        self.ALUSrcMux = Multiplexer(2, self.Controller.getALUSrc)
        self.WriteBackMux = Multiplexer(3, self.Controller.getWB)
        self.BranchSelectMux = Multiplexer(2, self.Controller.getBranchSelect)
        self.PCSelectMux = Multiplexer(4, self.Controller.getpcSelect)

        #Creating Data path

    
    def RunMCU(self):
        '''
            Runs the Main Control Unit.
        '''
        self.Controller.run(opcode = self.splitter.getOpcode())

    def connectRegFile(self):
        '''
            Method for connecting all the ports of the Register file.
        '''
        self.RegisterFile.connectReadPort(0, self.splitter.getRS)
        self.RegisterFile.connectReadPort(1, self.splitter.getRT)
        
        self.RegisterFile.connectWritePort(0, self.RegDstMux.getData)

    def getACUop(self):
        '''
            Method for retrieving the operation code from ALU Control Unit.
        '''
        return self.ALUController.getOperation(funct= self.splitter.getFunct())

    def connectALU(self):
        '''
            Method for connecting all the input ports to the ALU.
        '''

        self.ALU.setInputConnection(0, self.RegisterFile.read(0))
        self.ALU.setInputConnection(1, self.ALUSrcMux.getData)
        self.ALU.setInputConnection(2, self.splitter.getShamt)

    def ReadData(self):
        '''
            Method for retrieving data from Data Memory.
        '''

        return DataMemory.loadWord(self.ALU.getOutput())
    
    def WriteData(self):
        '''
            Method for writing to the Memory.
        '''
        DataMemory.storeWord(self.RegisterFile.read(1)())

    def connectRegDstMux(self):
        '''
            Method for connecting the input ports of RegDstMux.
        '''
        self.RegDstMux.connectData(0, self.splitter.getRT)
        self.RegDstMux.connectData(1, self.splitter.getRD)
        self.RegDstMux.connectData(2, lambda: 31)               

    def connectALUSrcMux(self):
        '''
            Method for connecting the input ports of ALUSrcMux.
        '''
        self.ALUSrcMux.connectData(0, self.RegisterFile.read(1))
        self.ALUSrcMux.connectData(1, self.__signExtend)

    def connectWriteBackMux(self):
        '''
            Method for connecting the input ports of WriteBackMux.
        '''

        self.WriteBackMux.connectData(0, self.ALU.getOutput)
        self.WriteBackMux.connectData(1, self.ReadData)
        self.WriteBackMux.connectData(2, lambda: PC+4)     #For now, we need to rewrite after we make the PC adder...

    def connectBranchSelectMux(self):
        '''
            Method for connecting the input ports of BranchSelectMux.
        '''

        self.BranchSelectMux.connectData(0, lambda: self.ALU.getOutput(0))                      #Need to find a better implementation...
        self.BranchSelectMux.connectData(1, lambda: int(not(self.ALU.getOutput(0))))
    
    def connectPCSelectMux(self):
        '''
            Method for connecting the input ports of BranchSelectMux.
        '''
        pass

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

