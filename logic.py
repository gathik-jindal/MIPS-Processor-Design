import gui

canvas = gui.canvas

registers = gui.registers  # [name, number, value]

rd_tb = gui.rd_tb
rr1_tb = gui.rr1_tb
rr2_tb = gui.rr2_tb
rr3_tb = gui.rr3_tb
tb_15_0 = gui.tb_15_0
rd2_tb = gui.rd2_tb
wd_tb = gui.wd_tb
rd1_tb = gui.rd1_tb
rw_tb = gui.rw_tb
j_tb = gui.j_tb
b_tb = gui.b_tb
mr_tb = gui.mr_tb
mtr_tb = gui.mtr_tb
aluo_tb = gui.aluo_tb
mw_tb = gui.mw_tb
alus_tb = gui.alus_tb


def update_text():
    text = "hello world"
    canvas.itemconfig(j_tb, text=text)


play_button = gui.play_button
play_one_step_button = gui.play_one_step_button
input_text = gui.input_text

play_button.configure(command=update_text)

gui.window.resizable(False, False)
gui.window.mainloop()
