#!/usr/bin/python3

import json
import sys

import numpy as np

grid  = []
moves = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		
		if '#' in line:
			grid.append(list(line))
		elif len(line) == 0:
			continue
		else:
			moves = moves + list(line)
			continue

grid = np.array(grid)
bot = np.where(grid == '@')
bot = (bot[0][0], bot[1][0])

print()
for row in grid: print(''.join(row))
print()


for move in moves:
	if move == '<':
		i, j = bot
		if grid[i,j-1] == '.':
			bot = (i, j-1)
			grid[bot] = '@'
			grid[i,j] = '.'
		elif grid[i,j-1] == 'O':
			spaces = np.where(grid[i,:] == '.')[0]
			spaces = spaces[spaces < j]
			
			if spaces.shape[0] > 0:
				walls = np.where(grid[i,:] == '#')[0]
				walls = walls[walls < j]
				assert(walls.shape[0] > 0)
				
				wall_max = np.max(walls)
				spaces = spaces[spaces > wall_max]
				
				if spaces.shape[0] > 0:
					max_id = np.max(spaces)
					grid[i,max_id:j] = grid[i,max_id+1:j+1]
					grid[i,j] = '.'
					bot = (i, j-1)
	elif move == '>':
		i, j = bot
		if grid[i,j+1] == '.':
			bot = (i, j+1)
			grid[bot] = '@'
			grid[i,j] = '.'
		elif grid[i,j+1] == 'O':
			spaces = np.where(grid[i,:] == '.')[0]
			spaces = spaces[spaces > j]
			
			if spaces.shape[0] > 0:
				walls = np.where(grid[i,:] == '#')[0]
				walls = walls[walls > j]
				assert(walls.shape[0] > 0)
				
				wall_min = np.min(walls)
				spaces = spaces[spaces < wall_min]
				
				if spaces.shape[0] > 0:
					min_id = np.min(spaces)
					grid[i,j+1:min_id+1] = grid[i,j:min_id]
					grid[i,j] = '.'
					bot = (i,j+1)
	elif move == '^':
		i, j = bot
		if grid[i-1,j] == '.':
			bot = (i-1, j)
			grid[bot] = '@'
			grid[i,j] = '.'
		elif grid[i-1,j] == 'O':
			spaces = np.where(grid[:,j] == '.')[0]
			spaces = spaces[spaces < i]
			
			if spaces.shape[0] > 0:
				walls = np.where(grid[:,j] == '#')[0]
				walls = walls[walls < i]
				assert(walls.shape[0] > 0)
				
				wall_max = np.max(walls)
				spaces = spaces[spaces > wall_max]
				
				if spaces.shape[0] > 0:
					max_id = np.max(spaces)
					grid[max_id:i,j] = grid[max_id+1:i+1,j]
					grid[i,j] = '.'
					bot = (i-1,j)
	elif move == 'v':
		i, j = bot
		if grid[i+1,j] == '.':
			bot = (i+1, j)
			grid[bot] = '@'
			grid[i,j] = '.'
		elif grid[i+1,j] == 'O':
			spaces = np.where(grid[:,j] == '.')[0]
			spaces = spaces[spaces > i]
			
			if spaces.shape[0] > 0:
				walls = np.where(grid[:,j] == '#')[0]
				walls = walls[walls > i]
				assert(walls.shape[0] > 0)
				
				wall_min = np.min(walls)
				spaces = spaces[spaces < wall_min]
				
				if spaces.shape[0] > 0:
					min_id = np.min(spaces)
					grid[i+1:min_id+1,j] = grid[i:min_id,j]
					grid[i,j] = '.'
					bot = (i+1,j)
	else:
		print('unknown move')
		sys.exit()
	
	print()
	for row in grid: print(''.join(row))
	print()

boxes = np.where(grid == 'O')
score = np.sum(boxes[0]*100) + np.sum(boxes[1])

print(f'score: {score}')
