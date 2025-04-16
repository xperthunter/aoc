#!/usr/bin/python3

import sys

kkeys = []
locks = []
with open(sys.argv[1], 'r') as fp:
	counter = 0
	data = [0,0,0,0,0]
	for line in fp.readlines():
		line = line.rstrip()
		if len(line) == 0:
			counter = 0
			continue
		
		counter += 1
		for i,d in enumerate(line):
			if d == '#': data[i] += 1
		
		if counter == 7:
			data = [d-1 for d in data]
			if line == '#####':
				kkeys.append(data)
			else:
				locks.append(data)
			
			data = [0,0,0,0,0]

#print(kkeys)
#print(locks)

matches = 0
for key in kkeys:
	for lock in locks:
		for k,l in zip(key,lock):
			if k+l > 5:
				matches -= 1
				break
		
		matches += 1
				
				
print(f'Part 1: {matches}')				