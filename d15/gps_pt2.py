#!/usr/bin/python3

import json
import sys

import numpy as np


def move_up_down(root, g, k):
	
	tree = dict()
	leaves = [root]
	up = True
	while up:
		dels = []
		for ii, leaf in enumerate(leaves.copy()):
			i,j = leaf
			dels.append(ii)
			if g[i+k,j] == '#':
				tree = dict()
				up = False
				break
			elif g[i+k,j] == '.':
				tree[(i,j)] = (i+k,j)
				
			else:
				tree[(i,j)] = (i+k,j)
				if g[i+k,j] == '[':
					leaves.append((i+k,j))
					leaves.append((i+k,j+1))
				else:
					leaves.append((i+k,j))
					leaves.append((i+k,j-1))
		
		leaves = [leaf for i,leaf in enumerate(leaves) if i not in dels]
		if len(leaves) == 0: up = False
	
	if len(list(tree.keys())) == 0: return g
	if k == 1: sending = True
	else:      sending = False
	for k,v in sorted(tree.items(), key=lambda x: x[0][0], reverse=sending):
		g[v] = g[k]
		g[k] = '.'
	
	return g

def move_right(node=None, g=None):
	i,j = node
	
	if g[i,j+1] == '.':
		g[i,j+1] = '@'
		g[i,j]   = '.'
		
		return g
	elif g[i,j+1] == '[' or g[i,j+1] == ']':
		spaces = np.where(g[i,:] == '.')[0]
		spaces = spaces[spaces > j]
			
		if spaces.shape[0] > 0:
			walls = np.where(g[i,:] == '#')[0]
			walls = walls[walls > j]
			assert(walls.shape[0] > 0)
			
			wall_min = np.min(walls)
			spaces = spaces[spaces < wall_min]
			
			if spaces.shape[0] > 0:
				min_id = np.min(spaces)
				g[i,j+1:min_id+1] = g[i,j:min_id]
				g[i,j] = '.'
				
				return g
	else:
		return g
	
	return g

def move_left(node=None, g=None):
	i,j = node
	
	if g[i,j-1] == '.':
		g[i,j-1] = '@'
		g[i,j]   = '.'
		
		return g
	elif g[i,j-1] == '[' or g[i,j-1] == ']':
		spaces = np.where(g[i,:] == '.')[0]
		spaces = spaces[spaces < j]
		
		if spaces.shape[0] > 0:
			walls = np.where(g[i,:] == '#')[0]
			walls = walls[walls < j]
			assert(walls.shape[0] > 0)
			
			wall_max = np.max(walls)
			spaces = spaces[spaces > wall_max]
			
			if spaces.shape[0] > 0:
				max_id = np.max(spaces)
				g[i,max_id:j] = g[i,max_id+1:j+1]
				g[i,j] = '.'
				
				return g
	else:
		return g
	
	return g
		
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

grid_pt2 = []
for row in grid:
	line = []
	for elm in row:
		if elm == '#':
			line.append('#')
			line.append('#')
		elif elm == 'O':
			line.append('[')
			line.append(']')
		elif elm == '@':
			line.append('@')
			line.append('.')
		else:
			line.append('.')
			line.append('.')
	grid_pt2.append(line)

gp2 = np.array(grid_pt2)

print()
for row in gp2: print(''.join(row))
print()

bot = np.where(gp2 == '@')
bot = (bot[0][0], bot[1][0])

for move in moves:
	print(f'bot: {bot} move: {move}')
	if move == '^':
		gp2 = move_up_down(bot, gp2, -1)
		bot = np.where(gp2 == '@')
		bot = (bot[0][0], bot[1][0])
	elif move == 'v':
		gp2 = move_up_down(bot, gp2, 1)
		bot = np.where(gp2 == '@')
		bot = (bot[0][0], bot[1][0])
	elif move == '>':
		gp2 = move_right(node=bot, g=gp2)
		bot = np.where(gp2 == '@')
		bot = (bot[0][0], bot[1][0])
	elif move == '<':
		gp2 = move_left(node=bot, g=gp2)
		bot = np.where(gp2 == '@')
		bot = (bot[0][0], bot[1][0])
	
	print()
	for row in gp2: print(''.join(row))
	print()
	
boxes = np.where(gp2 == '[')
score = np.sum(boxes[0]*100) + np.sum(boxes[1])

print(f'score: {score}')	
