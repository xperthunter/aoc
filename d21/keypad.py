#!/usr/bin/python3

import faulthandler
from functools import lru_cache
from heapq import heappop, heappush
import itertools
import json
import sys

import numpy as np

sys.setrecursionlimit(int(1e5))
faulthandler.enable()

numeric_keypad = [['7','8','9'],['4','5','6'],['1','2','3'],['gap','0','A']]
numeric_keypad = np.array(numeric_keypad)
dir_keypad = [['gap','^','A'],['<','v','>']]
dir_keypad = np.array(dir_keypad)
cache = dict()


def score_code(code):
	prev = None
	score = 0
	
	for i in range(0,len(code)-1):
		if code[i+1] != code[i]:
			score += 1
		else:
			score -= 1
		
	return score


def search(beg, end, pad):
	directions = [(1,0), (0,1), (-1,0), (0,-1)]
	symbols    = ['v','>','^','<']
	lowest_score = None
	openset = [(0, beg[0], beg[1], [pad[beg]], [])]
	while openset:
		current = heappop(openset)
		score, i, j, path, dirs = current
		
		if lowest_score and lowest_score < score:
			return
		
		if (i, j) == end:
			lowest_score = score
			return (''.join(path), dirs+['A'])
		
		for d,s in zip(directions,symbols):
			x = i + d[0]
			y = j + d[1]
			
			if x < pad.shape[0] and x >= 0 and y < pad.shape[1] and y >= 0:
				if pad[x,y] != 'gap':
					new_path = path + [pad[x,y]]
					new_dirs = dirs + [s]
					if len(dirs) > 0:
						if s != dirs[-1]:
							heappush(openset, (score+2, x, y, new_path, new_dirs))
						else:
							heappush(openset, (score+1, x, y, new_path, new_dirs))
					else:
						heappush(openset, (score+1, x, y, new_path, new_dirs))
	return


@lru_cache(maxsize=None)
def find_presses(code, iterations):
	
	if iterations == 0:
		return len(code)
	
	prev = 'A'
	total_length = 0
	for char in code:
		total_length += find_presses(tuple(cache[prev, char]), iterations-1)
		prev = char
	
	return total_length


symbols = ['>', '^', '<', 'v', 'A']
for s1 in symbols:
	beg = np.where(dir_keypad == s1)
	beg = (beg[0][0], beg[1][0])
	for s2 in symbols:
		if s1 == s2:
			cache[(s1,s2)] = 'A'
		end = np.where(dir_keypad == s2)
		end = (end[0][0], end[1][0])
		cache[(s1,s2)] = list()
		buttons, directions = search(beg, end, dir_keypad)
		cache[(s1,s2)] = directions

symbols = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', 'A']
for s1 in symbols:
	beg = np.where(numeric_keypad == s1)
	beg = (beg[0][0], beg[1][0])
	for s2 in symbols:
		if s1 == s2:
			cache[(s1,s2)] = 'A'
		end = np.where(numeric_keypad == s2)
		end = (end[0][0], end[1][0])
		buttons, directions = search(beg, end, numeric_keypad)
		cache[(s1,s2)] = directions


codes = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		codes.append(list(line))

numeric_start = np.where(numeric_keypad == 'A')
numeric_start = (numeric_start[0][0], numeric_start[1][0])
dir1_start     = np.where(dir_keypad == 'A')
dir1_start     = (dir1_start[0][0], dir1_start[1][0])
dir2_start     = dir1_start

complexity = 0
sub = 0
depth = int(sys.argv[2])
for code in codes:
	
	sub = int(''.join(code[:-1])) * find_presses(tuple(code), depth)
	complexity += sub
	
print(f'solution after {depth} pads: {complexity}')


