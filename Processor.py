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

        self.__status = Status.CONTINUE
        
        self.PC = Register(32, 0x400000)
        self.Controller = Control()

        self.InstructionMemory = InstructionMemory(input("Enter instruction file name (Has to be in memory folder): "))
        self.DataMemory = DataMemory(self.Controller.getMemRead, self.Controller.getMemWrite, input("Enter instruction file name (Has to be in memory folder): "))

        self.splitter = Splitter(self.__FetchData)
        
        self.ALUController = ALUControl(self.Controller.getALUOp, self.Controller.setpcSelect)
        self.ALU = ALU(control= self.getACUop)
        self.__connectALU()
        #### more ALU connections
        
        self.RegisterFile = RegSet(readPortCount = 2, writePortCount = 1, count = 32, size = 32, defaultVal = 0)
        self.RegisterFile.writeEnable(self.Controller.getRegWrite)
        self.RegisterFile.readEnable(self.Controller.getRegRead)
        self.__connectRegFile()

        self.RegDstMux = Multiplexer(3, self.Controller.getRegDst)
        self.__connectRegDstMux()

        self.ALUSrcMux = Multiplexer(2, self.Controller.getALUSrc)
        self.__connectALUSrcMux()

        self.WriteBackMux = Multiplexer(3, self.Controller.getWB)
        self.__connectWriteBackMux()
        self.BranchSelectMux = Multiplexer(2, self.Controller.getBranchSelect)
        self.__connectBranchSelectMux()
        self.PCSelectMux = Multiplexer(4, self.Controller.getpcSelect)
        self.__connectPCSelectMux()


        #Creating Data path

    
    def __FetchData(self):
        return self.InstructionMemory.loadWord(self.PC.getVal())

    def __connectRegFile(self):
        '''
            Method for connecting all the ports of the Register file.
        '''
        self.RegisterFile.connectReadPort(0, self.splitter.getRS)
        self.RegisterFile.connectReadPort(1, self.splitter.getRT)
        
        self.RegisterFile.connectWritePort(0, self.RegDstMux.getData, self.WriteBackMux.getData)



    def __connectALU(self):
        '''
            Method for connecting all the input ports to the ALU.
        '''

        self.ALU.setInputConnection(0, self.RegisterFile.read(0))
        self.ALU.setInputConnection(1, self.ALUSrcMux.getData)
        self.ALU.setInputConnection(2, self.splitter.getShamt)



    def __connectRegDstMux(self):
        '''
            Method for connecting the input ports of RegDstMux.
        '''

        self.RegDstMux.connectData(0, self.splitter.getRT)
        self.RegDstMux.connectData(1, self.splitter.getRD)
        self.RegDstMux.connectData(2, lambda: 31)

    def __connectALUSrcMux(self):
        '''
            Method for connecting the input ports of ALUSrcMux.
        '''

        self.ALUSrcMux.connectData(0, self.RegisterFile.read(1))
        self.ALUSrcMux.connectData(1, self.splitter.getImm)

    def __connectWriteBackMux(self):
        '''
            Method for connecting the input ports of WriteBackMux.
        '''

        self.WriteBackMux.connectData(0, self.ALU.getOutput)
        self.WriteBackMux.connectData(1, self.ReadData)
        self.WriteBackMux.connectData(2, self.PCadder)

    def __connectBranchSelectMux(self):
        '''
            Method for connecting the input ports of BranchSelectMux.
        '''

        self.BranchSelectMux.connectData(0, self.ALU.getZeroFlag)
        self.BranchSelectMux.connectData(1, self.notZero)
    
    def __connectPCSelectMux(self):
        '''
            Method for connecting the input ports of BranchSelectMux.
        '''
        self.PCSelectMux.connectData(0, self.PCadder)
        self.PCSelectMux.connectData(1, self.BranchAdder)
        self.PCSelectMux.connectData(2, self.JumpshiftLeft2)
        self.PCSelectMux.connectData(3, self.RegisterFile.read(0))

    def RunMCU(self):
        '''
            Runs the Main Control Unit.
        '''
        self.Controller.run(opcode = self.splitter.getOpcode())

    def getACUop(self):
        '''
            Method for retrieving the operation code from ALU Control Unit.
        '''
        return self.ALUController.getOperation(funct= self.splitter.getFunct())
    
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

    def signExtend(self):
        return self.splitter.getImm()
    
    def notZero(self):
        '''
            This method is for the not gate after the Zero flag(for BNE).
        '''
        return int(not(self.ALU.getZeroFlag()))
    
    def branchGate(self):
        '''
            This method is for the AND gate for branch instruction.
        '''
        return self.Controller.getBranch() and self.ALU.getZeroFlag()

    def ImmshiftLeft2(self):
        '''
            This method implements the Left Shifter(by 2) on Immediate value.
        '''
        return self.signExtend()<<2
    
    def JumpshiftLeft2(self):
        '''
            This method implements the Left Shifter(by 2) on Jump Location field.
        '''
        return self.splitter.getJumpLoc()<<2
    
    def PCadder(self):
        '''
            This method implements the PC adder(by 4) for incrementing PC.
        '''
        self.new_PC = self.PC.getVal() + 4
        return self.new_PC

    def BranchAdder(self):
        '''
            This method implements the branch adder unit(new PC + Immediate*4).
        ''' 
        return self.ImmshiftLeft2()+self.new_PC

    def run(self, mode = 0, untill = 1000000000):
        """
            This runs the processor.
        """
        self.__clock = 0

        if (mode == 0):
            while(self.__clock < untill and self.__status != Status.EXIT):
                self.__clock += 1
                print(f"Starting clock cycle {self.__clock}")
                
                #Instruction Fetch
                self.RunMCU()
                self.__status = self.ALU.run()
                self.WriteData()
                self.ReadData()
                self.RegisterFile.write()
                self.PC.writeVal(self.PCSelectMux.getData())




            else:
                if(self)

        elif (mode == 1):
            while(self.__clock < untill and self.__status != Status.EXIT)
                self.__clock += 1
                print(f"Starting clock cycle {self.__clock}")

        else:
            print("Invalid mode for running the Processor")
