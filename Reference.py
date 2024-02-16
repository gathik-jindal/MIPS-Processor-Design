def func1():
  return 1

def func2():
  return 2

def func3():
  return 3

def func4():
  return 4
  
class Controller():
    def __init__(self):
        self.__selectLine1 = 0
        self.__selectLine2 = 0      
        
    def line1(self):
        return self.__selectLine1

    def line2(self):
        return self.__selectLine2
        
    def run(self, op):
        self.__selectLine1 = op%2
        self.__selectLine2 = 1 - op%2 
        

class Mux():
    def __init__(self, size, cline):
        self.__mySelectLine = cline
        self.__data = [0 for i in range(size)]
        self.__size = size
        
    def connectData(self, lineNum, val):
        self.__data[lineNum] = val
        
    def getOutput(self):
        return self.__data[self.__mySelectLine()]()
        
if __name__ == "__main__":
    
    ctrl=Controller()
    m1 = Mux(2, ctrl.line1)
    m2 = Mux(2, ctrl.line2)
    m1.connectData(0, func1)
    m1.connectData(1, func2)
    m2.connectData(0, func3)
    m2.connectData(1, func4)
    
    while True:
        opcode = int(input())
        ctrl.run(opcode)
        print("m1:", m1.getOutput())
        print("m2:", m2.getOutput())
    
    
    
