#!/usr/bin/python3

import sys

import numpy as np

def guard_walk(grid):
	guard = np.where((grid == '^') | (grid == '>') | (grid == '<') | (grid == 'v'))
	
	i, j = guard[0][0], guard[1][0]
	start_x, start_y = i, j
	
	seen = dict()
	while True:
		#print('iter')
		#for row in grid: print(''.join(row))
		#print()
		if grid[i,j] == '^':
			#print('^')
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
			
# 			if (obs[0][-1],j) in seen:
# 				return (grid, False)
# 			else:
# 				seen[(obs[0][-1],j)] = True
			
			
			if obs[0][-1]+1 == i:
				grid[i,j] = '>'
				continue
			
# 			spot = grid[obs[0][-1],j]
# 			if spot == 'X':
# 				return (grid, False)
			
# 			unvisited = np.where(grid[obs[0][-1]:i,j] == '.')
# 			if np.shape(unvisited[0])[0] == 0:
# 				return (grid, False)
			
			grid[obs[0][-1]+1:i,j] = 'X'
			grid[i,j] = 'X'
			
			i = obs[0][-1]+1
			
			grid[i, j] = '>'
# 			if i == start_x and j == start_y:
# 				return (grid, False)
			
			continue
		
		elif grid[i,j] == '>':
			#print('>')
			obs = np.where(grid[i,j:] == '#')
			#print(obs)
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
			
			
				
			
# 			if (i,j+obs[0][0]) in seen: return (grid, False)
# 			else: seen[(i,j+obs[0][0])] = True
			
			if obs[0][0] == 1:
				grid[i,j] = 'v'
				continue
			
# 			spot = grid[i,j+obs[0][0]]
# 			if spot == 'X':
# 				return (grid, False)
			
# 			#print(obs[0][0])
# 			unvisited = np.where(grid[i,j:j+obs[0][0]] == '.')
# 			#print(unvisited)
# 			if np.shape(unvisited[0])[0] == 0:
# 				return (grid, False)
			
			grid[i,j:j+obs[0][0]] = 'X'
			grid[i,j] = 'X'
			
			j = j+obs[0][0]-1
			grid[i,j] = 'v'
			
# 			if i == start_x and j == start_y:
# 				return (grid, False)
			
			continue
		
		elif grid[i, j] == 'v':
			#print('v')
			obs = np.where(grid[i:,j] == '#')
			#print(obs)
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
			
			
# 			if (i+obs[0][0],j) in seen: return (grid, False)
# 			else: seen[(i+obs[0][0],j)] = True
			
			if obs[0][0] == 1:
				grid[i, j] = '<'
				continue
			
# 			spot = grid[i+obs[0][0],j]
# 			if spot == 'X':
# 				return (grid, False)
# 			
# 			unvisited = np.where(grid[i:i+obs[0][0],j] == '.')
# 			#print(unvisited)
# 			#print(grid[i:i+obs[0][0]-1])
# 			if np.shape(unvisited[0])[0] == 0:
# 				return (grid, False)
			
			grid[i:i+obs[0][0]-1,j] = 'X'
			grid[i,j] = 'X'
			
			i = i+obs[0][0]-1
			grid[i,j] = '<'
			
# 			if i == start_x and j == start_y:
# 				return (grid, False)
			
			continue
		
		elif grid[i, j] == '<':
			#print('<')
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
			
			
# 			if (i,obs[0][-1]) in seen: return (grid, False)
# 			else: seen[(i,obs[0][-1])] = True
			
			
			if obs[0][-1]+1 == j:
				grid[i,j] = '^'
				continue
			
# 			spot = grid[i,obs[0][-1]]
# 			if spot == 'X':
# 				return (grid, False)
			
# 			unvisited = np.where(grid[i,obs[0][-1]:j] == '.')
# 			if np.shape(unvisited[0])[0] == 0:
# 				return (grid, False)
			
			grid[i,obs[0][-1]+1:j] = 'X'
			grid[i,j] = 'X'
			
			j = obs[0][-1]+1
			grid[i,j] = '^'
			
# 			if i == start_x and j == start_y:
# 				return (grid, False)
			
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
print()
for row in grid: print(''.join(row))
print()
grid = np.array(grid)

initial_grid = grid.copy()
guard = np.where((grid == '^') | (grid == '>') | (grid == '<') | (grid == 'v'))
i, j = guard[0][0], guard[1][0]
start_x, start_y = i, j
start_d = grid[guard][0]

grid, status = guard_walk(grid)

print()
for row in grid:
	print(''.join(row))
print()
xs = np.sum(grid == 'X')
print(xs)
#sys.exit()
grid[start_x,start_y] = start_d

visited = np.where(grid == 'X')

cycle = 0
for bi,bj in zip(visited[0], visited[1]):
	
	print(bi,bj)
	grid = initial_grid.copy()
	
	grid[bi,bj] = '#'
	#print('start')
	#for row in grid: print(''.join(row))
	#print()
	
	grid, status = guard_walk(grid)
	if not status:
		cycle += 1
		print()
		print('cycle')
		for row in grid:
			print(''.join(row))
		print(cycle)
		print()
		#sys.exit()
			
		#sys.exit()
	
	grid[start_x,start_y] = start_d
	grid[bi,bj] = '.'
		
print(cycle)

"""

moving = True
while moving:
	
	if grid[i,j] == '^':
		obs = np.where(grid[:i,j] == '#')
		if np.shape(obs[0])[0] == 0:
			grid[:i+1,j] = 'X'
			moving = False
			print(grid[:,j])
			print('^')
			continue
		print(obs)
		print(obs[0][-1])
		print(obs[0][0])
		grid[obs[0][-1]+1:i,j] = 'X'
		grid[i,j] = 'X'
		
		i = obs[0][-1]+1
		grid[i, j] = '>'
		#print(grid)
		for row in grid:
			print(''.join(row))
		print(i,j)
		continue
	
	elif grid[i,j] == '>':
		obs = np.where(grid[i,j:] == '#')
		print(obs)
		if np.shape(obs[0])[0] == 0:
			moving = False
			grid[i,j:] = 'X'
			print(grid[i,:])
			print('>')
			continue
		grid[i,j:j+obs[0][0]] = 'X'
		grid[i,j] = 'X'
		
		j = j+obs[0][0]-1
		grid[i,j] = 'v'
		#print(grid)
		for row in grid:
			print(''.join(row))
		print(i,j)
		continue
	
	elif grid[i, j] == 'v':
		obs = np.where(grid[i:,j] == '#')
		if np.shape(obs[0])[0] == 0:
			moving = False
			grid[i:,j] = 'X'
			print(grid[:,j])
			print('v')
			continue
		
		grid[i:i+obs[0][0]-1,j] = 'X'
		grid[i,j] = 'X'
		
		i = i+obs[0][0]-1
		grid[i,j] = '<'
		#print(grid)
		for row in grid:
			print(''.join(row))
		print(i,j)
		continue
	
	elif grid[i, j] == '<':
		obs = np.where(grid[i,:j] == '#')
		if np.shape(obs[0])[0] == 0:
			moving = False
			grid[i,:j+1] = 'X'
			print(grid[i,:])
			print('<')
			continue
		print(obs)
		grid[i,obs[0][-1]+1:j] = 'X'
		grid[i,j] = 'X'
		
		j = obs[0][-1]+1
		grid[i,j] = '^'
		#print(grid)
		for row in grid:
			print(''.join(row))
		print(i,j)
		continue
"""	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
