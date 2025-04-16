#!/usr/bin/python3

"""

Day 3 Part 2
	* use grep to pre-process the input
		`grep -oE "mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)" input > results.txt`
	* then process results with the following script
		`python3 part2.py results.txt`

"""

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
		