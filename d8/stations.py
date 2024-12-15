#!/usr/bin/python3

import sys

import numpy as np

grid = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		grid.append(list(line))

grid = np.array(grid)

stations = dict()
for i, row in enumerate(grid):
	for j, elm in enumerate(row):
		if elm == '.': continue
		
		if elm not in stations:
			stations[elm] = ([i], [j])
		else:
			stations[elm][0].append(i)
			stations[elm][1].append(j)
			
antinodes = np.zeros(np.shape(grid))
for station in stations:
	print(station)
	print(stations[station])
	
	print(grid[stations[station]])
# 	continue
	for i in range(len(stations[station][0])):
		antinodes[stations[station][0][i], stations[station][1][i]] = 1
		for j in range(i+1, len(stations[station][0])):
			
			row_shift = stations[station][0][j] - stations[station][0][i]
			col_shift = stations[station][1][j] - stations[station][1][i]
			
			antinodes[stations[station][0][j], stations[station][1][j]] = 1
			
			in_grid = True
			k = 2
			while in_grid:
				grid_x = k*row_shift + stations[station][0][i]
				grid_y = k*col_shift + stations[station][1][i]
				
				if grid_x >= 0 and grid_y >= 0:
					try:
						antinodes[grid_x, grid_y] = 1
						k += 1
					except:
						in_grid = False
				else:
					in_grid = False
			
			in_grid = True
			k = 1
			while in_grid:
				grid_x = stations[station][0][i] - k*row_shift
				grid_y = stations[station][1][i] - k*col_shift
				
				if grid_x >= 0 and grid_y >= 0:
					try:
						antinodes[grid_x, grid_y] = 1
						k += 1
					except:
						in_grid = False
				else:
					in_grid = False
			 
				
			
			
			
# 			twice_row = 2*row_shift + stations[station][0][i]
# 			twice_col = 2*col_shift + stations[station][1][i]
# 			
# 			once_row = stations[station][0][i] - row_shift
# 			once_col = stations[station][1][i] - col_shift
# 			
# 			if twice_row >= 0 and twice_col >= 0:
# 				try:
# 					antinodes[twice_row, twice_col] = 1
# 					print(twice_row, twice_col)
# 				except: pass
# 			
# 			if once_row >= 0 and once_col >= 0:
# 				try:
# 					antinodes[once_row, once_col] = 1
# 					print(once_row, once_col)
# 				except: pass
			
# 			print(row_shift, col_shift)
# 			print(stations[station][0][i], stations[station][1][i])
# 			print(stations[station][0][j], stations[station][1][j])
# 			
# 			print(twice_row, twice_col)
# 			print(once_row, once_col)


print(antinodes)
print(np.sum(antinodes))
sys.exit()
anti = np.sum(grid[np.where(antinodes == 1)])
print(anti)
		



