#!/usr/bin/python3

from heapq import heappop, heappush
import json
import sys

def kmers(word, k):
	for i in range(0,len(word)-k+1):
		yield word[i:i+k], list(range(i,i+k))

def kmer_star(string, patterns):
	
	p = 0
	visited = {}
	openset = [(len(string),0,'','')]
	while openset:
		score, cur, sub, parts = heappop(openset)
		if score == 0:
			p += 1
			print()
			print(p)
			print(sub)
			print(string)
			print(parts)
			print()
			continue
		
		for i,pat in enumerate(patterns):
			word = string[cur:cur+len(pat)]
			if word == pat:
				new_parts = parts+'.'+str(i)
				if new_parts in visited:
					print('found a repeat')
					continue
				heappush(openset, (len(string)-len(sub)-len(pat), cur+len(pat), sub+pat, new_parts))
				visited[new_parts] = True
	
	return p


towels = []
pats = []
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		if ',' in line:
			pats = pats + line.split(', ')
		elif len(line) == 0: continue
		else:
			towels.append(line)

print(pats)
print(towels)

possibles = 0
for towel in towels:
	possibles += kmer_star(towel, pats)
	continue
	openset = [(len(towel),0,'')]
	visited = dict()
	while len(openset) > 0:
		score, cur, sub = heappop(openset)
		print(score, cur, sub, len(openset))
		print(towel)
		if score == 0:
			possibles += 1
			continue
			
		for pat in pats:
			word = towel[cur:cur+len(pat)]
			if word == pat:
				heappush(openset, (len(towel)-len(sub)-len(pat), cur+len(pat), sub+pat))
	

print(possibles)

"""


for towel in towel:
	word = 0
	for i in range(towel):
	while coverage:
		word = towel[i,i+k]
		if k 


sizes = dict()
for p in pats:
	if len(p) not in sizes: sizes[len(p)] = True

possibles = 0
for towel in towels:
	coverage = {}
	coverage = {ii:0 for ii in range(len(towel))}
	for k in sizes:
		for kmer, locs in kmers(towel,k):
			print(towel, kmer, locs)
			if kmer in pats:
				for loc in locs: coverage[loc] += 1
	
	vals = list(coverage.values())
	if min(vals) == 0:
		print(towel)
		print(json.dumps(coverage))
		sys.exit()
	else:              possibles += 1
				
print(possibles)			
"""			
	