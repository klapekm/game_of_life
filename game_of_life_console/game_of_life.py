import time, copy

file = open('game_of_life_settings', 'r')

file_lines = file.readlines()

WIDTH = len(file_lines[0])-1
HEIGHT = len(file_lines)

ALIVE = 'X'
DEAD = ' '

cells = {}
next_cells = {}

for y in range(HEIGHT):
	for x in range(WIDTH):
		file_line =	file_lines[y]
		if file_line[x] == '1':
			next_cells[(x, y)] = ALIVE

		if file_line[x] == '0':
			next_cells[(x, y)] = DEAD

file.close()
while True:
	cells = copy.deepcopy(next_cells)
	for y in range(HEIGHT):
		for x in range(WIDTH):
			print(cells[x, y], end='')
		print()
	time.sleep(0.3)
	print('\n' * 10)

	for x in range(WIDTH):
		for y in range(HEIGHT):
			left = (x-1) % WIDTH
			right = (x+1) % WIDTH
			above = (y+1) % HEIGHT
			below = (y-1) % HEIGHT
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

			if cells[(x, y)] == ALIVE and (neighbours == 2 or neighbours == 3):
				next_cells[(x, y)] = ALIVE
			elif cells[(x, y)] == DEAD and neighbours == 3:
				next_cells[(x, y)] = ALIVE
			else:
				next_cells[(x, y)] = DEAD
