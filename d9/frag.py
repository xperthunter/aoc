#!/usr/bin/python3

import sys

import numpy as np

fs = ''

fp = open(sys.argv[1], 'r')

fs = fp.readline().rstrip()

disk_map = []
file_id = -1
free = 0

files = dict()
gaps = dict()
running_sum = 0
for i, char in enumerate(fs):
	
	if i % 2 == 0:
		file_id += 1
		files[file_id] = (running_sum, running_sum+int(char))
		running_sum += int(char)
		disk_map = disk_map + [str(file_id)]*int(char)
	else:
		disk_map = disk_map + ['.']*int(char)
		free += int(char)
		gaps[file_id] = (running_sum, running_sum+int(char))
		running_sum += int(char)

# Part 1
disk_map1 = list(disk_map).copy()
map_rev  = disk_map1[::-1].copy()

for i, char in enumerate(disk_map1.copy()):
	if i >= (len(disk_map1) - free): break
	if char == '.':
		for j, rev in enumerate(map_rev):
			if rev != '.':
				disk_map1[i] = rev
				disk_map1[-1*((j+1))] = '.'
				
				map_rev[j] = '.'
				break

checksum = 0
for i, fid in enumerate(disk_map1):
	if fid == '.': break
	checksum += i*int(fid)

print(f'Part 1: {checksum}')




disk_map2 = list(disk_map)
for file in sorted(files.keys(), reverse=True):
	file_size = files[file][1] - files[file][0]
	
	for gap in gaps:
		if gaps[gap][0] > files[file][1]: break
		gap_size = gaps[gap][1] - gaps[gap][0]
		if gap_size >= file_size:
			disk_map2[gaps[gap][0]:(gaps[gap][0]+file_size)] = [str(file)]*file_size
			disk_map2[files[file][0]:(files[file][1])] = ['.']*file_size
			if gap_size > file_size:
				gaps[gap] = (gaps[gap][0]+file_size,gaps[gap][1])
				#moved[file] = True
			else:
				#print(gap_size, file_size)
				del gaps[gap]
			break
	
	continue

checksum = 0
for i, fid in enumerate(disk_map2):
	if fid == '.': continue
	checksum += i*int(fid)

print(f'Part 2: {checksum}')
