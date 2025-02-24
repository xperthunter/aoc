#!/usr/bin/python3

import sys
import numpy as np

def manhattan_distance(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def tuples(cen, radius, max_x, max_y):
	x, y = cen
	
	for xi in range(x-radius, x+radius+1):
		if xi < 0 or xi > max_x: continue
		for yi in range(y-radius, y+radius+1):
			if yi < 0 or yi > max_y:
				continue
			
			if manhattan_distance((xi,yi), (x,y)) <= radius and manhattan_distance((xi,yi), (x,y)) > 1:
				yield (xi, yi)

def cheats_part2(path, track):
	
	cheats = {}
	for d in range(20,21):
		
		for step in path:
			xc, yc = step
			
			for xa,ya in tuples((xc,yc), d, track.shape[0], track.shape[1]):
				if (xa,ya) not in path:
					continue
				
				if path[(xa,ya)] > path[(xc,yc)]:
					savings = path[(xa,ya)] - path[(xc,yc)] - manhattan_distance((xa,ya),(xc,yc))
					
					if savings not in cheats:
						cheats[savings] = 0
					
					cheats[savings] += 1
	
	return cheats


def count_path(track, start, end):
	
	directions = [(1,0), (0,1), (-1,0), (0,-1)]
	
	i, j = start
	path = [(i,j,0)]
	racing = True
	while racing:
		
		i, j, counter = path[-1]
		
		nbrs = []
		for d in directions:
			x = i + d[0]
			y = j + d[1]
			
			if track[x,y] == '#': continue
			elif (x,y,counter-1) in path: continue
			elif track[x,y] == 'E':
				nbrs.append((x,y,counter+1))
				racing = False
			else:
				nbrs.append((x,y,counter+1))
		
		assert(len(nbrs) == 1)
		path.append(nbrs[0])
	
	path = {(p[0], p[1]):int(p[2]) for p in path}
	
	return path

def valid_cheats(path, track):
	
	skips = [(2,0), (0,2), (-2,0), (0,-2)]
	walls = [(1,0), (0,1), (-1,0), (0,-1)]
	
	cheats = {}
	for step in path:
		i, j = step
		for d,w in zip(skips,walls):
			x = i + d[0]
			y = j + d[1]
			
			if x < 0 or x > track.shape[0] or y < 0 or y > track.shape[1]: continue
			
			if (x,y) in path:
				if path[(x,y)] > path[(i,j)]:
					wx = i + w[0]
					wy = j + w[1]
					
					if track[wx,wy] == '#':
						savings = path[(x,y)] - path[(i,j)] - 2
						
						print(f'from: {(i,j)} to: {(x,y)} savings: {savings}')
						print(f'from count: {path[(i,j)]} to count: {path[(x,y)]}')
						
						if savings not in cheats:
							cheats[savings] = 0
							
						
						cheats[savings] += 1
	
	return cheats


track = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		track.append(list(line))

track = np.array(track)

#print()
#for row in track: print(''.join(row))
#print()

start = np.where(track == 'S')
start = (start[0][0], start[1][0])
end   = np.where(track == 'E')
end   = (end[0][0], end[1][0])
track_length = np.sum(track == '.')

print(start)
print(end)
print(track_length)

path = count_path(track, start, end)

print(path)

# cheats = valid_cheats(path, track)
# 
# productive_cheats = 0
# for k,v in sorted(cheats.items(), key=lambda x: x[0]):
# 	if k >= 100:
# 		print(k,v)
# 		productive_cheats += v
# 
# print(productive_cheats)



# part 2

cheats = cheats_part2(path, track)

productive_cheats = 0
for k,v in sorted(cheats.items(), key=lambda x: x[0]):
	if k >= 100:
		print(v,k)
		productive_cheats += v

print(productive_cheats)




























