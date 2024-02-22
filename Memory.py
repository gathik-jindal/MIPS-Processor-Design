import linecache
from Utilities import typeCheck, printErrorandExit, convertToInt, convertToBase


class DataMemory:
    """
    Handles/Contains strictly the .data part.
    Note file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListData.txt") -> None:
        if not typeCheck({fileName: str}):
            printErrorandExit(f"{fileName} not of type str")

        self.__fileName = "Memory/" + fileName

        if (self.__fileName.endswith(".txt") == False):
            self.__fileName = self.__fileName + ".txt"

    def loadWord(self, location=convertToInt("10010000")) -> int:
        """
        Gets the word from that Memory address.
        """
        if not typeCheck({location: int}):
            printErrorandExit(
                f"Location provided ({location}) not of type integer.")

        location = location - convertToInt("10010000")

        location += 1

        linecache.checkcache(self.__fileName)
        word = linecache.getline(self.__fileName, location).rstrip("\n")

        word = convertToInt(word, 16)

        return word

    def storeWord(self, value: int, location=convertToInt("10010000")) -> None:
        """
        Stores the word in the proceeding 32 bits / 4 memory location.

        location and value should be of type integer.
        """

        if not typeCheck({value: int, location: int}):
            printErrorandExit(f"value ({value}) or location ({
                              location}) is not of type integer.")

        location = location - convertToInt("10010000")

        value = convertToBase(value)

        with open(self.__fileName, 'r') as fh:
            lines = fh.readlines()

        value = "0"*(8 - len(value)) + value
        lines[location] = value + '\n'

        with open(self.__fileName, 'w') as fh:
            fh.writelines(lines)


if __name__ == "__main__":

    # .data starts from 0x10010000

    obj = DataMemory("LinkedListData")
    x = 1
    print(obj.loadWord(convertToInt("10010000") + x))
    obj.storeWord(26, convertToInt("10010000") + x)
    print(obj.loadWord(convertToInt("10010000") + x))
