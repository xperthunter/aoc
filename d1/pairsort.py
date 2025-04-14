#!/usr/bin/python3

import sys

with open(sys.argv[1], 'r') as fp:
	list_1 = []
	list2 = []
	list_2 = {}
	
	for line in fp.readlines():
		line = line.rstrip()
		
		line = line.split()
		
		list_1.append(int(line[0]))
		
		l2 = int(line[1])
		
		# Part 1
		list2.append(int(line[1]))
		
		# Part 2
		if l2 not in list_2: list_2[l2] = 0
		list_2[l2] += 1


# Part 1
list_1 = sorted(list_1, reverse=False)
list2  = sorted(list2, reverse=False)

distance = 0
for l1, l2 in zip(list_1, list2):
	distance += abs(l1 - l2)

print(f'Part 1: {distance}')

# Part 2
score = 0
for num in list_1:
	if num in list_2: score += num*list_2[num]

print(f'Part 2: {score}')