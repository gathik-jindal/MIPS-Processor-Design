from Utilities import *

class Register:

    """
        This class simulates a register holding integers in 2's compliment form
    """
    
    def __init__(self, size:int, startVal = 0):
        
        """
            A Register is created of the required size and starting value.
        """

        typeCheck({size:int, startVal:int})
        if (size <= 0):
            printErrorandExit("Invalid Register Size")
        self.__size=size
        self.writeVal(startVal)

    
    def getSize(self):
        
        """
            It returns the size of the register.
        """

        return self.__size

    
    def getVal(self):
        
        """
            This gives the value held by the register in decimal form
        """
        
        return self.__val
 

    
    def __str__(self):

        """
            It returns the value held by the register in its binary form
        """
        
        val = self.__val
        i = 0
        ans = ""
        while(i < self.__size):
            i += 1
            ans = ans + str(val%2)
            val = val >> 1

        return ans[::-1]


    def inc(self, count:int):

        """
            It incriments the value stored in the register by "count"
        """

        typeCheck({count:int})
        self.__val = self.__val + count


    def readBin(self, start=0, end=None):
        
        """
            It returns a slice of the value held by the register in decimal form.
        """

        if end==None:
            end=self.__size

        typeCheck({start:int, end:int})
            
        return (str(self))[start:end]


    def writeBin(self, val, start=0, end=None):
        
        """
            It takes a string of bits as a value and overwrites the given register from [start, end).
        """
    
        if end==None:
            end=self.__size
        typeCheck({val:str, start:int, end:int})

        if ((len(val) != end - start)):
            print("val =", val, "start =", start, "end =", end)
            printErrorandExit("Invalid write size.")

        if ((end > self.__size) or (start < 0) or (end - start > self.__size)):
            print("val =", val, "start =", start, "end =", end)
            printErrorandExit("Invalid write bounds.")

        ans = str(self)
        self.__val = int((ans[:start:] + val + ans[end::]), 2)
        
        if (self.__val >= 2**(self.__size -1)):
            self.__val = - (int(str(self)[1::]))

            
    def readVal(self, start=0, end=None):
        
        """
            It returns a slice of the stored value in decimal form.
        """

        if end==None:
            end=self.__size

        typeCheck({start:int, end:int})
            
        return int((str(self))[start:end], 2)
            

    def writeVal(self, val):
        
        """
            It takes in a decimal value and overwrites the given register fully.
        """
            
        typeCheck({val:int})
        
        if((val >= 2**(self.__size-1)) or (val < ((-1) * (2**(self.__size -1))))):
            printErrorandExit("Invalid value to write.")

        self.__val = val



if __name__ == "__main__":
    
    R1 = Register(32)
    print(R1)
    print(len(str(R1)))
    print(R1.getSize())
    print(R1.getVal())
    
        
