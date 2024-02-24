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

    self.__inpPorts = [ self._ground for i in range(self.__iPC)] 
    self.__outPorts = [ self._ground for i in range(self.__oPC)] 

    self.__operations = {
            Operation.NOP           :           self.__nop,
            Operation.ADD           :           self.__add,
            Operation.SLL           :           self.__sll,
            Operation.SRA           :           self.__sra,
            Operation.SUB           :           self.__sub,
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
      """

      pass

    def setInputConnection(self, portID):
      pass

    def getOutput(self, portID):
      pass
