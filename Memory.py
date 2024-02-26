from abc import ABC, abstractmethod
import linecache
from Utilities import typeCheck, printErrorandExit
from typing import Callable

DATA = 0x10010000
STACKPOINTER = 0x7fffeffc
GLOBALPOINTER = 0x10008000
TEXT = 0x00400000

MAXSTACKSIZE = 10000    # in bytes


class Memory(ABC):
    """
    Parent for various memory classes.
    """

    def __init__(self, fileName: str) -> None:
        typeCheck({fileName: str})

        self._fileName = "Memory/" + fileName

        if (self._fileName.endswith(".txt") == False):
            self._fileName = self._fileName + ".txt"

    @abstractmethod
    def loadWord(self, location: int) -> str:
        """
        Fetches the 32 bit word at that memory location.
        """

        pass

    @abstractmethod
    def storeWord(self, value: str, location: int) -> None:
        """
        Stores the value at that memory location.
        """

        pass


class DataMemory(Memory):
    """
    Handles which part of memory to access.
    """

    def __init__(self, readControl: Callable, writeControl: Callable, fileNameData: str, fileNameStack: str, fileNameGlobal: str) -> None:
        """
        Initializer

        readControl: callable for the dataRead control signal
        writeControl : callable for the dataWrite control signal
        fileNameData: file name containing the .data part
        fileNameStack: file name for containing stack
        fileNameGlobal: file name for containing global (heap)
        """
        typeCheck({fileNameGlobal: str, fileNameData: str, fileNameStack: str,
                  readControl: Callable, writeControl: Callable})

        self.__fileNameGlobal = fileNameGlobal
        self.__fileNameData = fileNameData
        self.__fileNameStack = fileNameStack

        self.__readControl = readControl
        self.__writeControl = writeControl

        self.__dataMem = Data(readControl, writeControl, self.__fileNameData)
        self.__global = Global(self.__fileNameGlobal)
        self.__stack = Stack(self.__fileNameStack)

    def loadWord(self, location: int) -> str:
        """
        Loads the word into that memory location.
        """

        if (self.__readControl() == 1):
            if (location < DATA):
                return self.__global.loadWord(location)
            else:
                if (STACKPOINTER - location < MAXSTACKSIZE):
                    return self.__stack.loadWord(location)
                else:
                    return self.__dataMem.loadWord(location)

        return "0"

    def storeWord(self, value: str, location: int) -> None:
        """
        Store the word at that memory location.
        """

        if (self.__writeControl() == 1):
            if (location < DATA):
                return self.__global.storeWord(value, location)
            else:
                if (STACKPOINTER - location < MAXSTACKSIZE):
                    return self.__stack.storeWord(value, location)
                else:
                    return self.__dataMem.storeWord(value, location)

        return "0"

    def loadString(self, location: int) -> str:
        """
        Reads the string until a null terminating character is read.
        """
        return self.__dataMem.loadString(location)

    def malloc(self, bytes: int) -> int:
        """
        Mallocs some bytes.
        """

        return self.__global.malloc(bytes)


class Global(Memory):
    """
    Handles/Contains strictly the memory handeled by $gp.
    Note the file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListGlobalBin.txt") -> None:
        self.__gpWrtToFile = 0
        super().__init__(fileName)

    def storeWord(self, value: str, location: int) -> None:
        """
        Stores the word in the global heap.
        """

        if (type(0) == type(value)):
            val = value
            i = 0
            ans = ""
            while (i < 32):
                i += 1
                ans = ans + str(val % 2)
                val = val >> 1

        value = ans[::-1]

        typeCheck({location: int, value: str})

        location = location - GLOBALPOINTER

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4
        location += self.__gpWrtToFile

        with open(self._fileName, 'r') as fh:
            lines = fh.readlines()

        if location >= len(lines):
            for i in range(len(lines), location+1):
                lines.append('\n')

        if location < 0:
            while (location < 0):
                lines = ['\n'] + lines
                self.__gpWrtToFile += 1
                location += 1

        lines[location] = value + '\n'

        with open(self._fileName, 'w') as fh:
            fh.writelines(lines)

    def loadWord(self, location: int) -> str:
        """
        Loads the word from the global heap.
        """

        typeCheck({location: int})

        location = location - GLOBALPOINTER

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4
        location += 1 + self.__gpWrtToFile

        linecache.checkcache(self._fileName)
        word = linecache.getline(self._fileName, location).rstrip("\n")

        return word

    def malloc(self, bytes: int) -> int:
        """
        Used for mallocing space in the heap, returns the address.
        For now bytes have to be a multiple of 4.
        """

        if (bytes % 4 != 0):
            printErrorandExit(
                "Number of bytes for malloc is not a multiple of 4.")

        bytes //= 4

        with open(self._fileName, 'r') as fh:
            lines = fh.readlines()
            length = len(lines)

        while (bytes > 0):
            lines.append('\n')
            bytes -= 1

        with open(self._fileName, 'w') as fh:
            fh.writelines(lines)

        return length + GLOBALPOINTER - self.__gpWrtToFile


class Data(Memory):
    """
    Handles/Contains strictly the .data part.
    Note file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, readControl: Callable, writeControl: Callable, fileName="LinkedListData.txt") -> None:
        super().__init__(fileName)

        typeCheck({readControl: Callable, writeControl: Callable})

        self.__readControl = readControl
        self.__writeControl = writeControl

    def loadWord(self, location=None) -> str:
        """
        Loads the 32 bit word from the address
        """
        if (self.__readControl() == 0):
            print("Read Enable is 0, cannot read word from DataMemory.")
            return "0"
        return self.__loadWord(location)

    def storeWord(self, value=None, location=None) -> str:
        """
        Stores the word in the proceeding 32 bits / 4 memory location.
        Location and value should be of type integer.
        """
        if (self.__writeControl() == 0):
            print("Write Enable is 0, cannot write word to DataMemory.")
            return "0"
        self.__storeWord(value, location)

    def loadString(self, location: int) -> str:
        """
        This function gets the entire word (string), until the null terminating
        byte is read.

        It has a location param, which specifies the starting location of the string.
        """

        word = ""
        flag = True

        location = location - DATA
        precLocation = 4 - location % 4
        location //= 4

        linecache.checkcache(self._fileName)

        if (precLocation % 4 != 0):
            location += 1

            temp = linecache.getline(self._fileName, location)

            for i in range(precLocation-1, -1, -1):
                chars = temp[8*i:8*i+8]
                chars = chr(int(chars, 2))

                if chars == '\0':
                    flag = False
                    break

                word = word + chars

        location += 1

        while (flag):
            temp = linecache.getline(self._fileName, location).rstrip("\n")
            for i in range(3, -1, -1):
                chars = temp[8*i:8*i+8]
                chars = chr(int(chars, 2))

                if chars == '\0':
                    flag = False
                    break

                word = word + chars
            location += 1

        return word

    def __loadWord(self, location=DATA) -> int:
        """
        Gets the word from that Memory address.
        """
        typeCheck({location: int})

        location = location - DATA

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4
        location += 1

        linecache.checkcache(self._fileName)
        word = linecache.getline(self._fileName, location).rstrip("\n")

        return word

    def __storeWord(self, value: str, location=DATA) -> None:
        """
        Stores the word in the proceeding 32 bits / 4 memory location.
        Location and value should be of type integer.
        """

        typeCheck({value: str, location: int})

        location = location - DATA

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4

        with open(self._fileName, 'r') as fh:
            lines = fh.readlines()

        lines[location] = value + '\n'

        with open(self._fileName, 'w') as fh:
            fh.writelines(lines)


