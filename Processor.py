from ALU import *
from ALU_Control import *
from Control import *
from Memory import *
from Multiplexer import *
from RegSet import *
from Register import *
from Utilities import *
from Splitter import *
import time


class Processor():

    """
        A processor that understands the MIPS ISA.
    """

    def __init__(self):
        """
            Creates a processor.
        """

        # Creating the objects and setting up the data path

        self.__status = Status.CONTINUE

        self.PC = Register(32, 0x400000)
        self.HI = Register(32)
        self.LO = Register(32)

        self.Controller = Control()
        self.Controller.run(opcode="000000", enable=0)

        self.InstructionMemory = InstructionMemory(
            input("Enter instruction file name (Has to be in memory folder): "))
        self.DataMemory = DataMemory(self.Controller.getMemRead, self.Controller.getMemWrite, input("Enter data file name (Has to be in memory folder): "), input(
            "Enter global data file name (Has to be in memory folder): "), input("Enter stack file name (Has to be in memory folder): "))

        self.ALUController = ALUControl(
            self.Controller.getALUOp, self.Controller.setpcSelect)
        self.ALU = ALU(control=self.getACUop)

        self.WriteBackMux = Multiplexer(3, self.Controller.getWB)
        self.__connectWriteBackMux()

        self.splitter = Splitter(self.__FetchData)

        self.RegDstMux = Multiplexer(3, self.Controller.getRegDest)
        self.__connectRegDstMux()

        self.RegisterFile = RegSet(
            readPortCount=2, writePortCount=1, count=32, size=32, defaultVal=0)
        self.RegisterFile.writeEnable(self.Controller.getRegWrite)
        self.RegisterFile.readEnable(self.Controller.getRegRead)
        self.__connectRegFile()

        self.ALUSrcMux = Multiplexer(2, self.Controller.getALUSrc)
        self.__connectALUSrcMux()

        self.BranchSelectMux = Multiplexer(2, self.Controller.getBranchSelect)
        self.__connectBranchSelectMux()
        self.PCSelectMux = Multiplexer(4, self.Controller.getpcSelect)
        self.__connectPCSelectMux()

        self.__connectALU()

    def __FetchData(self):
        return self.InstructionMemory.loadWord(self.PC.getVal())

    def __connectRegFile(self):
        '''
            Method for connecting all the ports of the Register file.
        '''
        self.RegisterFile.connectReadPort(0, self.splitter.getRS)
        self.RegisterFile.connectReadPort(1, self.splitter.getRT)

        self.RegisterFile.connectWritePort(
            0, self.RegDstMux.getData, self.WriteBackMux.getData)

    def __connectALU(self):
        '''
            Method for connecting all the input ports to the ALU.
        '''
        
        self.ALU.setInputConnection(0, self.RegisterFile.read)
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
        print(self.RegisterFile.read)
        self.ALUSrcMux.connectData(0, self.RegisterFile.read)
        self.ALUSrcMux.connectData(1, lambda a: self.splitter.getImm)

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
        self.PCSelectMux.connectData(0, lambda: self.PCadder)
        self.PCSelectMux.connectData(1, lambda: self.BranchAdder)
        self.PCSelectMux.connectData(2, lambda: self.JumpshiftLeft2)
        self.PCSelectMux.connectData(3, self.RegisterFile.read)

    def RunMCU(self):
        '''
            Runs the Main Control Unit.
        '''

        self.Controller.run(opcode=self.splitter.getOpcode())

    def getACUop(self):
        '''
            Method for retrieving the operation code from ALU Control Unit.
        '''
        return self.ALUController.getOperation(funct=self.splitter.getFunct())

    def ReadData(self):
        '''
            Method for retrieving data from Data Memory.
        '''

        return self.DataMemory.loadWord(self.ALU.getOutput())

    def WriteData(self):
        '''
            Method for writing to the Memory.
        '''
        self.DataMemory.storeWord(
            location=self.ALU.getOutput(), value=self.RegisterFile.read(1)())

    def signExtend(self):
        return self.splitter.getImm()

    def notZero(self):
        '''
            This method is for the not gate after the Zero flag(for BNE).
        '''
        return int(not (self.ALU.getZeroFlag()))

    def branchGate(self):
        '''
            This method is for the AND gate for branch instruction.
        '''
        return self.Controller.getBranch() and self.ALU.getZeroFlag()

    def ImmshiftLeft2(self):
        '''
            This method implements the Left Shifter(by 2) on Immediate value.
        '''
        return self.signExtend() << 2

    def JumpshiftLeft2(self):
        '''
            This method implements the Left Shifter(by 2) on Jump Location field.
        '''
        return self.splitter.getJumpLoc() << 2

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

    def __instructionRun(self):
        """
            This runs the processor.
        """
        # Instruction Fetch
        self.RunMCU()
        print("hi", self.RegisterFile.read(0)())
        self.__status = self.ALU.run()

        if (self.__status == Status.CONTINUE):
            self.WriteData()
            self.ReadData()
            self.RegisterFile.write()

        elif (self.__status == Status.EXIT):
            return

        elif (self.__status == Status.MUL):

            a = self.RegisterFile.read(0)()
            b = self.RegisterFile.read(1)()

            val = a*b
            i = 0
            ans = ""
            while (i < 32):
                i += 1
                ans = ans + str(val % 2)
                val = val >> 1
            ans = int(ans[::-1], 2)
            print(ans)
            self.RegisterFile.hardcode(Splitter.getRD(), ans)
            self.LO.writeVal(ans)

            i = 0
            ans = ""
            while (i < 32):
                i += 1
                ans = ans + str(val % 2)
                val = val >> 1
            ans = int(ans[::-1], 2)
            print(ans)
            self.HI.writeVal(ans)

        elif (self.__status == Status.DIV):

            a = self.RegisterFile.read(0)()
            b = self.RegisterFile.read(1)()

            val = a//b
            rem = a % b

            i = 0
            ans = ""
            while (i < 32):
                i += 1
                ans = ans + str(val % 2)
                val = val >> 1
            val = int(ans[::-1], 2)

            i = 0
            ans = ""
            while (i < 32):
                i += 1
                ans = ans + str(rem % 2)
                rem = rem >> 1
            rem = int(ans[::-1], 2)

            self.HI.writeVal(rem)
            self.LO.writeVal(val)

        else:
            self.magic()
        self.PC.writeVal(self.PCSelectMux.getData()()())

    def magic(self):
        print(self.__status)
        if (self.__status.value == Status.MAGIC2.value):
            self.RegisterFile.hardcode(Splitter.getRD(), self.HI.readVal())

        elif (self.__status == Status.MAGIC3):
            self.RegisterFile.hardcode(Splitter.getRD(), self.LO.readVal())

        elif (self.__status == Status.MAGIC1):
            code = self.RegisterFile._regset[2].readVal()
            print(code)
            if code == 1:
                print(self.RegisterFile._regset[4].readVal())

            elif code == 4:
                address = self.RegisterFile._regset[4].readVal()
                string = self.DataMemory.loadString(address)
                print(string)

            elif code == 9:
                n = self.RegisterFile._regset[4].readVal()
                addr = self.DataMemory.malloc(n)
                self.RegisterFile._regset[2].writeVal(addr)

            elif code == 10:
                self.__status = Status.EXIT

            elif code == 5:
                val = int(input())
                self.RegisterFile._regset[2].writeVal(val)

            elif code == 30:
                val = time.time() * 1000000
                val = val//1
                i = 0
                ans = ""
                while (i < 31):
                    i += 1
                    ans = ans + str(val % 2)
                    val = val >> 1
                val = int(ans[::-1], 2)
                self.RegisterFile._regset[4].writeVal(val)

            else:
                printErrorandExit("Unsupported syscall")

        else:
            printErrorandExit("Error status")

    def run(self, mode=0, untill=1000000000):
        """
            This runs the processor.
        """
        self.__clock = 0

        if (mode == 0):
            while (self.__clock < untill and self.__status != Status.EXIT):
                self.__clock += 1
                # input("Enter to continue:")
                print(f"Starting clock cycle {self.__clock}")
                self.__instructionRun()
                self.RegisterFile.dump()
                print()
            else:
                if (self.__clock == untill):
                    print(f"Reached Breakpoint before clock cycle {self.__clock}")
                else:
                    print(f"Program Succesfully terminated at clock cycle {self.__clock}")

        elif (mode == 1):
            while (self.__clock < untill and self.__status != Status.EXIT):
                self.__clock += 1
                # input("Enter to continue:")
                print(f"Starting clock cycle {self.__clock}")
                self.__instructionRun()
                self.RegisterFile.dump()
                print()
                # input()
            else:
                if (self.__clock == untill):
                    print(f"Reached Breakpoint before clock cycle {self.__clock}")
                else:
                    print(f"Program Succesfully terminated at clock cycle {self.__clock}")

        else:
            print("Invalid mode for running the Processor")


if __name__ == "__main__":

    P = Processor()
    P.run()
