import tkinter as tk

window = tk.Tk()


def label_clicked(event):
	if event.num == 1:
		label.config(bg="black")
	elif event.num == 3:
		label.config(bg="white")


label = tk.Label(master=window, text='X', bg="red", fg="green", width=4, height=2)
label.pack()

while True:
	label.bind('<Button>', label_clicked)
	window.mainloop()
