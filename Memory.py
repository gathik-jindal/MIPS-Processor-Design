import linecache
from Utilities import typeCheck, printErrorandExit, convertToInt


class DataMemory:
    """
    Handles/Contains strictly the .data part.
    Note file provided should be of .TXT format.
    The fileName can optionally not have the filetype.
    """

    def __init__(self, fileName="LinkedListData.txt"):
        if not typeCheck({fileName:str}):
            printErrorandExit(f"{fileName} not of type str")

        self.__fileName = "Memory/" + fileName

        if (self.__fileName.endswith(".txt") == False):
            self.__fileName = self.__fileName + ".txt"

    # gets the next 4 bytes starting from the location itself
    def loadWord(self, location=0):
        pass
        """
        Gets the word from that Memory address.
        """
        if not typeCheck({location: int}):
            printErrorandExit(
                f"Location provided ({location}) not of type integer.")

        linecache.checkcache(self.__fileName)
        word = linecache.getline(self.__fileName, location).rstrip("\n")

        word = convertToInt(word, 16)

        return word


if __name__ == "__main__":
    obj = DataMemory("LinkedListData")

    print(obj.loadWord(0))