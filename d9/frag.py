#!/usr/bin/python3

import sys

import numpy as np

fs = ''

fp = open(sys.argv[1], 'r')

fs = fp.readline().rstrip()

print(fs)

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

print(disk_map)
print(''.join(disk_map))
disk_map = list(disk_map)
#moved = dict()
for file in sorted(files.keys(), reverse=True):
	print(file, files[file])
	file_size = files[file][1] - files[file][0]
	
	for gap in gaps:
		if gaps[gap][0] > files[file][1]: break
		gap_size = gaps[gap][1] - gaps[gap][0]
		if gap_size >= file_size:
			disk_map[gaps[gap][0]:(gaps[gap][0]+file_size)] = [str(file)]*file_size
			disk_map[files[file][0]:(files[file][1])] = ['.']*file_size
			if gap_size > file_size:
				gaps[gap] = (gaps[gap][0]+file_size,gaps[gap][1])
				#moved[file] = True
			else:
				#print(gap_size, file_size)
				del gaps[gap]
			break
	print(''.join(disk_map))
	
	continue

checksum = 0
for i, fid in enumerate(disk_map):
	if fid == '.': continue
	checksum += i*int(fid)

print(checksum)
sys.exit()

		
"""
for gap in gaps:
	
	gap_size = gaps[gap][1]-gaps[gap][0]
	#print(gap, gap_size)
	offset = 0
	for file in sorted(files.keys(), reverse=True):
		
		if files[file][0] < gaps[gap][0]: continue
		
		#print(file)
		fs = files[file][1]-files[file][0]
		if fs <= gap_size:
			#print(len(disk_map))
			#print(disk_map[(gaps[gap][0]+offset):(gaps[gap][0]+fs+offset)])
			#print(disk_map[files[file][0]:files[file][1]])
			#print(file)
			disk_map[(gaps[gap][0]+offset):(gaps[gap][0]+fs+offset)] = [str(file)]*int(fs)
			disk_map[files[file][0]:(files[file][1]+1)] = ['.']*int(fs)
			del files[file]
			#print(disk_map)
			#print(len(disk_map))
			
			print(''.join(disk_map))
			break
			gap_size = gap_size - fs
			if gap_size == 0: break
			else:
				offset += fs
				continue
			#sys.exit()
		else:
			del files[file]
			continue

"""		
		
print(''.join(disk_map))		
		

#print(disk_map)
#print(len(disk_map))

# Part 2
#sys.exit()


#map_rev = disk_map[::-1].copy()



#for i, char in enumerate 


"""
# Part 1
#disk_map = list(disk_map)
map_rev  = disk_map[::-1].copy()

for i, char in enumerate(disk_map.copy()):
	if i >= (len(disk_map) - free): break
	if char == '.':
		for j, rev in enumerate(map_rev):
			if rev != '.':
				#print(i, j)
				disk_map[i] = rev
				disk_map[-1*((j+1))] = '.'
				
				map_rev[j] = '.'
				#print(''.join(disk_map))
				#print(''.join(map_rev))
				break

#print(''.join(disk_map))
"""
checksum = 0
for i, fid in enumerate(disk_map):
	if fid == '.': break
	checksum += i*int(fid)

print(checksum)


sys.exit()