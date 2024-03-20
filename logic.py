import gui
import tkinter as tk
import Processor


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
        self.play_one_step_button = gui.play_one_step_button
        self.input_text = gui.input_text
        self.input_text.configure(command=self.get_KI)
        self.play_one_step_button.configure(command=self.dump_reg_image)

    def dump_reg_image(self):
        text = "hello world"
        self.canvas.itemconfig(self.j_tb, text=text)

        l = '0'*len(self.registers)
        for i in range(len(self.registers)):
            self.canvas.itemconfig(self.registers[i][2], text=l[i])

    def get_KI(self):
        text = self.kernel_input.get() + '\n'
        self.kernel_output.configure(state=tk.NORMAL)
        self.kernel_output.insert(tk.END, text)
        self.kernel_output.configure(state=tk.DISABLED)
        self.l.append(text)
        print(text, end='')

    def run(self, proc):
        self.proc = proc
        gui.window.resizable(False, False)
        gui.window.mainloop()


if __name__ == "__main__":
    g = logic()
    g.run(0)
