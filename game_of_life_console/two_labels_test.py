import tkinter as tk

window = tk.Tk()


def clicked(event, label_name):
	if event.num == 1:
		if labels[label_name].cget('bg') == 'yellow':
			labels[label_name].config(bg='blue')
		else:
			labels[label_name].config(bg='yellow')


labels = list()
labels.append(tk.Label(master=window, height=5, width=10, bg='black'))
labels.append(tk.Label(master=window, height=5, width=10, bg='blue'))
labels.append(tk.Label(master=window, height=5, width=10, bg='red'))



# for i, l in enumerate(labels):
# 	# print(i,l)
# 	l.bind('<Button>', lambda event: clicked(event, i),add="+")


for i, l in enumerate(labels):
	labels[i].bind('<Button>', lambda event, label_name=i: clicked(event, label_name))

# i=1
# labels[i].bind('<Button>', lambda event, i=1: clicked(event, i))


labels[0].pack()
labels[1].pack()
labels[2].pack()

window.mainloop()