class Stack(Memory):
    """
    Handles/Contains strictly the memory handeled by $sp.
    Note the file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListStackBin.txt") -> None:
        super().__init__(fileName)

    def storeWord(self, value: str, location: int) -> None:
        """
        Stores the word in the stack.
        """
        typeCheck({location: int, value: str})

        location = STACKPOINTER - location

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4

        with open(self._fileName, 'r') as fh:
            lines = fh.readlines()

        if location >= len(lines):
            for i in range(len(lines), location+1):
                lines.append('\n')

        lines[location] = value + '\n'

        with open(self._fileName, 'w') as fh:
            fh.writelines(lines)

    def loadWord(self, location: int) -> str:
        """
        Loads the word from the stack.
        """

        typeCheck({location: int, value: str})

        location = STACKPOINTER - location

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4
        location += 1

        linecache.checkcache(self._fileName)
        word = linecache.getline(self._fileName, location).rstrip("\n")

        return word


class InstructionMemory(Memory):
    """
    Handles/Contains strictly the .text part.
    Only has a loadWord method.
    Note the file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListTextBin") -> None:
        super().__init__(fileName)

    def storeWord(self, value: str, location: int) -> None:
        """
        Dummy class, will never be called.
        """

        printErrorandExit(
            "Error: storeWord was performed on InstructionMemory!")

    def loadWord(self, location: int) -> str:
        """
        Fetches the instruction at memory location <location>.
        """
        typeCheck({location: int})

        location = location - TEXT

        if (location % 4 != 0):
            printErrorandExit(
                f"Error: location ({location}) is not a multiple of 4.")

        location //= 4
        location += 1

        linecache.checkcache(self._fileName)
        word = linecache.getline(self._fileName, location).rstrip("\n")

        return word


def foo():
    return True


if __name__ == "__main__":

    # .data starts from 0x10010000 (DATA)
    # $sp starts from 0x7fffeffc (STACKPOINTER)
    # $gp starts from 0x10008000 (GLOBALPOINTER)
    # DATA = 0x10010000
    # STACKPOINTER = 0x7fffeffc
    # GLOBALPOINTER = 0x10008000
    # TEXT = 0x00400000
    value = "11111111111111111111111111111111"

    obj = DataMemory(foo, foo, "LinkedListDataBin",
                     "LinkedListStackBin", "LinkedListHeapBin")

    print(obj.malloc(100))

    # data
    x = 4
    print(obj.loadWord(DATA + x))
    obj.storeWord(value, DATA + x)
    print(obj.loadWord(DATA + x))
    print(obj.loadString(DATA + 70))

    # stack
    x = 8
    obj.storeWord(value, STACKPOINTER - x)
    print(obj.loadWord(STACKPOINTER - x))

    # global
    x = 8
    obj.storeWord(value, GLOBALPOINTER - x)
    print(obj.loadWord(GLOBALPOINTER - x))
    x = 0
    obj.storeWord(value, GLOBALPOINTER - x)
    print(obj.loadWord(GLOBALPOINTER - x))
    x = -8
    obj.storeWord(value, GLOBALPOINTER - x)
    print(obj.loadWord(GLOBALPOINTER - x))

    obj = InstructionMemory("LinkedListTextBin")
    x = 6
    print(obj.loadWord(TEXT + x*4))
