#!/usr/bin/python3

import json
import math
import sys

import numpy as np

robots = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		info = line.split()
		
		bot = {'pos': [], 'vel': []}
		
		pos = info[0][2:].split(',')
		pos = [int(p) for p in pos]
		
		vel = info[1][2:].split(',')
		vel = [int(v) for v in vel]
		
		bot['pos'] = pos
		bot['vel'] = vel
		
		robots.append(bot)

"""
# Part 1
width  = int(sys.argv[2])
height = int(sys.argv[3])
grid = [['.']*height for i in range(width)]
grid = np.array(grid)
steps  = int(sys.argv[4])
for step in range(steps):
	grid = [['.']*height for i in range(width)]
	grid = np.array(grid)
	
	
	for bot in robots:
		bot['pos'][0] = bot['pos'][0]+bot['vel'][0]
		bot['pos'][1] = bot['pos'][1]+bot['vel'][1]
		
		if bot['pos'][0] < 0:
			bot['pos'][0] = width + bot['pos'][0]
		else:
			bot['pos'][0] = bot['pos'][0] % width
		
		if bot['pos'][1] < 0:
			bot['pos'][1] = height + bot['pos'][1]
		else:
			bot['pos'][1] = bot['pos'][1] % height
		
		grid[bot['pos'][0],bot['pos'][1]] = 1
	
	print()
	print(f'step: {step}')
	for row in grid: print(''.join(row))
	print()
	
	
	
#sys.exit()
q1 = 0
q2 = 0
q3 = 0
q4 = 0


hw = math.floor(width / 2)
hh = math.floor(height / 2)

print(hw, hh)

for bot in robots:
	if bot['pos'][0] < hw:
		if bot['pos'][1] < hh:
			q1 += 1
		elif bot['pos'][1] > hh:
			q2 += 1
		else:
			pass
	elif bot['pos'][0] > hw:
		if bot['pos'][1] < hh:
			q3 += 1
		elif bot['pos'][1] > hh:
			q4 += 1
		else:
			pass
	else:
		pass

print(q1, q2, q3, q4)

print(f'score: {q1*q2*q3*q4}')
"""

# Part 2
width  = int(sys.argv[2])
height = int(sys.argv[3])
grid = [['.']*width for i in range(height)]
grid = np.array(grid)

stretch = int(sys.argv[4])
steps  = int(sys.argv[5])
for step in range(steps):
	grid = [['.']*width for i in range(height)]
	grid = np.array(grid)
	for bot in robots:
		#print(bot['pos'])
		bot['pos'][0] = bot['pos'][0]+bot['vel'][0]
		bot['pos'][1] = bot['pos'][1]+bot['vel'][1]
		
		if bot['pos'][0] < 0:
			bot['pos'][0] = width + bot['pos'][0]
		else:
			bot['pos'][0] = bot['pos'][0] % width
		
		if bot['pos'][1] < 0:
			bot['pos'][1] = height + bot['pos'][1]
		else:
			bot['pos'][1] = bot['pos'][1] % height
		
		#print(bot['pos'])
		grid[bot['pos'][1],bot['pos'][0]] = 1
	
	for bot in robots:
		i,j = bot['pos']
		cont = True
		for k in range(1,stretch):
			try:
				if grid[i+k][j] == '.':
					cont = False
					break
				else:
					continue
			except:
				cont = False
				break
		
		if cont:
			print()
			print(f'step: {step+1}')
			for row in grid: print(''.join(row))
			print()
			break


