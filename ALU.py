from Utilities import *
from ALU_Control import *

class ALU():
  
  """
    It is the ALU of a processor and can perform functions like addition, subtraction, etc.
  """

  def __init__(self, control = None, inpPortCount = 3, outPortCount = 2):
    """
      This is a constructor that creates an ALU for a processor. The created ALU variable number of input and output ports.
    """

    if (control == None):
      control = self._ground
      
    typeCheck({control : Callable, inpPortCount : int, outPortCount : int})
    
    self.__control = control
    self.__iPC = inpPortCount
    self.__oPC = outPortCount

    self.__inpPorts = [ self._ground for i in range(self.__iPC)]        #Index 0: RD1; Index 1: ALUSrcMux; Index 2: shamt
    self.__outPorts = [ self._ground() for i in range(self.__oPC)]        #Index 0: Zero Flag; Index 1: ALUresult

    self.__operations = {
            Operation.NOP           :           self.__nop,
            Operation.ADD           :           self.__add,
            Operation.SLL           :           self.__sll,
            Operation.SRA           :           self.__sra,
            Operation.SUB           :           self.__sub,
            Operation.LUI           :           self.__lui,
            Operation.COMP          :           self.__comp,
            Operation.OR            :           self.__or,
            Operation.XOR           :           self.__xor,
            Operation.DIV           :           self.__div,
            Operation.MUL           :           self.__mul,
            Operation.RET           :           self.__ret,
            Operation.MAG           :           self.__mag
    }

  def _ground(self):
    """
        Used for grounding control signals
    """

    return 0

  def run(self):
    """
        This method executes the operation based on the current control value.
    """
    self.__operation[self.__control()]()

  def __nop(self):
    """
        This method executes a NOP(does nothing).
    """
    pass


  def __add(self):
    """
        Method for add operation.
    """
    self.__outPorts[1] = self.__inpPorts[0]()+self.__inpPorts[1]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __sll(self):
    """
        Method for shift left logical operation.
    """

    self.__outPorts[1] = self.__inpPorts[0]() << self.__inpPorts[2]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __sra(self):
    """
        Method for shift right arithmetic operation.
    """
    self.__outPorts[1] = self.__inpPorts[0]() >> self.__inpPorts[2]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __sub(self):
    """
        Method for sub operation.
    """
    self.__outPorts[1] = self.__inpPorts[0]()-self.__inpPorts[1]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __comp(self):
    """
        Method for algebraic comparison of inputs.
    """
    self.__outPorts[1] = self.__inpPorts[0]()<self.__inpPorts[1]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2


  def __or(self):
    """
        Method for bitwise or operation.
    """
    self.__outPorts[1] = self.__inpPorts[0]() | self.__inpPorts[1]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __xor(self):
    """
        Method for bitwise xor operation.
    """
    self.__outPorts[1] = self.__inpPorts[0]() ^ self.__inpPorts[1]()
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __div(self):
    """

    """

    pass

  def __mul(self):
    """
    """

    pass

  def __ret(self):
    """
        Terminates the program.
    """
    print("Break instruction encountered.\nProgram Terminated.")
    sys.exit(0)

  def __lui(self):
    '''
        Special operation to right shift immediate value by 16
    '''
    self.__outPorts[1] = self.__inpPorts[1] << 16
    self.__outPorts[0] = ((self.__outPorts[1] and 1)+1)%2

  def __mag(self):
    """
        This method handles all the syscall, mfho, mfli instructions.
    """
    pass


  def setInputConnection(self, portID: int, portConnection:Callable):
    typeCheck({portID : int, portConnection: Callable})
    if(portID >= self.__iPC):
      printErrorandExit(f"Invalid portID for an ALU with {self.__iPC} input ports.")
    self.__inpPorts[portID] = portConnection

  def getOutput(self, portID=1):
    '''
        This method can be used to get output from anyone of the output ports of the ALU.
        It is set to return output of port 1 by default.
    '''
    typeCheck({portID: int})
    if(portID >= self.__oPC):
      printErrorandExit(f"Invalid portID for an ALU with {self.__oPC} output ports.")
    return self.__outPorts[portID]
  
  def getZeroFlag(self):
    '''
        Method to get the zero flag from ALU. 
    '''
    return self.__outPorts[0]
