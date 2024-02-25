from Utilities import *

class Splitter():
    '''
        Splitter class which splits the binary string from fetched instruction memory
    '''

    def __init__(self, data: str):
        '''
            Parameter data must be a string of size 32.
        '''
        typeCheck({data : int})
        self.__data = data

        if(data.size()>32):
            printErrorandExit("Invalid data provided.")


    def getOpcode(self):
        '''
            Method to get Opcode from the word.
        '''
        return self.__data[:6]
    
    def getRS(self):
        '''
           Method to get RS field from the word. 
        '''
        return int(self.__data[6:11], 2)
    
    def getRT(self):
        '''
           Method to get RT field from the word. 
        '''
        return int(self.__data[11:16], 2)
    
    def getRD(self):
        '''
           Method to get RD field from the word. 
        '''
        return int(self.__data[16:21], 2)
    
    def getImm(self):
        '''
           Method to get Immediate field from the word. 
        '''
        if(self.__data[6]==1):
            return int(self.__data[6:], 2)-2**16
        else:
            return int(self.__data[6:], 2)
    
    def getShamt(self):
        '''
           Method to get shamt field from the word. 
        '''
        return int(self.__data[21:26], 2)
    
    def getFunct(self):
        '''
           Method to get Funct field from the word. 
        '''
        return self.__data[26:]
    
    def getJumpLoc(self):
        '''
           Method to get JumpLoc field from the word. 
        '''
        return int(self.__data[6:], 2)
    
