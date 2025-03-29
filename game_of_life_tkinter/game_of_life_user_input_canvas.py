import random
from tkinter import *
import copy
HEIGHT = 100
WIDTH = 100
arcs = []
window = Tk()
C = Canvas(window, bg="blue", height=HEIGHT * 5, width=WIDTH * 5)
colours = ['red', 'blue']
ALIVE = 'X'
DEAD = ' '
evolution_running = False
cells = {}
next_cells = {}
label_names = []
pos = 0
button_frame = Frame(master=window, width=60 * WIDTH, height=60 * HEIGHT)
button_frame.grid(row=1, column=2)

for y in range(HEIGHT):
	for x in range(WIDTH):
		label_names.append(pos)
		pos += 1


def evolution():
	global cells
	global labels
	global running
	global generation
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
				C.itemconfig(arcs[pos], fill="blue")
			# death by underpopulation
			elif cells[(x, y)] == ALIVE and neighbours < 2:
				next_cells[(x, y)] = DEAD
				C.itemconfig(arcs[pos], fill="blue")
			# rebirth of a cell
			elif cells[(x, y)] == DEAD and neighbours == 3:
				next_cells[(x, y)] = ALIVE
				C.itemconfig(arcs[pos], fill="red")
			else:
				if cells[(x, y)] == DEAD:
					next_cells[(x, y)] = DEAD
					C.itemconfig(arcs[pos], fill="blue")
				elif cells[(x, y)] == ALIVE:
					next_cells[(x, y)] = ALIVE
					C.itemconfig(arcs[pos], fill="red")
			pos += 1


def overlapping(event):
	canvas = event.widget
	x = canvas.canvasx(event.x)
	y = canvas.canvasy(event.y)
	overlapping = canvas.find_overlapping(x, y, x, y)
	for item in overlapping:
		if next_cells[label_names[item] % WIDTH, label_names[item]//WIDTH] == DEAD:
			canvas.itemconfigure(item, fill="red")
			next_cells[label_names[item] % WIDTH, label_names[item]//WIDTH] = ALIVE
		else:
			canvas.itemconfigure(item, fill="blue")
			next_cells[label_names[item] % WIDTH, label_names[item] // WIDTH] = DEAD


def start_stop():
	global evolution_running
	if evolution_running:
		evolution_running = False
		start_stop_button.config(text='START')
	else:
		evolution_running = True
		start_stop_button.config(text='STOP')


v = 5
C.bind('<B1-Motion>', overlapping)

for y in range(WIDTH):
	for x in range(HEIGHT):
		arc = C.create_rectangle(x*v, y*v, x*v+5, y*v+5,width=1, fill='blue')
		next_cells[x, y] = DEAD
		arcs.append(arc)


start_stop_button = Button(master=button_frame, height=2, width=12, bg='grey', text='START', command=start_stop)
start_stop_button.grid(row=1, column=1)


C.grid(row=1, column=1)
while True:
	if evolution_running:
		evolution()
	window.update()


