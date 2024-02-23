from Utilities import *
from ALU_Control import *

class ALU():
  
  """
    It is the ALU of a processor and can perform functions like addition, subtraction, etc.
  """

  def __init__(self, control = None, inpPortCount = 2, outPortCount = 1):
    """
      This is a constructor that creates an ALU for a processor. The created ALU variable number of input and output ports.
    """

    if (control = None):
      control = self._ground
      
    typeCheck({control : Callable, inpPortCount : int, outPortCount : int})
    
    self.__control = control
    self.__iPC = inpPortCount
    self.__oPC = outPortCount

    self.__inpPorts = [ self._ground for i in range(self.__iPC)] 
    self.__outPorts = [ self._ground for i in range(self.__oPC)] 

    self.__operations = {

    }

    def _ground(self):
      """
          Used for grounding control signals
      """

    def run(self):
      """
      """

      pass

    def setInputConbnection(self, portID):
      pass

    def getOutput(self, portID):
      pass
