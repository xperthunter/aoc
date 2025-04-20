#!/usr/bin/python3

from heapq import heappop, heappush
import json
import sys

import numpy as np

directions = [(1,0), (0,1), (-1,0), (0,-1)]
symbols    = ['v','>','^','<']

numeric_keypad = [['7','8','9'],['4','5','6'],['1','2','3'],['gap','0','A']]
numeric_keypad = np.array(numeric_keypad)
dir_keypad = [['gap','^','A'],['<','v','>']]
dir_keypad = np.array(dir_keypad)

def search(start, end, pad):
	
	directions = [(1,0), (0,1), (-1,0), (0,-1)]
	symbols    = ['v','>','^','<']
	lowest_score = None
	openset = [(0, start[0], start[1], [pad[start]], [])]
	while openset:
		current = heappop(openset)
		score, i, j, path, dirs = current
		
		if lowest_score and lowest_score < score:
			return
		
		if (i, j) == end:
			yield (path, dirs+['A'])
			continue
		
		for d,s in zip(directions,symbols):
			x = i + d[0]
			y = j + d[1]
			
			if x < pad.shape[0] and x >= 0 and y < pad.shape[1] and y >= 0:
				if pad[x,y] != 'gap':
					new_path = path + [pad[x,y]]
					new_dirs = dirs + [s]
					heappush(openset, (score+1, x, y, new_path, new_dirs))
	
	return


def sub_paths(buttons, directions, presses):
	
# 	print(buttons)
# 	print(directions)
	
# 	for i, (button, direction) in enumerate(zip(buttons[1:-1], directions[1:-1])):
# 		print(button, direction)
# 		presses[(button, buttons[-1])] = directions[i:-1]
	
	for i, bi in enumerate(buttons[:-1]):
		for j, bj in zip(range(i+1,len(buttons)),buttons[i+1:]):
#			print(i,bi,j,bj)
			presses[(bi,bj)] = directions[i:j]+['A']
	
	
	
	return presses



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

enters = dict()

for i,code in enumerate(codes):
	
	for j,c in enumerate(code):
		end = np.where(numeric_keypad == c)
		end = (end[0][0], end[1][0])
		best1 = search(numeric_start, end)
		
		for b1 in best1:
			
	
	
	for j,c in enumerate(code):
		enters[i][j] = dict()
		end = np.where(numeric_keypad == c)
		end = (end[0][0], end[1][0])
		for (path1, dirs1) in search(numeric_start, end):
			
			enters[i][j][dirs1] = dict()
			numeric_start = end
			
			for d1 in dirs1:
				end = np.where(dir_keypad == d1)
				end = (end[0][0], end[1][0])
				for path2, dirs2 in search(dir1_start, end, dir_keypad):
					dir1_start = end
					enters[1] += ''.join(dirs2)
					
					for d2 in dirs2
					
			
# 		if (numeric_keypad[numeric_start], c) in presses:
# 			dirs1 = presses[(numeric_keypad[numeric_start], c)]
# 			numeric_start = np.where(numeric_keypad == c)
# 			numeric_start = (numeric_start[0][0], numeric_start[1][0])
		#else:
		path1, dirs1 = search(numeric_start, end, numeric_keypad)
		presses[(numeric_keypad[numeric_start], c)] = dirs1
		presses = sub_paths(path1, dirs1, presses)
		numeric_start = np.where(numeric_keypad == c)
		numeric_start = (numeric_start[0][0], numeric_start[1][0])
		
		enters[0] += ''.join(dirs1)
		#print(path1)
		#print(dirs1)
		#print(presses)
		#sys.exit()
		for  p1 in dirs1:
# 			if (dir_keypad[dir1_start], p1) in presses:
# 				dirs2 = presses[(dir_keypad[dir1_start], p1)]
# 				dir1_start = np.where(dir_keypad == p1)
# 				dir1_start = (dir1_start[0][0], dir1_start[1][0])
			#else:
			end = np.where(dir_keypad == p1)
			end = (end[0][0], end[1][0])
			path2, dirs2 = search(dir1_start, end, dir_keypad)
			presses[(dir_keypad[dir1_start], p1)] = dirs2
			presses = sub_paths(path2, dirs2, presses)
			
			dir1_start = np.where(dir_keypad == p1)
			dir1_start = (dir1_start[0][0], dir1_start[1][0])
			
			enters[1] += ''.join(dirs2)
			#print(presses)
			#print(path2)
			#print(dirs2)
			#sys.exit()
			for p2 in dirs2:
