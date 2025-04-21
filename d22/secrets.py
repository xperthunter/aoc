#!/usr/bin/python3

import sys

with open(sys.argv[1], 'r') as fp:
	inputs = fp.readlines()
	inputs = [int(ii.rstrip()) for ii in inputs]


cache = dict()

def evolve(num):
	
	if num in cache:
		return cache[num]
	
	start = num
	temp = num * 64
	num = temp ^ num
	
	num = num % 16777216
	
	temp = num // 32
	num = temp ^ num
	
	num = num % 16777216
	
	temp = num * 2048
	num = temp ^ num
	
	num = num % 16777216
	
	cache[start] = num
	
	return num

score = 0
part1 = 0
total_diffs = dict()
for buyer, beg in enumerate(inputs):
	last_four = [None, None, None, None]
	diffs = dict()
	for i in range(2000):
		new = evolve(beg)
		
		diff = (new % 10) - (beg % 10)
		last_four = last_four[1:]
		last_four.append(diff)
		if None not in last_four:
			four_key = tuple(last_four)
			if four_key in diffs:
				diffs[four_key] = max(diffs[four_key], new % 10)
			else:
				diffs[four_key] = new % 10
		beg = new
	
	for k,v in diffs.items():
		if k not in total_diffs:
			total_diffs[k] = v
		else:
			total_diffs[k] += v
	
	part1 += beg

most_bananas = list(sorted(total_diffs.values()))[-1]

print(f'Part 1: {part1}')
print(f'Part 2: {most_bananas}')	


	
	