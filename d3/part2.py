#!/usr/bin/python3

import sys

do = True
score = 0
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		
		if do and 'mul' in line:
			nums = line[4:-1].split(',')
			score += int(nums[0]) * int(nums[1])
			continue
		
		if 'do()' in line:
			do = True
			continue
		
		if "don't()" in line:
			do = False
			continue

print(score)
		