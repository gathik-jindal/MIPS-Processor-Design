from Utilities import *
from Register import *


class RegSet():

    """
        Creates a group of Registers that can be accessed and overwritten.
    """

    def __init__(self, readPortCount:int, writePortCount:int, count:int, size:int, defaultVal = 0):

        """
            A group of "count" registers of size "size" are created and initiallized to 0
        """

        typeCheck({count:int, readPortCount:int, writePortCount:int, size:int, defaultVal:int})
        
        self._regset = [Register(size, defaultVal) for i in range(count)]
        self.__count = count
        
        self.__rPC = readPortCount
        self.__readLines = [self._ground for i in range(self.__rPC)]
        
        self.__wPC = writePortCount
        self.__writeLines = [self._ground for i in range(self.__wPC)]
        self.__dataLines = [self._ground for i in range(self.__wPC)]
        
        self.__we = self._ground
        self.__re = self._ground
        self.__mode = 1
        

    def hardcode(self, num, val):

        self._regset[num].writeVal(val)
        
    
    def _ground(self):

        """
            Used to ground signals.
        """

        return 0

    def changeMode(self):
        self.__mode = 1 - self.__mode

    def insertReg(self, pos:int, size:int, defaultVal = 0):
        
        """
            Adds another register at the required position.
        """
        
        typeCheck({pos:int, size:int, defaultVal:int})

        self._regset.insert(pos, Register(size, defaultVal))
        self.__count += 1


    def writeEnable(self, ctrl:Callable):

        """
            Sets the writeEnable control line
        """

        typeCheck({ctrl:Callable})
        self.__we = ctrl

    def readEnable(self, ctrl:Callable):

        """
            Sets the writeEnable control line
        """

        typeCheck({ctrl:Callable})
        self.__re = ctrl

    def connectReadPort(self, portID:int, regConnection:Callable):

        """
            Gives Read Address for port
        """

        typeCheck({portID:int, regConnection:Callable})
        if (self.__rPC <= portID):
            printErrorandExit(f"Invalid portID: {portID}")
            
        self.__readLines[portID] = regConnection

    def connectWritePort(self, portID:int, regConnection:Callable, dataConnection:Callable):

        """
            Gives Write Address for port

            regConnection should be a callable that returns.
        """

        typeCheck({portID:int, regConnection:Callable, dataConnection:Callable})
        if (self.__wPC <= portID):
            printErrorandExit(f"Invalid portID: {portID}")
            
        self.__writeLines[portID] = regConnection
        self.__dataLines[portID] = dataConnection

    def read(self, portID = 0):
        
        """
            Used to read from required port.
        """

        typeCheck({portID:int})
        if (self.__rPC <= portID):
            printErrorandExit(f"Invalid portID: {portID}")
            
        regNumber = (self.__readLines[portID])()
        if type(regNumber) == type("1"):
            regNumber = int("0"+regNumber,2)

        if (self.__count <= regNumber):
            printErrorandExit(f"Invalid Register ID: {regNumber}")

        if (self.__re() == 1):
            return ((self._regset[regNumber]).getVal)
        else:
            if (self.__mode):
                print("Reading is not enabled.")
            return self._ground

    def dump(self):
        print()
        n = 0
        for i in self._regset:
            print(f"${n}: {i.getVal()}", end=" ")
            n += 1
        print()

    def write(self, portID = 0):
        
        """
            Used to write from required port.
        """

        typeCheck({portID:int})
        if (self.__wPC <= portID):
            printErrorandExit(f"Invalid portID: {portID}")
        
        regNumber = (self.__writeLines[portID])()()
        if type(regNumber) == type("1"):
            regNumber = int("0" + regNumber,2)

        if (self.__count <= regNumber):
            printErrorandExit(f"Invalid Register ID: {regNumber}")
            
        writeData = self.__dataLines[portID]()()
        if type(writeData) == type("1"):
            writeData = int(writeData,2)

        if (self.__we() == 1):
            if (self.__mode):
                print(f"Writing value {writeData} to ${regNumber}.")
            self._regset[regNumber].writeVal(writeData)
        else:
            if (self.__mode):
                print("Write is not enabled")
            return self._ground

        if self.__mode:
            print()



if __name__ == "__main__":

    def giveData():
        return int(input("Enter data to be written: "))

    def setPort1():
        return int(input("Enter regiseter ID to be read from: "))

    def setPort2():
        return int(input("Enter regiseter ID to be read from: "))

    def setPort3():
        return int(input("Enter regiseter ID to be written to: "))

    def w():
        return int(input("Orders, sir. Sir !!!!!!!\n"))

    def r():
        return int(input("Orders sir. Sir !!!!!!!\n"))
    
    RegFile = RegSet(2, 1, 32, 32)
    RegFile.writeEnable(w)
    RegFile.readEnable(r)
    RegFile.connectReadPort(0, setPort1)
    RegFile.connectReadPort(1, setPort2) 
    RegFile.connectWritePort(0, setPort3, giveData)

    while (True):

        print("Reg Read Phase")
        print(RegFile.read(0)())
        print(RegFile.read(1)())

        print("Reg Write Phase")
        RegFile.write(0)
