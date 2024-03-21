from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, RIGHT, Y, Scrollbar


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry(f"{round(1434*0.8)}x{round(948*0.8)}")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=948*0.8,
    width=1434*0.8,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    32.0*0.8,
    115.0*0.8,
    994.0*0.8,
    755.0*0.8,
    fill="#D9D9D9",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1_8.png"))
image_1 = canvas.create_image(
    493.0*0.8,
    432.0*0.8,
    image=image_image_1
)

rd_tb = canvas.create_text(
    389.0*0.8,
    238.0*0.8,
    anchor="nw",
    text="RD TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

rr1_tb = canvas.create_text(
    286.0*0.8,
    456.0*0.8,
    anchor="nw",
    text="RR1 TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

rr2_tb = canvas.create_text(
    286.0*0.8,
    498.0*0.8,
    anchor="nw",
    text="RR2 TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

rr3_tb = canvas.create_text(
    286.0*0.8,
    561.0*0.8,
    anchor="nw",
    text="RR3 TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

tb_15_0 = canvas.create_text(
    260.0*0.8,
    658.0*0.8,
    anchor="nw",
    text="15-0 TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

rd2_tb = canvas.create_text(
    597.0*0.8,
    591.0*0.8,
    anchor="nw",
    text="RD2 TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

wd_tb = canvas.create_text(
    784.0*0.8,
    727.0*0.8,
    anchor="nw",
    text="Write Data TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

rd1_tb = canvas.create_text(
    555.0*0.8,
    459.0*0.8,
    anchor="nw",
    text="RD1 TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

rw_tb = canvas.create_text(
    471.0*0.8,
    420.0*0.8,
    anchor="nw",
    text="RW TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

j_tb = canvas.create_text(
    510.0*0.8,
    279.0*0.8,
    anchor="nw",
    text="J TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

b_tb = canvas.create_text(
    505.0*0.8,
    298.0*0.8,
    anchor="nw",
    text="B TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

mr_tb = canvas.create_text(
    513.0*0.8,
    315.0*0.8,
    anchor="nw",
    text="MR TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

mtr_tb = canvas.create_text(
    513.0*0.8,
    332.0*0.8,
    anchor="nw",
    text="MtR TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

aluo_tb = canvas.create_text(
    494.0*0.8,
    351.0*0.8,
    anchor="nw",
    text="ALUO TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

mw_tb = canvas.create_text(
    597.0*0.8,
    365.0*0.8,
    anchor="nw",
    text="MW TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

alus_tb = canvas.create_text(
    588.0*0.8,
    415.0*0.8,
    anchor="nw",
    text="ALUS TB",
    fill="#000000",
    font=("Inter", 14 * -1)
)

canvas.create_rectangle(
    999.0*0.8,
    115.0*0.8,
    1416.0*0.8,
    941.0*0.8,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    32.0*0.8,
    760.0*0.8,
    994.0*0.8,
    941.0*0.8,
    fill="#D9D9D9",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1_8.png"))
entry_bg_1 = canvas.create_image(
    757.0*0.8,
    850.0*0.8,
    image=entry_image_1
)

kernel_input = entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=588.0*0.8,
    y=767.0*0.8,
    width=338.0*0.8,
    height=164.0*0.8
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2_8.png"))
entry_bg_2 = canvas.create_image(
    304.5*0.8,
    851.5*0.8,
    image=entry_image_2
)


def scroll_kernel_output(*args):
    kernel_output.yview(*args)


# Create the Scrollbar widget
scrollbar = Scrollbar(command=scroll_kernel_output)

kernel_output = entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=40.0*0.8,
    y=770.0*0.8,
    width=529.0*0.8,
    height=161.0*0.8
)

# Link the Text widget with the Scrollbar
kernel_output.config(yscrollcommand=scrollbar.set)

# Pack the widgets
scrollbar.place(x=569.0*0.8, y=770.0*0.8, height=161.0*0.8)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.create_rectangle(
    528.0*0.8,
    32.0*0.8,
    866.0*0.8,
    87.0*0.8,
    fill="#D9D9D9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1_8.png"))
play_button = button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=597.0*0.8,
    y=39.0*0.8,
    width=40.0*0.8,
    height=40.0*0.8
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2_8.png"))
play_one_step_button = button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=737.4000244140625*0.8,
    y=39.0*0.8,
    width=40.0*0.8,
    height=40.0*0.8
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3_8.png"))
input_text = button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=938.0*0.8,
    y=831.0*0.8,
    width=40.0*0.8,
    height=40.0*0.8
)


a, b = 115.0, 132.0
registers = []  # [name, number, value]
y = 117.0

l = [
    "$zero",
    "$at",
    "$v0",
    "$v1",
    "$a0",
    "$a1",
    "$a2",
    "$a3",
    "$t0",
    "$t1",
    "$t2",
    "$t3",
    "$t4",
    "$t5",
    "$t6",
    "$t7",
    "$s0",
    "$s1",
    "$s2",
    "$s3",
    "$s4",
    "$s5",
    "$s6",
    "$s7",
    "$t8",
    "$t9",
    "$k0",
    "$k1",
    "$gp",
    "$sp",
    "$fp",
    "$ra",
    "pc",
    "hi",
    "lo"
]

for i in range(0, 36):

    canvas.create_rectangle(
        1275.0*0.8,
        a*0.8,
        1416.0*0.8,
        b*0.8,
        fill="#A3A3A3",
        outline="")

    canvas.create_rectangle(
        999.0*0.8,
        a*0.8,
        1138.0*0.8,
        b*0.8,
        fill="#A3A3A3",
        outline="")

    canvas.create_rectangle(
        1137.0*0.8,
        a*0.8,
        1276.0*0.8,
        b*0.8,
        fill="#A3A3A3",
        outline="")

    registers.append([canvas.create_text(
        1054.5*0.8,
        y*0.8,
        anchor="nw",
        text=f"{l[i - 1]}" if i > 0 else "",
        fill="#000000",
        font=("Inter", 10 * -1)
    ),

        canvas.create_text(
        1188.5*0.8,
        y*0.8,
        anchor="nw",
        text=f"{i - 1}" if i < 33 else "",
        fill="#000000",
        font=("Inter", 10 * -1)
    ),

        canvas.create_text(
        1331.5*0.8,
        y*0.8,
        anchor="nw",
        text="0",
        fill="#000000",
        font=("Inter", 10 * -1)
    )])
    y += (133.0 - 117.0)

    a += 131.0-115.0
    b += 148.0-132.0

canvas.itemconfig(registers[0][1], text="Number")
canvas.itemconfig(registers[0][0], text="Name")
canvas.itemconfig(registers[0][2], text="value")