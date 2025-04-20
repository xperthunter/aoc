#!/usr/bin/python3

import json
import sys

import networkx as nx
import numpy as np

def find_faces(dic):
	faces = []
	for level in dic:
		vals = sorted(dic[level],reverse=True)
		prev = None
		for i in range(len(vals)):
			if prev == None:
				prev = vals.pop()
				face = [prev]
				continue
			else:
				if prev+1 in vals:
					face.append(prev+1)
					vals.remove(prev+1)
					prev = prev+1
					continue
				else:
					faces.append(face)
					vals = sorted(vals, reverse=True)
					prev = vals.pop()
					face = [prev]
					continue
			
		faces.append(face)
	
	return faces

# read in garden from command line args
with open(sys.argv[1], 'r') as fp:
	garden = []
	for line in fp.readlines():
		line = line.rstrip()
		garden.append(list(line))

# pad the garden on all sides
garden = [['.']+row+['.'] for row in garden]
dummy = ['.'] * (len(garden)+2)
garden.insert(0, dummy)
garden.append(dummy)

garden_array = np.array(garden)

# collect neighbor information
width = len(garden)
self_nodes = []
self_edges = []
non_self_nodes = []
non_self_edges = []
for i in range(1,len(garden)-1):
	row = garden[i]
	for j in range(1,len(row)-1):
		elm = garden[i][j]
		ind = j + i * width # each cell gets a numerical index
		
		# check cell above
		if garden[i-1][j] == elm:
			self_edges.append((ind, ind-width))
			if ind not in self_nodes: self_nodes.append(ind)
			if ind-width not in self_nodes: self_nodes.append(ind-width)
		else:
			non_self_edges.append((ind, ind-width))
			if ind not in non_self_nodes: non_self_nodes.append(ind)
			if ind-width not in non_self_nodes: non_self_nodes.append(ind-width)
		
		# check cell right
		if garden[i][j+1] == elm:
			self_edges.append((ind, ind+1))
			if ind not in self_nodes: self_nodes.append(ind)
			if ind+1 not in self_nodes: self_nodes.append(ind+1)
		else:
			non_self_edges.append((ind, ind+1))
			if ind not in non_self_nodes: non_self_nodes.append(ind)
			if ind+1 not in non_self_nodes: non_self_nodes.append(ind+1)
		
		# check cell left
		if j == 1:
			non_self_edges.append((ind, ind-1))
			if ind not in non_self_nodes: non_self_nodes.append(ind)
			if ind-1 not in non_self_nodes: non_self_nodes.append(ind-1)
		
		# check cell down
		if i == len(garden)-2:
			non_self_edges.append((ind,ind+width))
			if ind not in non_self_nodes: non_self_nodes.append(ind)
			if ind+width not in non_self_nodes: non_self_nodes.append(ind+width)
		
# build graphs
self_graph = nx.Graph()
non_self_graph = nx.Graph()

self_graph.add_nodes_from(self_nodes)
self_graph.add_edges_from(self_edges)

non_self_graph.add_nodes_from(non_self_nodes)
non_self_graph.add_edges_from(non_self_edges)

# for nodes in non-self that have degree 4, they have no neighbors and are singletons
# Ex: 
#  ...O...
#  ...|...  
#  .O-X-O.
#  ...|...
#  ...O...

singletons = [n for n,d in dict(non_self_graph.degree()).items() if d == 4]
cost = 4*len(singletons)

# set up costs for part 1 and 2
cost_part1 = cost
cost_part2 = cost

# go through connected components and bound each one
for c in nx.connected_components(self_graph):
	
	# area := the number of nodes in the component
	area = len(list(c))
	
	# determine the bounding nodes
	# note -> nx.induced_subgraph() returns subgraph with edges with both ends 
	# 	of edge in query nodes
	# by definition, non_self_graph wont have any edges between query nodes in this case
	sub = nx.induced_subgraph(non_self_graph, list(c))
	sub_nodes = list(sub.nodes)
	
	# plant symbol
	plant = garden[int(sub_nodes[0]/width)][sub_nodes[0] % width]
	
	# find the non-self nodes that bound the sub_nodes
	# found by accessing non_self_graph.neighbors(boundary_node)
	outer_nodes1 = []
	outer_nodes2 = []
	for boundary_node in sub_nodes:
		for nbr in non_self_graph.neighbors(boundary_node):
			if nbr in sub_nodes: continue
			if nbr not in outer_nodes2:
				outer_nodes2.append(nbr)
			
			outer_nodes1.append(nbr)
	
	cost_part1 += area * len(outer_nodes1)
	#print(f'part 1 --> region: {plant}, {area} * {len(outer_nodes1)}, {area*len(outer_nodes1)}')
	
	outer_nodes = outer_nodes2
	# expanded our sub-graph to include the nodes from the outer_nodes
	expanded = nx.induced_subgraph(non_self_graph, sub_nodes+outer_nodes).copy()
	
	# remove edges between non-self nodes, not needed
	redges = []
	for e in expanded.edges():
		u, v = e
		if u not in sub_nodes:
			if v not in sub_nodes:
				redges.append(e)
		if u not in sub_nodes and v not in sub_nodes: redges.append(e)
	expanded.remove_edges_from(redges)
	
	# re cast the node labeling from integer to order pair coordinates
	sets = dict()
	for sub_node in sub_nodes:
		for nbr in expanded.neighbors(sub_node):
			if nbr in sub_nodes: continue
			row = int(nbr / width)
			col = nbr % width
			diff = sub_node - nbr
			if diff not in sets: sets[diff] = list()
			sets[diff].append([row,col])
	
	faces = []
	for d in sets:
		levels = dict()
		if abs(d) == 1:
			entries = sorted(sets[d], key = lambda x: (x[1], x[0]))
			for coord in entries:
				if coord[1] not in levels:
					levels[coord[1]] = list()
				levels[coord[1]].append(coord[0])
		else:
			entries = sorted(sets[d], key = lambda x: (x[0], x[1]))
			for coord in entries:
				if coord[0] not in levels:
					levels[coord[0]] = list()
				levels[coord[0]].append(coord[1])
		
		new_faces = find_faces(levels)
		faces = faces + new_faces	
	
	cost_part2 += area*(len(faces))
	
	#print(f'part 2 --> region: {plant}, {area} * {len(faces)}, {area*len(faces)}')
	
		

print(f'Part 1: {cost_part1}')
print(f'Part 2: {cost_part2}')

