import tkinter as tk


def update_text():
    canvas.itemconfig(text_id, text="New Text")


root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=100)
canvas.pack()

# Initial text on canvas
text_id = canvas.create_text(
    100, 50, text="Original Text", font=("Helvetica", 12))

# Button to update text
update_button = tk.Button(root, text="Update Text", command=update_text)
update_button.pack()

root.mainloop()
