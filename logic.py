import gui
import tkinter as tk
from Processor import *
from ALU import *
from ALU_Control import *
from Control import *
from Memory import *
from Multiplexer import *
from RegSet import *
from Register import *
from Utilities import *
from Splitter import *


class logic:

    def __init__(self):
        self.l = []

        self.canvas = gui.canvas

        self.registers = gui.registers[1:]  # [name, number, value]

        self.rd_tb = gui.rd_tb
        self.rr1_tb = gui.rr1_tb
        self.rr2_tb = gui.rr2_tb
        self.rr3_tb = gui.rr3_tb
        self.tb_15_0 = gui.tb_15_0
        self.rd2_tb = gui.rd2_tb
        self.wd_tb = gui.wd_tb
        self.rd1_tb = gui.rd1_tb
        self.rw_tb = gui.rw_tb
        self.j_tb = gui.j_tb
        self.b_tb = gui.b_tb
        self.mr_tb = gui.mr_tb
        self.mtr_tb = gui.mtr_tb
        self.aluo_tb = gui.aluo_tb
        self.mw_tb = gui.mw_tb
        self.alus_tb = gui.alus_tb

        self.kernel_input = gui.kernel_input
        self.kernel_output = gui.kernel_output
        self.kernel_output.configure(state=tk.DISABLED)

        self.play_button = gui.play_button
        self.play_button.configure(command=self.play)
        self.play_one_step_button = gui.play_one_step_button
        self.play_one_step_button.configure(command=self.play_1)
        self.input_text = gui.input_text
        self.input_text.configure(command=self.get_KI)

        self.kernInputWait = tk.IntVar()
        self.playOneWait = tk.IntVar()

    def dumpkern(self, data):
        self.dump_reg_image()
        self.kernel_output.configure(state=tk.NORMAL)
        self.kernel_output.insert(tk.END, data)
        self.kernel_output.configure(state=tk.DISABLED)

    def play(self):
        self.__clock = 0
        self.__status = Status.CONTINUE
        self.play_button.configure(command=lambda: 0)
        self.play_one_step_button.configure(command=lambda: 0)
        while (self.__clock < self.untill and self.__status != Status.EXIT):
            self.dump_reg_image()
            self.__clock += 1
            self.proc.callInstructionRun()
            self.__status = self.proc.getStatus()
        else:
            if (self.__clock == self.untill):
                self.dumpkern(f"\nReached Breakpoint before clock cycle {self.__clock} and instruction opcode = {
                    self.proc.splitter.getOpcode()} and functin = {self.proc.splitter.getFunct()}\n")
            else:
                self.dumpkern(f"\nProgram Succesfully terminated at clock cycle {
                    self.__clock}\n")

        self.play_button.configure(command=lambda: self.play())
        self.play_one_step_button.configure(command=self.dump_reg_image)

    def play_1(self):
        self.__clock = 0
        self.__status = Status.CONTINUE
        self.play_button.configure(command=lambda: 0)
        self.play_one_step_button.configure(
            command=lambda: self.playOneWait.set(1))
        while (self.__clock < self.untill and self.__status != Status.EXIT):
            self.dump_reg_image()
            self.play_one_step_button.wait_variable(self.playOneWait)
            self.playOneWait.set(0)
            self.__clock += 1
            self.proc.callInstructionRun()
            self.__status = self.proc.getStatus()
        else:
            if (self.__clock == self.untill):
                self.dumpkern(f"\nReached Breakpoint before clock cycle {self.__clock} and instruction opcode = {
                    self.proc.splitter.getOpcode()} and functin = {self.proc.splitter.getFunct()}\n")
            else:
                self.dumpkern(f"\nProgram Succesfully terminated at clock cycle {
                    self.__clock}\n")

        self.play_button.configure(command=lambda: self.play())
        self.play_one_step_button.configure(command=self.dump_reg_image)

    def dump_reg_image(self):
        text = "hello world"
        self.canvas.itemconfig(self.j_tb, text=text)

        regs = self.proc.dumpRegToGUI()
        for i in range(len(self.registers)):
            self.canvas.itemconfig(self.registers[i][2], text=regs[i][0])

    def getKernIn(self):
        self.input_text.wait_variable(self.kernInputWait)
        self.kernInputWait.set(0)
        return self.l[-1]

    def get_KI(self):
        text = self.kernel_input.get() + '\n'
        self.dumpkern(text)
        self.l.append(text)
        print(text, end='')
        self.kernel_input.delete(0, tk.END)
        self.kernInputWait.set(1)

    def run(self, proc, untill):
        self.untill = untill
        self.proc = proc
        gui.window.resizable(False, False)
        gui.window.mainloop()


if __name__ == "__main__":
    g = logic()
    g.run(0)
