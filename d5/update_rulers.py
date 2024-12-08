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

# for k1 in rules.keys():
# 	for k2 in rules[k1].keys():
# 		print(k1,k2)


mids = 0
for orders in pages:
	correct = True
	for i, pg in enumerate(orders):
		#if pg not in rules: continue
		
		for j in range(i+1, len(orders)):
			if orders[j] in rules:
				if pg in rules[orders[j]]:
					correct = False
					break
		
		if not correct: break
	if correct:
		print(orders[int((len(orders)-1)/2)])
		mids += int(orders[int((len(orders)-1)/2)])

print(mids)