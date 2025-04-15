#!/usr/bin/python3

import json
import math
import sys

fp = open(sys.argv[1], 'r')
steps = int(sys.argv[2])

start = fp.readline()
start = start.rstrip()
stones = start.split()
stones = [int(stone) for stone in stones]

num_stones = len(stones)

faces = dict()
for stone in stones:
	if stone not in faces: faces[stone] = 0
	faces[stone] += 1

seen = dict()
for i in range(steps):
	new = {face:0 for face in seen}
	new = {face:0 for face in faces}
	for stone in faces.keys():
		
		if stone in seen:
			new[seen[stone][0]] += faces[stone]
			new[seen[stone][1]] += faces[stone]
			continue
		else:
			if stone == 0:
				new[1] = faces[stone]

			else:			
				digits = int(math.log10(stone))+1
				half = int(digits / 2)
				if digits % 2 == 0:
					left = int(str(stone)[:half])
					right = int(str(stone)[half:])
					
					seen[stone] = (left, right)
					if left not in new: new[left] = 0
					if right not in new: new[right] = 0
					new[left] += faces[stone]
					new[right] += faces[stone]
							
				else:
					new[stone*2024] = faces[stone]
	faces = new
	pri = {k:v for k,v in new.items() if v > 0}
	counter = 0
	for v in pri.values(): counter += v

counter = 0
for v in pri.values(): counter += v
print(f'Answer after {steps} steps: {counter}')

