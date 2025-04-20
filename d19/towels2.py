#!/usr/bin/python3

"""
Used responses from this reddit thread to help me
	- https://www.reddit.com/r/adventofcode/comments/1hmsmxf/2024_day_19_part_2_why_i_struggled_with_this/
learned about caches and helped me with memoization
"""


from functools import lru_cache
from heapq import heappop, heappush
import json
import sys

def towel_options(towel, patterns):
	towel_opts = dict()
	
	for i,t in enumerate(towel):
		if i not in towel_opts: towel_opts[i] = list()
		for pat in patterns:
			if pat[0] != t: continue
			if i+len(pat) > len(towel): continue
			
			if towel[i:i+len(pat)] == pat: towel_opts[i].append(pat)
	
	return towel_opts

def kmer_star(towel, patterns):
	
	opts = towel_options(towel, patterns)
	
	p = 0
	openset = [(len(towel),0,'')]
	while openset:
		score, cur, sub = heappop(openset)
		if score == 0:
			p += 1
			continue
		
		#print(score, cur, opts[cur], sub, len(openset))
		if len(opts[cur]) == 0: continue
		
		for opt in opts[cur]:
			heappush(openset, (len(towel)-len(sub)-len(opt), cur+len(opt), sub+opt))
	
	return p	

def count_solutions(design, patterns):
	
	if design == '':
		return 1
	
	if design in cache:
		print(f'already found score for design {design} => {cache[design]}')
		return cache[design]
	
	result = 0
	for pat in patterns:
		if design.startswith(pat):
			remain = design[len(pat):]
			print(f'found pat {pat} at pos {len(design)}')
			result += count_solutions(remain, patterns)
	
	cache[design] = result
	return result

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

pats = tuple(pats)
cache = dict()
possibles = 0
for towel in towels:
	possibles += count_solutions(towel, pats)

print(possibles)







































