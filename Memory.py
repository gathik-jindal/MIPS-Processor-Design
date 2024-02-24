from abc import ABC, abstractmethod
import linecache
from Utilities import typeCheck, printErrorandExit, convertToInt, convertToBase


class Memory(ABC):
    """
    Parent for various memory classes.
    """

    def __init__(self, fileName="LinkedListData.txt") -> None:
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
    def storeWord(self, value: int, locatoin: int) -> None:
        """
        Stores the value by converting it to 8 digit hexadeciaml and stores
        it at that memory location.
        """

        pass


class InstructionMemory(Memory):
    """
    Handles/Contains strictly the .text part.
    Note the file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListText") -> None:
        super().__init__(fileName)

    def loadWord(self, location: int) -> str:
        """
        Fetches the instruction at memory location <location>.
        """
        pass


class DataMemory(Memory):
    """
    Handles/Contains strictly the .data part.
    Note file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListData.txt") -> None:
        super().__init__(fileName)

    def loadWord(self, location=convertToInt("10010000")) -> int:
        """
        Gets the word from that Memory address.
        """
        typeCheck({location: int})

        location = location - convertToInt("10010000")

        location += 1

        linecache.checkcache(self._fileName)
        word = linecache.getline(self._fileName, location).rstrip("\n")

        word = convertToInt(word, 16)

        return word

    def storeWord(self, value: int, location=convertToInt("10010000")) -> None:
        """
        Stores the word in the proceeding 32 bits / 4 memory location.
        In reality it is stored as 8 hexadecimal digits.
        Location and value should be of type integer.
        """

        typeCheck({value: int, location: int})

        location = location - convertToInt("10010000")

        value = convertToBase(value)

        with open(self._fileName, 'r') as fh:
            lines = fh.readlines()

        value = "0"*(8 - len(value)) + value
        lines[location] = value + '\n'

        with open(self._fileName, 'w') as fh:
            fh.writelines(lines)


if __name__ == "__main__":

    # .data starts from 0x10010000

    obj = DataMemory("LinkedListData")
    x = 1
    print(obj.loadWord(convertToInt("10010000") + x))
    obj.storeWord(26, convertToInt("10010000") + x)
    print(obj.loadWord(convertToInt("10010000") + x))
