from Utilities import *
from Controller import *

class ALUControl:
    '''
        Defines the ALUControl class to map the ALU opcodes and funct field values to the right operation code for ALU.
    '''
    def __init__(self, aluOP = ALUOp.DEF, funct = Funct.DEF):
        '''
            @param aluOP: An optional parameter if the user wants to set a value for ALUOp during instantiation.
                          Set to ALU.DEF as default.
            @param funct: An optional parameter if the user wants to set a value for funct during instantiation.
                          Set to Funct.DEf as default.
        '''
        try:
            if(ALUOp(aluOP) in ALUOp):
                self.__ALUOp = ALUOp(aluOP)
        except:
            printErrorandExit("Invalid operation request.\nNo such ALU opcode exists.")
        try:
            if(Funct(funct) in Funct):
                self.__funct = Funct(funct)
        except:
            printErrorandExit("Invalid operation request.\nNo such funct value exists.")

        self.__rf_operations = {
                   Funct.SLL       :        Operation.SLL,
                   Funct.SRA       :        Operation.SRA,
                   Funct.XOR       :        Operation.XOR,
                   Funct.SUBU      :        Operation.SUB,
                   Funct.ADDU      :        Operation.ADD,
                   Funct.ADD       :        Operation.ADD,
                   Funct.SUB       :        Operation.SUB,
                   Funct.SLT       :        Operation.COMP,
                   Funct.SLTU      :        Operation.COMP,
                   Funct.JR        :        Operation.NOP,
                   Funct.BREAK     :        Operation.RET,
                   Funct.SYSCALL   :        Operation.MAG,
                   Funct.MFHI      :        Operation.MAG,
                   Funct.MFLO      :        Operation.MAG,
                   Funct.DEF       :        Operation.NOP
                   }
        
        self.__operations = {
                   ALUOp.ADDI      :       Operation.ADD,
                   ALUOp.ADDIU     :       Operation.ADD,
                   ALUOp.BEQ       :       Operation.COMP,
                   ALUOp.BNE       :       Operation.COMP,
                   ALUOp.LUI       :       Operation.SLL,
                   ALUOp.LW        :       Operation.ADD,
                   ALUOp.ORI       :       Operation.OR,
                   ALUOp.SLTI      :       Operation.COMP,
                   ALUOp.SW        :       Operation.ADD,
                   ALUOp.R_FORMAT  :       self.__rf_operations[self.__funct],
                   ALUOp.J         :       Operation.NOP,
                   ALUOp.JAL       :       Operation.NOP,
                   ALUOp.DEF       :       Operation.NOP,
                   ALUOp.DIV       :       Operation.DIV,
                   ALUOp.MUL       :       Operation.MUL
                   }
 
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
            Fetches the ALU opcode from the controller and sets it.
        '''
        typeCheck({Controller.getOpcode(): Enum})
        if(Controller.getOpcode() not in ALUOp):
            printErrorandExit("Invalid operation request.\nNo such ALU opcode exists.")
        self.__ALUOp = Controller.getOpcode()
        return
    
    def getOperation(self, funct = None, fetchALUOp = True):
        '''
            Returns the operation code to be given to the ALU unit.
            @param funct: The function field value. If no value is given, it maintains the previous value.
            @param fetchALUOp: If set to false, doesn't fetch any value from the Controller. True by default.
        '''
        if(fetchALUOp):
            self.__setALUOp()
        print(self.__ALUOp)
        if(funct != None and self.__ALUOp == ALUOp.R_FORMAT):
            self.__setFunct(funct)
        print(self.__funct)
        
        if(self.__ALUOp not in self.__operations or self.__funct not in self.__rf_operations):
            printErrorandExit("ALU cannot handle this request. Please update the ALU.")
        return self.__operations[self.__ALUOp]
    
if __name__ == '__main__':
    aluc = ALUControl("011", "111111")
    print(aluc.getOperation("100001"))