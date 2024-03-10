from Utilities import *
from typing import Callable

class Multiplexer():
    def __init__(self, size: int, control: Callable):
        '''
            Creates an instance of a Multiplexer. Size is scaled up to a power of 2.
            The second parameter must be a Callable(function) object that returns an integer value.
        '''
        typeCheck({size: int, control: Callable, control(): int})
        if(size<=1):
            printErrorandExit(f"Invalid size for a multiplexer.")
        self.__size = 2**ceil(log2(size))
        self.__input = [self.__ground for i in range(self.__size)]
        self.__control = control

    def __ground(self):
        '''
            Used for grounding input
        '''
        return 0
    def connectData(self, line: int, data: Callable):
        '''
            A method to connect a port of mux to some data.
            The parameter data must be a Callable(function) object that 
            returns any value.
        '''
        typeCheck({line: int, data: Callable})
        if(line>self.__size):
            printErrorandExit(f"No such port exists for a {self.__size}:{log2(self.__size)} mux.")
        self.__input[line] = data
        return
  
    def getData(self):
        '''
            Method to retrieve data from the mux. Control line
            controls the output of the mux.
        '''
        if(self.__control()>self.__size-1):
            printErrorandExit(f"Invalid Control Signal.")

        return self.__input[self.__control()]############

