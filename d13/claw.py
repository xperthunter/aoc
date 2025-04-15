#!/usr/bin/python3

import sys

import numpy as np
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

offset = int(sys.argv[2])

with open(sys.argv[1], 'r') as fp:
	problems = []
	
	for line in fp.readlines():
		line = line.rstrip()
		
		if 'Button A' in line:
			problem = [[], [], []]
			parts = line.split(':')
			moves = parts[1].split(',')
			xmove = int(moves[0].split('+')[1])
			ymove = int(moves[1].split('+')[1])
			problem[0].append(xmove)
			problem[1].append(ymove)
		elif 'Button B' in line:
			parts = line.split(':')
			moves = parts[1].split(',')
			xmove = int(moves[0].split('+')[1])
			ymove = int(moves[1].split('+')[1])
			problem[0].append(xmove)
			problem[1].append(ymove)
		elif 'Prize' in line:
			parts = line.split(':')
			coords = parts[1].split(',')
			xcoord = int(coords[0].split('=')[1])+offset
			ycoord = int(coords[1].split('=')[1])+offset
			problem[2].append(xcoord)
			problem[2].append(ycoord)
			
			problems.append(problem)
			
		else:
			problem = [[], [], []]
			continue

button_cost = np.array([[3.], [1.]])
total_cost = 0
for problem in problems:
	
	A = [problem[0], problem[1]]
	A = np.array(A)
	b = np.array(problem[2])
	b = np.transpose(b)
	
	x = np.matmul(np.linalg.inv(A), b)
	
	x_int = np.rint(x)
	
	if np.allclose(x_int, x, rtol=0, atol=1e-4):
		cost = np.matmul(x_int, button_cost)
		total_cost += cost
	
print(f'total cost: {int(total_cost[0])}')