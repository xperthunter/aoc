#!/usr/bin/python3

from heapq import heappop, heappush
import sys

import numpy as np

def a_star(start, end, grid):
	
	def can_visit(i, j, score):
		prev_score = visited.get((i,j))
		
		if prev_score and prev_score < score:
			return False
		
		visited[(i,j)] = score
		
		return True
	
	directions = [(1,0), (0,1), (-1,0), (0,-1)]
	
	visited = {}
	lowest_score = None
	winning_paths = set()
	
	openset = [(0, start[0], start[1], {start})]
	while openset:
		current = heappop(openset)
		score, i, j, path = current
		
		if lowest_score and lowest_score < score:
			break
		
		if (i, j) == end:
			lowest_score = score
			print(len(path)-1)
			return True
			
			winning_paths |= path
			counter += 1
			continue
		
		if not can_visit(i, j, score):
			continue
		
		for d in directions:
			x = i + d[0]
			y = j + d[1]
			
			if x < grid.shape[0] and x >= 0 and y < grid.shape[1] and y >= 0:
				if grid[x,y] != 1:
					h = ((x-end[0])**2 + (y-end[1])**2)**0.5
					if can_visit(x, y, score+1+h):
						heappush(openset, (score+1+h, x, y, path | {(x,y)}))
	
	return False


size = int(sys.argv[2])
with open(sys.argv[1], 'r') as fp:
	ijs = [[],[]]
	for i, line in enumerate(fp.readlines()):
		#if i == size: break
		line = line.rstrip()
		
		xy = line.split(',')
		
		#print(xy[1], xy[0])
		
		ijs[0].append(int(xy[1]))
		ijs[1].append(int(xy[0]))

rows, cols = int(sys.argv[3]), int(sys.argv[4])

grid = np.zeros((rows, cols))
xs = np.array(ijs[0])[:size]
ys = np.array(ijs[1])[:size]

coords = (xs, ys)

grid[coords] = 1

# print()
# for row in grid:
# 	row = [str(int(c)) for c in row]
# 	print(' '.join(row))
# print()

start = (0,0)
end   = (70,70)

print(f'Part 1: {a_star(start, end, grid)}')

### Part 2 ###

searching = True
size = int(1024)
while searching:
	size += 1
	if size > len(ijs[0]):
		print('done')
		sys.exit()
	grid = np.zeros((rows, cols))
	xs = np.array(ijs[0])[:size]
	ys = np.array(ijs[1])[:size]
	
	coords = (xs, ys)
	
	grid[coords] = 1
	
	success = a_star(start, end, grid)
	if not success: searching = False

print(size)
print(f'Part 2: {ijs[1][size-1]}, {ijs[0][size-1]}')


		