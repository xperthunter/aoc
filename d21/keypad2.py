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
	
	print(code, iterations)
	
	if iterations == 0:
		return len(code)
	
	prev = 'A'
	total_length = 0
	for char in code:
		print(prev, char, iterations)
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
		#print(f'from: {s1} to: {s2}')
		cache[(s1,s2)] = list()
		buttons, directions = search(beg, end, dir_keypad)
		#print(buttons, directions)
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
		#print(f'from: {s1} to: {s2}')
		buttons, directions = search(beg, end, numeric_keypad)
		#print(buttons, directions)
		cache[(s1,s2)] = directions


# for k in cache:
# 	print(f"{k} -> {''.join(cache[k])}")

#sys.exit()


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
depth = 4
for code in codes:
	
	sub = int(''.join(code[:-1])) * find_presses(tuple(code), depth)
	print(f'sub {sub}')
	complexity += sub
	
print(complexity)


# """
# def flatten(node):
# 	if isinstance(node, str):
# 		return [node]
# 	elif isinstance(node, list):
# 		return node
# 	elif isinstance(node, tuple):
# 		return flatten(node[0]) + flatten(node[1])
# 	else:
# 		raise TypeError(f"Unexpected type: {type(node)}")
# 
# 
# def compute_codes(input_code, depth=2):
# 	
# 	for i in range(0, len(input_code)-1, 2):
# 		step = tuple(input_code[i:i+2])
# 		assert(step in cache)
# 		new_code = cache[step]
# 		#print(step)
# 		#print(new_code)
# 		for ii in range(depth):
# 			iter_result = new_find(['A']+new_code)
# 			cache[tuple(['A']+new_code)] = iter_result
# 			new_code = iter_result
# 			print(ii, len(new_code))
# 			
# 			#sys.exit()
# 			#new_code = flatten(new_code)
# 			#print(new_code)
# 		print(new_code)
# 		for k in cache:
# 			if len(k) == 2: continue
# 			print(k, ''.join(cache[k]))
# 		sys.exit()
# 
# 
# def new_find(input_code):
# 	#print(input_code)
# 	if len(input_code) < 2: return []
# 	result = []
# 	
# 	seq = input_code
# 	max_segment = len(input_code)-1
# 	while seq:
# 		if tuple(seq) not in cache:
# 			seq = seq[:-1]
# 			max_segment -= 1
# 		else:
# 			print(f'in cache, length {len(seq)}')
# 			result += cache[tuple(seq)]
# 			break
# 	
# 	#print(input_code, result)
# 	
# 	if seq != input_code:
# 		result += cache[(seq[-1], input_code[max_segment+1])]
# 		cache[tuple(input_code[:(max_segment+2)])] = result
# 		#print(f'new key in cache {tuple(input_code[:(max_segment+2)])}')
# 		
# 		#print(max_segment)
# 		remaining = input_code[max_segment+1:]
# 		result += new_find(remaining)
# 	else:
# 		return result
# 	
# 	
# 	
# 	return result
# 
# def find_presses(seq):
# 	
# 	key = tuple(seq)
# 	if key in cache:
# 		return cache[key]
# 	
# 	prefix_result = find_presses(seq[:-1])
# 	suffix_result = cache[tuple(seq[-2:])]
# 	
# 	result = prefix_result + suffix_result
# 	cache[key] = result
# 	return result
# 
# 
# symbols = ['>', '^', '<', 'v', 'A']
# for s1 in symbols:
# 	beg = np.where(dir_keypad == s1)
# 	beg = (beg[0][0], beg[1][0])
# 	for s2 in symbols:
# 		if s1 == s2:
# 			cache[(s1,s2)] = 'A'
# 		end = np.where(dir_keypad == s2)
# 		end = (end[0][0], end[1][0])
# 		#print(f'from: {s1} to: {s2}')
# 		cache[(s1,s2)] = list()
# 		buttons, directions = search(beg, end, dir_keypad)
# 		#print(buttons, directions)
# 		cache[(s1,s2)] = directions
# 
# symbols = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', 'A']
# for s1 in symbols:
# 	beg = np.where(numeric_keypad == s1)
# 	beg = (beg[0][0], beg[1][0])
# 	for s2 in symbols:
# 		if s1 == s2:
# 			cache[(s1,s2)] = 'A'
# 		end = np.where(numeric_keypad == s2)
# 		end = (end[0][0], end[1][0])
# 		#print(f'from: {s1} to: {s2}')
# 		buttons, directions = search(beg, end, numeric_keypad)
# 		#print(buttons, directions)
# 		cache[(s1,s2)] = directions
# 
# 
# codes = []
# with open(sys.argv[1], 'r') as fp:
# 	for line in fp.readlines():
# 		line = line.rstrip()
# 		codes.append(list(line))
# 
# numeric_start = np.where(numeric_keypad == 'A')
# numeric_start = (numeric_start[0][0], numeric_start[1][0])
# dir1_start     = np.where(dir_keypad == 'A')
# dir1_start     = (dir1_start[0][0], dir1_start[1][0])
# dir2_start     = dir1_start
# 
# complexity = 0
# for code in codes:
# 	
# 	print(code)
# 	scr = compute_codes(['A']+code, depth=9)
# 	sys.exit()
# 	
# 	intermediate_code = find_presses(['A']+code, numeric_keypad)
# 	for i in range(10):
# 		
# 		intermediate_code = ['A']+flatten(intermediate_code)
# 		intermediate_code = find_presses(intermediate_code, dir_keypad)
# 		print(f'iter: {i} | code length: {len(flatten(intermediate_code))} | cache keys: {len(list(cache.keys()))}')
# 	
# 	complexity += int(''.join(code[:-1])) * len(flatten(intermediate_code))
# 
# 
# 
# print(complexity)
# 
# 
# """
# """
# 		dir_codes, button_codes = find_presses(code, 'A', dir_keypad)
# 	
# 	dir1_codes, button1_codes = find_presses(code, 'A', numeric_keypad)
# 	
# 	print(dir1_codes)
# 	print(button1_codes)
# 	
# 	dir2_codes = dict()
# 	button2_codes = dict()
# 	
# 	for dir1_code in dir1_codes:
# 		d2, b2 = find_presses(dir1_code, 'A', dir_keypad)
# 		
# 		for _ in d2:
# 			if _ not in dir2_codes: dir2_codes[_] = True
# 		
# 		for _ in b2:
# 			if _ not in button2_codes: button2_codes[_] = True
# 	
# 	dir2_lengths = [len(k) for k in dir2_codes]
# 	min_length   = min(dir2_lengths)
# 	
# 	dir2_codes = {k:v for k,v in dir2_codes.items() if len(k) <= min_length}
# 	
# 	dir3_codes = dict()
# 	for d2_code in dir2_codes:
# 		
# 		d3, b3 = find_presses(d2_code, 'A', dir_keypad)
# 		
# 		for _, button in zip(d3, b3):
# 			if _ not in dir3_codes:
# 				dir3_codes[_] = list()
# 			
# 			dir3_codes[_].append(button)
# 		
# 	
# 	dir3_lengths = [len(k) for k in dir3_codes]
# 	min_length = min(dir3_lengths)
# 	print(min_length)
# 	#sys.exit()
# 	dir3_codes = {k:v for k,v in dir3_codes.items() if len(k) <= min_length}
# 	complexity += int(''.join(code[:-1])) * min_length
# 	
# 	dir_code = memoize(code, 'A', numeric_keypad)
# 	#print(len(dir_codes))
# 	#print(dir_codes)
# 	for i in range(13):
# 		print(f'iter {i}')
# 		
# 		dircode = memoize(dir_)
# 		
# 		#print(len(dir_codes))
# 		step_dirs = dict()
# 		step_buttons = dict()
# 		
# 		for d in dir_codes:
# 			new_dirs, new_buttons = find_presses(d, 'A', dir_keypad)
# 			#print(len(new_dirs))
# 			for nd in new_dirs:
# 				if nd not in step_dirs:
# 					step_dirs[nd] = True
# 					#print(nd, len(nd), score_code(nd), d)
# 			
# 			for nb in new_buttons:
# 				if nb not in step_buttons: step_buttons[nb] = True
# 		
# # 		for sd in step_dirs:
# # 			print(sd, len(sd), score_code(sd), d)
# 		#sys.exit()
# 
# # 		for sd in step_dirs:
# # 			print(sd, len(sd))
# 		#sys.exit()
# 		
# 		dir_codes = sorted(list(step_dirs.keys()), key=score_code)
# 		dir_codes = [dir_codes[0]]
# 		#print([dir_codes[0]])
# 		continue
# 		sys.exit()
# 		
# 		dir_lengths = [len(k) for k in step_dirs]
# 		min_length = min(dir_lengths)
# 		print(len(step_dirs))
# 		len_data = dict()
# 		for ll in dir_lengths:
# 			if ll not in len_data: len_data[ll] = 0
# 			len_data[ll] += 1
# 		
# 		print(json.dumps(len_data,indent=2))
# 		dir_codes = {k:v for k,v in step_dirs.items() if len(k) <= min_length}
# 		#print(json.dumps(dir_codes,indent=2))
# 		print(len(dir_codes))
# 		dir_codes = [list(dir_codes.keys())[0]]
# 	
# 	complexity += int(''.join(code[:-1])) * len(dir_codes[0])
# 	
# 	
# 	# def find_presses(code, start, pad):
# # 	
# # 	beg = np.where(pad == start)
# # 	beg = (beg[0][0], beg[1][0])
# # 	
# # 	directions = {i:list() for i in range(len(code))}
# # 	buttons    = {i:list() for i in range(len(code))}
# # 		
# # 	for i, c in enumerate(code):
# # 		
# # 		#print(f'fp iter {i} c {c}')
# # 		
# # 		end = np.where(pad == c)
# # 		end = (end[0][0], end[1][0])
# # 		
# # 		if (pad[beg], pad[end]) in cache:
# # 			button_paths = cache[(pad[beg], pad[end])]['buttons']
# # 			dir_paths    = cache[(pad[beg], pad[end])]['directions']
# # 			#print('in cache')
# # 		else:
# # 			searches = list(search(beg, end, pad))
# # 				
# # 			button_paths = [s[0] for s in searches]
# # 			dir_paths    = [s[1] for s in searches]
# # 			
# # 			cache[(pad[beg], pad[end])] = dict()
# # 			cache[(pad[beg], pad[end])]['buttons'] = list()
# # 			cache[(pad[beg], pad[end])]['directions'] = list()
# # 			
# # 			cache[(pad[beg], pad[end])]['buttons'] = button_paths
# # 			cache[(pad[beg], pad[end])]['directions'] = dir_paths
# # 			
# # 		
# # 		buttons[i]    = button_paths
# # 		directions[i] = dir_paths
# # 		
# # 		beg = end
# # 	
# # 	
# # 	direction_results = ''
# # 	
# # 	total = 0
# # 	for pos in directions:
# # 		direction_results += ''.join(directions[pos][0])
# # 		continue
# # 		if len(directions[pos]) == 1:
# # 			direction_results += ''.join(directions[pos][0])
# # 			total += score_code(directions[pos][0])
# # 		else:
# # 			direction_results += ''.join(directions[pos][0])
# # 			continue
# # 			options = {}
# # 			for opt in directions[pos]:
# # 				new = direction_results + ''.join(opt)
# # 				options[tuple(opt)] = score_code(new)
# # 			
# # 			#print(direction_results)
# # 			#print(options)
# # 			opts = sorted(options)
# # 			#print(opts)
# # 			direction_results += ''.join(opts[0])
# # 	
# # 	r = list()
# # 	cache[''.join(code)] = direction_results
# # 	r.append(direction_results)
# # 	#print(r)
# # 	return r, []
# # 				
# # 			
# # 	
# # 	
# # 	print(directions)	
# # 	print('before combos')
# # 	direction_combos = list(itertools.product(*(directions[k] for k in directions)))
# # 	
# # 	direction_results = []
# # 	for combo in direction_combos:
# # 		new = ''
# # 		for c in combo:
# # 			new += ''.join(c)
# # 		direction_results.append(new)
# # 	
# # 	button_combos  = list(itertools.product(*(buttons[k] for k in buttons)))
# # 	button_results = []
# # 	for combo in button_combos:
# # 		new = ''
# # 		for c in combo:
# # 			new += ''.join(c)
# # 		button_results.append(new)
# # 	
# # 	return direction_results, button_results
# 	
# 	
# 
# 		chunked_results = []
# 		for j in range(0, len(intermediate_code), chunk_size):
# 			if j + chunk_size > len(intermediate_code):
# 				chunk = intermediate_code[j:]
# 			else:
# 				chunk = intermediate_code[j:j+chunk_size]
# 			
# 			chunk_result = find_presses(chunk, dir_keypad)
# 			chunked_results.extend(flatten(chunk_result))
# 		
# 		intermediate_code = chunked_results
# 		#intermediate_code = find_presses(['A']+flatten(intermediate_code), dir_keypad)
# 
# """
# 
# """
