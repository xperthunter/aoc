#!/usr/bin/python3

import sys


# read in the input puzzle
with open(sys.argv[1], 'r') as fp:
	puz = []
	for line in fp.readlines():
		line = line.rstrip()
		puz.append(list(line))


# read in the pattern we want to find
pat = str(sys.argv[2])
patr = pat[::-1] # reverse the pattern -- important for later


# we will located all words of length equal to the pattern length 
# all words, sub words (subs) stored in a dictionary
subs = dict()
for i, row in enumerate(puz):
	for j, char in enumerate(row):
		
		# there are 4 directions you can look for sub words
		# we save the i,j indices of each sub word
		keyr = '.'.join((str(i),str(j)))
		keyd = '.'.join((str(i),str(j)))
		keyg = '.'.join((str(i),str(j)))
		keyu = '.'.join((str(i),str(j)))
		
		subr = puz[i][j]
		subd = puz[i][j]
		subg = puz[i][j]
		subu = puz[i][j]
		
		for k in range(1,len(pat)):
			
			# the try/except structure handles access errors
			try:
				subr += puz[i][j+k]
				keyr = '.'.join((keyr, str(i), str(j+k)))
				if len(subr) == len(pat): subs[keyr] = subr
			except: pass
			
			try: 
				subd += puz[i+k][j]
				keyd = '.'.join((keyd, str(i+k),str(j)))
				if len(subd) == len(pat): subs[keyd] = subd
			except: pass
			
			try:
				subg += puz[i+k][j+k]
				keyg = '.'.join((keyg, str(i+k), str(j+k)))
				if len(subg) == len(pat): subs[keyg] = subg
			except: pass
			
			# no looping, i.e no periodic boundary conditions
			if i-k < 0: continue
			else:
				try:
					subu += puz[i-k][j+k]
					keyu = '.'.join((keyu, str(i-k), str(j+k)))
					if len(subu) == len(pat): subs[keyu] = subu
				except: pass

# we just want to count how many sub-words that matched the pattern
found = 0
for k, v in subs.items():
	if v == pat: found += 1
	elif v == patr: found += 1
	else: continue

print(found)

# actually printing the resulting puzzle is slighlty more work
