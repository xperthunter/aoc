#!/usr/bin/python3

import json
import sys


def find_maximal_cliques(graph):
	stack = [(set(), set(graph.keys()), set())]
	maximal_cliques = []
	
	while stack:
		R, P, X = stack.pop()
		
		if not P and not X:
			maximal_cliques.append(R)
			continue
		
		for v in list(P):
			new_R = R | {v}
			new_P = P & graph[v]
			new_X = X & graph[v]
			
			stack.append((new_R, new_P, new_X))
			P.remove(v)
			X.add(v)
			
	
	return maximal_cliques


pairs = dict()
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		ids = line.split('-')
		
		if ids[0] not in pairs:
			pairs[ids[0]] = list()
		
		if ids[1] not in pairs:
			pairs[ids[1]] = list()
		
		pairs[ids[0]].append(ids[1])
		pairs[ids[1]].append(ids[0])

pairs = {k:set(v) for k,v in pairs.items()}
triplets = []
for k1 in sorted(pairs):
	for k2 in sorted(pairs[k1]):
		for k3 in sorted(pairs[k2]):
			if k3 == k1 or k3 == k2:
				continue
			
			if k3 in pairs[k1]:
				triple = [k1, k2, k3]
				triple = sorted(triple)
				triple = tuple(triple)
				if triple not in triplets:
					triplets.append(triple)

#print(json.dumps(triplets,indent=2))

possibles = 0
for trip in triplets:
	for id in trip:
		if id.startswith('t'):
			possibles += 1
			break

print(f'Part 1: {possibles}')

max_cliques = find_maximal_cliques(pairs)

max_cliques = sorted(max_cliques, key=len)
#print(len(max_cliques[-1]))

#print(max_cliques[-1])
print(f"Part 2: {','.join(sorted(max_cliques[-1]))}")

			