# 				if (dir_keypad[dir2_start], p2) in presses:
# 					dirs3 = presses[(dir_keypad[dir2_start], p2)] 
# 					dir2_start = np.where(dir_keypad == p2)
# 					dir2_start = (dir2_start[0][0], dir2_start[1][0])
# 				else:
				end = np.where(dir_keypad == p2)
				end = (end[0][0], end[1][0])
				path3, dirs3 = search(dir2_start, end, dir_keypad)
				presses[(dir2_start, p2)] = dirs3
				presses = sub_paths(path3, dirs3, presses)
				
				dir2_start = np.where(dir_keypad == p2)
				dir2_start = (dir2_start[0][0], dir2_start[1][0])
				
				enters[2] += ''.join(dirs3)
				#print(dirs3)
				#print(enters)
				#sys.exit()
			#print(presses)
			
			#sys.exit()
	print(json.dumps(enters,indent=2))
	
	numeric = int(''.join(code[:-1]))
	length  = len(enters[2])
	
	score = numeric*length
	print(numeric, length, score, code)
	complexity += score
	#sys.exit()

print(complexity)
			

"""
def search(start, end, pad):
	
	directions = [(1,0), (0,1), (-1,0), (0,-1)]
	symbols    = ['v','>','^','<']
	
	openset = [(0, start[0], start[1], [pad[start]], [])]
	#print(start, end)
	while openset:
		current = heappop(openset)
		score, i, j, path, dirs = current
		
		if (i, j) == end:
			print()
			print(f'start: {start}, {pad[start]} to end: {end}, {pad[end]}')
			print(path, dirs+['A'])
			print()
			return path, dirs+['A']
		
		for d,s in zip(directions,symbols):
			x = i + d[0]
			y = j + d[1]
			
			if x < pad.shape[0] and x >= 0 and y < pad.shape[1] and y >= 0:
				if pad[x,y] != 'gap':
					#print(f'ij: {(i,j)} xy: {(x,y)} d: {d} pad {pad[x,y]}')
					new_path = path + [pad[x,y]]
					new_dirs = dirs + [s]
					heappush(openset, (score+1, x, y, new_path, new_dirs))
	
	return False, False

def astar(start1, start2, start3, end num_pad, dir_pad):
	
	def _search(start, end, pad):
		
		directions = [(1,0), (0,1), (-1,0), (0,-1)]
		symbols    = ['v','>','^','<']
		
		lowest_score = None
		
		_heap = [(0, start[0], start[1], [pad[start]], [])]
		while _heap:
			score, i, j, path, dirs = heappop(_heap)
			
			if lowest_score and lowest_score < score:
				break
			
			if (i, j) == end:
				yield (path, dirs+['A'])
				continue
		
			for d,s in zip(directions,symbols):
				x = i + d[0]
				y = j + d[1]
				if x < pad.shape[0] and x >= 0 and y < pad.shape[1] and y >= 0:
					if pad[x,y] != 'gap':
						new_path = path + [pad[x,y]]
						new_dirs = dirs + [s]
						heappush(_heap, (score+1, x, y, new_path, new_dirs))
		return
	
	def can_visit(i1, j1, i2, j2, i3, j3, score):
		prev_score = visited.get((i1, j1, i2, j2, i3, j3))
		
		if prev_score and prev_score < score:
			return False
		
		visited[(i1, j1, i2, j2, i3, j3)] = score
		
		return True
	
	directions = [(1,0), (0,1), (-1,0), (0,-1)]
	symbols    = ['v','>','^','<']
	
	visited = {}
	lowest_score = None
	
	start1_i, start1_j = start1
	start2_i, start2_j = start2
	start3_i, start3_j = start3
	
	openset = [(0, start1_i, start1_j, start2_i, start2_j, start3_i, start3_j, [], [], [])]
	while openset:
		current = heappop(openset)
		score, i1, j1, i2, j2, i3, j3, dirs = current
		
		if lowest_score and lowest_score < score:
			break
		
		if (i1, j1) == end:
			lowest_score = score
			return dirs
		
		if not can_visit(i1, j1, i2, j2, i3, j3, score):
			continue
		
		for d, s in zip(directions, symbols):
			x1 = i1 + d[0]
			y1 = j1 + d[1]
			
			if x1 < pad.shape[0] and x1 >= 0 and y1 < pad.shape[1] and y1 >= 0:
				if pad[x1,y1] != 'gap':
					for p2 in _search((i2,j2), s, dir_pad):
						for step2, dir2 in p2:
							x2, y2 = dir2
							for p3 in _search((i3,j3), (x2, y2), dir_pad):
								for step3, dir3 in p3:
									x3, y3 = dir3
									if can_visit(x1, y1, x2, y2, x3, y3, score+1):
										heappush(
											openset,
											(
												score+1,
												x1,
												y1,
												x2,
												y2,
												x3,
												y3
											)
										)
									
					
					
					new_path = path + [pad[x,y]]
					new_dirs = dirs + [s]
					heappush(openset, (score+1, x, y, new_path, new_dirs))
		
		
		for nbr in find_neighbors(i, j, d, grid):
			x, y, weight, new_d = nbr
			if can_visit(new_d, x, y, score+weight):
				if weight == 1000:
					heappush(openset, (score+weight, new_d, i, j, path))
				else:
					heappush(openset, (score+weight, d, x, y, path | {(x,y)}))
	
	print(counter)
	return len(winning_paths)


"""





