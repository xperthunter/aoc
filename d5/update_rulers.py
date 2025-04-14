#!/usr/bin/python3

import sys

# read in the rules and page orderings
with open(sys.argv[1], 'r') as fp:
	rules = dict()
	pages = list()
	
	for line in fp.readlines():
		line = line.rstrip()
		if '|' in line:
			rule = line.split('|')
			if rule[0] not in rules: rules[rule[0]] = dict()
			rules[rule[0]][rule[1]] = True
		if ',' in line:
			order = line.split(',')
			pages.append(order)

# Part 1
mids = 0
incorrects = list()
for orders in pages:
	correct = True
	for i, pg in enumerate(orders):
		for j in range(i+1, len(orders)):
			if orders[j] in rules:
				if pg in rules[orders[j]]:
					correct = False
					break
		
		if not correct: break
	if correct:
		mids += int(orders[int((len(orders)-1)/2)])
	else:
		incorrects.append(orders)

print(f'Part 1: mids')

# Part 2
mids = 0
while len(incorrects) > 0:
	for ii, inc in enumerate(incorrects):
		correct = True
		for i, pg in enumerate(inc):
			for j in range(i+1, len(inc)):
				if inc[j] in rules:
					if pg in rules[inc[j]]:
						incorrects[ii][i], incorrects[ii][j] = incorrects[ii][j], incorrects[ii][i]
						correct = False
						break
			
			if not correct: break
		if correct:
			mids += int(inc[int((len(inc)-1)/2)])
			del incorrects[ii]

print(f'Part 2: {mids}')
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					