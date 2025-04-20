#!/usr/bin/python3

"""
Help from this solution:
https://github.com/mgtezak/Advent_of_Code/blob/master/2024/16/p2.py
"""


from heapq import heappop, heappush
import math
import sys

import numpy as np


def find_neighbors(i, j, direction, grid):
	
	if direction == '>':
		if grid[i,j+1] != '#': yield (i,j+1,1,'>')
		if grid[i-1,j] != '#': yield (i,j,1000,'^')
		if grid[i+1,j] != '#': yield (i,j,1000,'v')
	elif direction == '^':
		if grid[i-1,j] != '#': yield (i-1,j,1,'^')
		if grid[i,j+1] != '#': yield (i,j,1000,'>')
		if grid[i,j-1] != '#': yield (i,j,1000,'<')
	elif direction == '<':
		if grid[i,j-1] != '#': yield (i,j-1,1,'<')
		if grid[i+1,j] != '#': yield (i,j,1000,'v')
		if grid[i-1,j] != '#': yield (i,j,1000,'^')
	elif direction == 'v':
		if grid[i+1,j] != '#': yield (i+1,j,1,'v')
		if grid[i,j-1] != '#': yield (i,j,1000,'<')
		if grid[i,j+1] != '#': yield (i,j,1000,'>')
	else:
		print(f'invalid direction {direction}')
		sys.exit()
	


def astar(start, end, grid):
	
	def can_visit(d, i, j, score):
		prev_score = visited.get((d,i,j))
		
		if prev_score and prev_score < score:
			return False
		
		visited[(d,i,j)] = score
		
		return True
	
	visited = {}
	lowest_score = None
	winning_paths = set()
	
	grid[end] = '.'
	
	openset = [(0, '>', start[0], start[1], {start})]
	counter = 0
	while openset:
		current = heappop(openset)
		score, d, i, j, path = current
		
		if lowest_score and lowest_score < score:
			break
		
		if (i, j) == end:
			lowest_score = score
			winning_paths |= path
			counter += 1
			continue
		
		if not can_visit(d, i, j, score):
			continue
		
		for nbr in find_neighbors(i, j, d, grid):
			x, y, weight, new_d = nbr
			if can_visit(new_d, x, y, score+weight):
				if weight == 1000:
					heappush(openset, (score+weight, new_d, i, j, path))
				else:
					heappush(openset, (score+weight, d, x, y, path | {(x,y)}))
	
	print(f'Part 1: {lowest_score}')
	print(f'Part 2: {len(winning_paths)}')
	return

maze = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		
		maze.append(list(line))

maze = np.array(maze)

start = np.where(maze == 'S')
start = (start[0][0], start[1][0])
end   = np.where(maze == 'E')
end   = (end[0][0], end[1][0])

astar(start, end, maze)

