#!/usr/bin/python3

import sys

import numpy as np

def guard_walk(grid):
	guard = np.where((grid == '^') | (grid == '>') | (grid == '<') | (grid == 'v'))
	
	i, j = guard[0][0], guard[1][0]
	start_x, start_y = i, j
	
	seen = dict()
	while True:
		if grid[i,j] == '^':
			obs = np.where(grid[:i,j] == '#')
			if np.shape(obs[0])[0] == 0:
				grid[:i+1,j] = 'X'
				return (grid, True)
			
			if (i+1,j) not in seen:
				seen[(i+1,j)] = dict()
				if (obs[0][-1],j) not in seen[(i+1,j)]:
					seen[(i+1,j)][(obs[0][-1],j)] = True
			else:
				if (obs[0][-1],j) in seen[(i+1,j)]:
					return (grid, False)
			
			if obs[0][-1]+1 == i:
				grid[i,j] = '>'
				continue
			
			grid[obs[0][-1]+1:i,j] = 'X'
			grid[i,j] = 'X'
			
			i = obs[0][-1]+1
			
			grid[i, j] = '>'
			continue
		
		elif grid[i,j] == '>':
			obs = np.where(grid[i,j:] == '#')
			if np.shape(obs[0])[0] == 0:
				grid[i,j:] = 'X'
				return (grid, True)
			
			if (i,j-1) not in seen:
				seen[(i,j-1)] = dict()
				if (i,j+obs[0][0]) not in seen[(i,j-1)]:
					seen[(i,j-1)][(i,j+obs[0][0])] = True
			else:
				if (i,j+obs[0][0]) in seen[(i,j-1)]:
					return (grid, False)			
			
			if obs[0][0] == 1:
				grid[i,j] = 'v'
				continue
			
			grid[i,j:j+obs[0][0]] = 'X'
			grid[i,j] = 'X'
			
			j = j+obs[0][0]-1
			grid[i,j] = 'v'
			continue
		
		elif grid[i, j] == 'v':
			obs = np.where(grid[i:,j] == '#')
			if np.shape(obs[0])[0] == 0:
				grid[i:,j] = 'X'
				return (grid, True)
			
			if (i-1,j) not in seen:
				seen[(i-1,j)] = dict()
				if (i+obs[0][0],j) not in seen[(i-1,j)]:
					seen[(i-1,j)][(i+obs[0][0],j)] = True
			else:
				if (i+obs[0][0],j) in seen[(i-1,j)]:
					return (grid, False)			
			
			if obs[0][0] == 1:
				grid[i, j] = '<'
				continue
			
			grid[i:i+obs[0][0]-1,j] = 'X'
			grid[i,j] = 'X'
			
			i = i+obs[0][0]-1
			grid[i,j] = '<'
			continue
		
		elif grid[i, j] == '<':
			obs = np.where(grid[i,:j] == '#')
			if np.shape(obs[0])[0] == 0:
				grid[i,:j+1] = 'X'
				return (grid, True)
			
			if (i,j+1) not in seen:
				seen[(i,j+1)] = dict()
				if (i,obs[0][-1]) not in seen[(i,j+1)]:
					seen[(i,j+1)][(i,obs[0][-1])] = True
			else:
				if (i,obs[0][-1]) in seen[(i,j+1)]:
					return (grid, False)			
			
			if obs[0][-1]+1 == j:
				grid[i,j] = '^'
				continue
			
			grid[i,obs[0][-1]+1:j] = 'X'
			grid[i,j] = 'X'
			
			j = obs[0][-1]+1
			grid[i,j] = '^'
			continue
		
		else:
			print('problem!')
			sys.exit()

# read input puzzle
with open(sys.argv[1], 'r') as fp:
	grid = []
	for line in fp.readlines():
		line = line.rstrip()
		grid.append(list(line))

grid = np.array(grid)

initial_grid = grid.copy()
guard = np.where((grid == '^') | (grid == '>') | (grid == '<') | (grid == 'v'))
i, j = guard[0][0], guard[1][0]
start_x, start_y = i, j
start_d = grid[guard][0]

# Part 1
grid, status = guard_walk(grid)

xs = np.sum(grid == 'X')
print(f'Part 1: {xs}')

# Part 2
grid[start_x,start_y] = start_d
visited = np.where(grid == 'X')

cycle = 0
for bi,bj in zip(visited[0], visited[1]):
	
	grid = initial_grid.copy()
	
	grid[bi,bj] = '#'
	
	grid, status = guard_walk(grid)
	if not status:
		cycle += 1
	
	grid[start_x,start_y] = start_d
	grid[bi,bj] = '.'
		
print(f'Part 2: {cycle}')