from Utilities import *

class Splitter():
    def __init__(self, data: str):
        typeCheck({data : int})
        
        self.__data = data
    
    def getOpcode(self):
        return self.__data[:6]
    
    def getRS(self):
        return self.__data[6:11]
    
    def getRT(self):
        return self.__data[11:16]
    
    def getRD(self):
        return self.__data[16:21]
    
    def getImm(self):
        return self.__data[16:]
    
    def getShamt(self):
        return self.__data[21:26]
    
    def getFunct(self):
        return self.__data[26:]
    