from Utilities import *
from Control import *

class ALUControl:
    '''
        Defines the ALUControl class to map the ALU opcodes and funct field values to the right operation code for ALU.
    '''
    def __init__(self, control = None, settr = None, aluOP = ALUOp.DEF, funct = Funct.DEF):
        '''
            @param aluOP: An optional parameter if the user wants to set a value for ALUOp during instantiation.
                          Set to ALU.DEF as default.
            @param funct: An optional parameter if the user wants to set a value for funct during instantiation.
                          Set to Funct.DEf as default.
            @param control: It is the control line sent from the main controller.
        '''

        if (control == None):
            control = self._ground

        if (settr == None):
            settr = self._ground
        
        self.__ctrl = settr
        
        typeCheck({control:Callable})
        self.__control = control

        try:    
            self.__ALUOp = ALUOp(aluOP)
        except:
            printErrorandExit("Invalid operation request.\nNo such ALU opcode exists.")
        try:
            self.__funct = Funct(funct)
        except:
            printErrorandExit("Invalid operation request.\nNo such funct value exists.")

        self.__rf_operations = {
                   Funct.SLL       :        Operation.SLL,
                   Funct.SRL       :        Operation.SRL,
                   Funct.SRA       :        Operation.SRA,
                   Funct.XOR       :        Operation.XOR,
                   Funct.SUBU      :        Operation.SUB,
                   Funct.ADDU      :        Operation.ADD,
                   Funct.ADD       :        Operation.ADD,
                   Funct.SUB       :        Operation.SUB,
                   Funct.SLT       :        Operation.COMP,
                   Funct.SLTU      :        Operation.UNSIGNED_COMP,
                   Funct.JR        :        Operation.NOP,
                   Funct.BREAK     :        Operation.RET,
                   Funct.SYSCALL   :        Operation.MAG1,
                   Funct.MFHI      :        Operation.MAG2,
                   Funct.MFLO      :        Operation.MAG3,
                   Funct.DIV       :        Operation.DIV,
                   Funct.DEF       :        Operation.NOP
                   }
        
        self.__operations = {
                   ALUOp.ADDI      :       Operation.ADD,
                   ALUOp.ADDIU     :       Operation.ADD,
                   ALUOp.BEQ       :       Operation.SUB,
                   ALUOp.BNE       :       Operation.SUB,
                   ALUOp.LUI       :       Operation.LUI,
                   ALUOp.LW        :       Operation.ADD,
                   ALUOp.ORI       :       Operation.OR,
                   ALUOp.SLTI      :       Operation.COMP,
                   ALUOp.SW        :       Operation.ADD,
                   ALUOp.R_FORMAT  :       self.__rf_operations[self.__funct],
                   ALUOp.J         :       Operation.NOP,
                   ALUOp.JAL       :       Operation.NOP,
                   ALUOp.DEF       :       Operation.NOP,
                   ALUOp.MUL       :       Operation.MUL
                   }


    def _ground(self, val=0):
        """
            It grounds control signals.
        """

        return 0
        
    def __pcSelectModifier(self):
        '''
            Changes the pcSelect control signal if instruction is a jr.
        '''
        self.__ctrl(3)
    def __setFunct(self, funct: str):
        '''
            Sets the value of the funct field. 
            @param funct: The funct field value.
        '''
        typeCheck({funct: str})
        ###check for the length of string after making the support file..
        try:
            if(Funct(funct) in Funct):
                self.__funct = Funct(funct)
                self.__operations[ALUOp.R_FORMAT] = self.__rf_operations[self.__funct]
                return
        except:
            printErrorandExit("Invalid operation request.\n No such funct value exists.")
        
    def __setALUOp(self):
        '''
            Fetches the ALU opcode from the Control and sets it.
        '''
        ctrl = ALUOp(self.__control())
        if(ctrl not in ALUOp):
            printErrorandExit("Invalid operation request.\nNo such ALU opcode exists.")
        self.__ALUOp = ctrl
        return
    
    def getOperation(self, funct = None, fetchALUOp = True):
        '''
            Returns the operation code to be given to the ALU unit.
            @param funct: The function field value. If no value is given, it maintains the previous value.
            @param fetchALUOp: If set to false, doesn't fetch any value from the Control. True by default.
        '''
        if(fetchALUOp):
            self.__setALUOp()
        if(funct != None and self.__ALUOp == ALUOp.R_FORMAT):
            self.__setFunct(funct)
        
        if(self.__ALUOp not in self.__operations or self.__funct not in self.__rf_operations):
            printErrorandExit("ALU cannot handle this request. Please update the ALU.")
        if(self.__ALUOp==ALUOp.R_FORMAT and self.__funct == Funct.JR):
            self.__pcSelectModifier()
        return self.__operations[self.__ALUOp]
    
if __name__ == '__main__':
    
    def getOpcode():
        return input("Enter the required Opcodes: ")
    C = Control()
    aluc = ALUControl(C.getALUOp)
    #aluc = ALUControl(C.getALUOp, "011", "111111")
    while True:
        C.run(getOpcode())
        print(aluc.getOperation("100001"))
