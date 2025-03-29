import tkinter as tk

file = open('game_of_life_settings', 'r')
file_lines = file.readlines()

WIDTH = len(file_lines[0]) - 1
HEIGHT = len(file_lines)

window = tk.Tk()

frame = tk.Frame(master=window, width=40*WIDTH, height=40*HEIGHT)
frame.pack()

label_names = []
labels = []

for i in range(HEIGHT*WIDTH):
	label_names.append('label'+str(i))


def clicked(event, label_name):
	if event.num == 1:
		if labels[label_name].cget('bg') == 'red':
			labels[label_name].config(bg='blue')
		else:
			labels[label_name].config(bg='red')

pos = 0
for y in range(HEIGHT):
	for x in range(WIDTH):
		file_line = file_lines[y]
		if file_line[x] == '1':
			labels.append(tk.Label(master=window, height=5, width=10, bg='red'))
		elif file_line[x] == '0':
			labels.append(tk.Label(master=window, height=5, width=10, bg='blue'))
		labels[pos].place(x=40*x, y=40*y)
		pos += 1
for i, l in enumerate(labels):
	labels[i].bind('<Button>', lambda event, label_name=i: clicked(event, label_name))



window.mainloop()

frame.pack()


