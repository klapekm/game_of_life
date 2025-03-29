import time, copy
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


WIDTH = 20
HEIGHT = 20

dead_cell_colour = '#000000'
alive_cell_colour = '#0000ff'
alive_cell_colour_RGB = (255, 255, 255)
dead_cell_colour_RGB = (0, 0, 0)

border_colour = '#ff0000'
border_colour_RGB = (255, 0, 0)
cell_border_width = 1

window = tk.Tk()
grid_frame = tk.Frame(master=window, width=500, height=500)
grid_frame.grid(row=1, column=1)
grid_frame.grid_propagate(0)

button_frame = tk.Frame(master=window, width=60 * WIDTH, height=60 * HEIGHT)
button_frame.grid(row=1, column=2)


grid_frame.grid_columnconfigure(list(range(HEIGHT)), weight=3)
grid_frame.grid_rowconfigure(list(range(WIDTH)), weight=3)


labels = []

ALIVE = 'X'
DEAD = ' '

evolution_running = False
program_running = True

cells = {}
next_cells = {}

generation = 0
pos = 0

label_names = []
for y in range(HEIGHT):
	for x in range(WIDTH):
		label_names.append(pos)
		pos += 1


def clicked(event, label_name):
	if event.num == 1:
		if labels[label_name].cget('bg') == alive_cell_colour:
			labels[label_name].config(bg=dead_cell_colour, highlightbackground=border_colour)
			next_cells[(label_names.index(label_name) % WIDTH, label_names.index(label_name) // WIDTH)] = DEAD
		else:
			labels[label_name].config(bg=alive_cell_colour, highlightbackground=border_colour)
			next_cells[(label_names.index(label_name) % WIDTH, label_names.index(label_name) // WIDTH)] = ALIVE


def save_file():
	file = fd.asksaveasfile(mode='w', filetypes=(('text files', '*.txt'), ('All files', '*.*')))
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if next_cells[x, y] == ALIVE:
				file.write('1')
			else:
				file.write('0')
		file.write('\n')
	file.close()


def load_file():
	global labels
	global label_names
	file = fd.askopenfile('r')
	file_lines = file.readlines()
	for item in grid_frame.winfo_children():
		item.destroy()
	pos = 0
	labels.clear()
	label_names.clear()
	for y in range(HEIGHT):
		for x in range(WIDTH):
			label_names.append(pos)
			pos += 1
	pos = 0
	for y in range(HEIGHT):
		for x in range(WIDTH):
			file_line = file_lines[y]
			if file_line[x] == '1':
				labels.append(tk.Label(master=grid_frame, bg=alive_cell_colour, highlightthickness=cell_border_width, highlightcolor=border_colour, highlightbackground=border_colour))
				next_cells[(x, y)] = ALIVE
			elif file_line[x] == '0':
				labels.append(tk.Label(master=grid_frame, bg=dead_cell_colour, highlightthickness=cell_border_width, highlightcolor=border_colour, highlightbackground=border_colour))
				next_cells[(x, y)] = DEAD
			labels[pos].grid(row=y, column=x, sticky='nesw')
			pos += 1
	for i, l in enumerate(labels):
		labels[i].bind('<Button>', lambda event, label_name=i: clicked(event, label_name))
	file.close()


def start_stop():
	global evolution_running
	if evolution_running :
		evolution_running = False
		start_stop_button.config(text='START')
	else:
		evolution_running = True
		start_stop_button.config(text='STOP')


def evolution():
	global cells
	global labels
	global running
	global generation
	if evolution_running:
		generation += 1
		gen_counter.config(text=str(generation))
		cells = copy.deepcopy(next_cells)
		pos = 0
		for y in range(HEIGHT):
			for x in range(WIDTH):
				left = (x - 1) % WIDTH
				right = (x + 1) % WIDTH
				above = (y + 1) % HEIGHT
				below = (y - 1) % HEIGHT
				neighbours = 0
				if cells[(x, above)] == ALIVE:
					neighbours += 1
				if cells[(x, below)] == ALIVE:
					neighbours += 1
				if cells[(left, y)] == ALIVE:
					neighbours += 1
				if cells[(right, y)] == ALIVE:
					neighbours += 1
				if cells[(left, above)] == ALIVE:
					neighbours += 1
				if cells[(right, above)] == ALIVE:
					neighbours += 1
				if cells[(left, below)] == ALIVE:
					neighbours += 1
				if cells[(right, below)] == ALIVE:
					neighbours += 1
				# death by overpopulation
				if cells[(x, y)] == ALIVE and neighbours > 3:
					next_cells[(x, y)] = DEAD
					labels[pos].config(bg=dead_cell_colour, highlightbackground=border_colour)
				# death by underpopulation
				elif cells[(x, y)] == ALIVE and neighbours < 2:
					next_cells[(x, y)] = DEAD
					labels[pos].config(bg=dead_cell_colour, highlightbackground=border_colour)
				# rebirth of a cell
				elif cells[(x, y)] == DEAD and neighbours == 3:
					next_cells[(x, y)] = ALIVE
					labels[pos].config(bg=alive_cell_colour, highlightbackground=border_colour)
				else:
					if cells[(x, y)] == DEAD:
						next_cells[(x, y)] = DEAD
						labels[pos].config(bg=dead_cell_colour, highlightbackground=border_colour)
					elif cells[(x, y)] == ALIVE:
						next_cells[(x, y)] = ALIVE
						labels[pos].config(bg=alive_cell_colour, highlightbackground=border_colour)
				pos += 1


def load_config():
	pos = 0
	for y in range(HEIGHT):
		for x in range(WIDTH):
			labels.append(tk.Label(master=grid_frame, bg=dead_cell_colour, highlightthickness=cell_border_width, highlightbackground=border_colour))
			next_cells[(x, y)] = DEAD
			labels[pos].grid(row=y, column=x, sticky='nesw')
			pos += 1
	for i, l in enumerate(labels):
		labels[i].bind('<Button>', lambda event, label_name=i: clicked(event, label_name))


def on_exit():
	global program_running
	window.destroy()
	window.quit()
	program_running = False


def tup2hex(t1, t2, t3):
	return f'#{t1:02x}{t2:02x}{t3:02x}'


def hex2tup(s):
	return int(s[1:3],base=16),int(s[3:5],base=16),int(s[5:7],base=16)


def new_selected(selection):
	colour_scale_red.set(hex2tup(dropbox_options[selection])[0])
	colour_scale_green.set(hex2tup(dropbox_options[selection])[1])
	colour_scale_blue.set(hex2tup(dropbox_options[selection])[2])


def change_colour(event, colour, selection):
	if not selection == 'Select an option':
		if colour == 'Alive Cells':
			_, t2, t3 = hex2tup(dropbox_options[selection])
			dropbox_options[selection] = tup2hex(int(event), t2, t3)
		if colour == 'Dead Cells':
			t1, _, t3 = hex2tup(dropbox_options[selection])
			dropbox_options[selection] = tup2hex(t1, int(event), t3)
		if colour == 'Border':
			t1, t2, _ = hex2tup(dropbox_options[selection])
			dropbox_options[selection] = tup2hex(t1, t2, int(event))
	else:
		print('SElECT AN OPTION FIRST')


load_config()

colour_changes = ttk.Combobox(master=button_frame, state='readonly', values=['Alive Cells', 'Dead Cells', 'Border'])
colour_changes.grid(row=6, column=1)
colour_changes.bind('<<ComboboxSelected>>', lambda selection:new_selected(selection=colour_changes.get()))

colour_changes.set('Select an option')

colour_scale_red = tk.Scale(master=button_frame, from_=0, to=255, orient='horizontal',
							command=lambda event:change_colour(event=event, colour='Alive Cells', selection=colour_changes.get()))
colour_scale_red.grid(row=3, column=1)

colour_scale_green = tk.Scale(master=button_frame, from_=0, to=255, orient='horizontal',
							  command=lambda event:change_colour(event=event, colour='Dead Cells', selection=colour_changes.get()))
colour_scale_green.grid(row=4, column=1)

colour_scale_blue = tk.Scale(master=button_frame, from_=0, to=255, orient='horizontal',
							 command=lambda event:change_colour(event=event, colour='Border', selection=colour_changes.get()))
colour_scale_blue.grid(row=5, column=1)

dropbox_options = {'Alive Cells': alive_cell_colour, 'Dead Cells': dead_cell_colour, 'Border': border_colour}

start_stop_button = tk.Button(master=button_frame, height=2, width=12, bg='grey', text='START', command=start_stop)
start_stop_button.grid(row=1, column=1)

# clear_button = tk.Button(master=button_frame, height=2, width=12, bg='grey', text='Clear', command=clear_all_cells)
# clear_button.grid(row=1, column=2)

gen_counter = tk.Label(master=button_frame, height=2, width=12, bg='grey', text='0', borderwidth='2', relief='raised')
gen_counter.grid(row=2, column=1)

menubar = tk.Menu(master=window, bg='red')
fileMenu = tk.Menu(master=menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)

fileMenu.add_command(label='Save as', command=save_file)
fileMenu.add_command(label='Open', command=load_file)
fileMenu.add_command(label="Exit", command=on_exit)

window.config(menu=menubar)
window.protocol("WM_DELETE_WINDOW", on_exit)


while program_running:
	alive_cell_colour = dropbox_options['Alive Cells']
	dead_cell_colour = dropbox_options['Dead Cells']
	border_colour = dropbox_options['Border']
	evolution()
	window.update()
	time.sleep(0.1)

