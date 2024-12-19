#!/usr/bin/python3

import sys

import networkx as nx
import numpy as np

trail_map = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		line = [int(item) for item in line]
		
		trail_map.append(line)

trail_map = np.array(trail_map)

G = nx.DiGraph()

width  = trail_map.shape[1]
height = trail_map.shape[0] 
print(f'height: {height} width: {width}')
nodes = []
edges = []
for i, row in enumerate(trail_map):
	for j, item in enumerate(row):
		ind = j + i * width
		print(i, j, width-1)
		nodes.append((ind, {'value':trail_map[i,j]}))
		
		if j < width-1:
			if trail_map[i,j+1] - trail_map[i,j] == 1:
				edges.append((ind, ind+1))
				print(ind, ind+1, 'right')
		
		if j > 0:
			if trail_map[i,j-1] - trail_map[i,j] == 1:
				edges.append((ind,ind-1))
				print(ind, ind-1, 'left')
		
		if i > 0:
			if trail_map[i-1,j] - trail_map[i,j] == 1:
				edges.append((ind, ind-width))
				print(ind, ind-width, 'up')
		
		if i < height-1:
			if trail_map[i+1,j] - trail_map[i,j] == 1:
				edges.append((ind, ind+width))
				print(ind, ind+width, 'down')

print(len(nodes))
print(len(edges))
G.add_nodes_from(nodes)
G.add_edges_from(edges)
trail_heads = [node for node, data in G.nodes(data=True) if data['value'] == 0]
trail_ends  = [node for node, data in G.nodes(data=True) if data['value'] == 9]
print(trail_heads)
print(trail_ends)

score = 0
for head in trail_heads:
	for end in trail_ends:
		
		if nx.has_path(G, head, end):
			print(f'path! {head}, {end}')
			score += 1

print(score)

score = 0
for head in trail_heads:
	for end in trail_ends:
		
		if nx.has_path(G, head, end):
			paths = list(nx.all_simple_paths(G, source=head, target=end))
			score += len(paths)

print(score)



