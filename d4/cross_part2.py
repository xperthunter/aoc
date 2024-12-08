#!/usr/bin/python3

import sys

# read input puzzle
with open(sys.argv[1], 'r') as fp:
	puz = []
	for line in fp.readlines():
		line = line.rstrip()
		puz.append(list(line))

# pattern to match
pat = str(sys.argv[2])
patr = pat[::-1]

# same as part 1, but we are only looking on diagonals now
subs = dict()
for i, row in enumerate(puz):
	for j, char in enumerate(row):
		
		keyg = '.'.join((str(i),str(j)))
		keyu = '.'.join((str(i),str(j)))
		
		subg = puz[i][j]
		subu = puz[i][j]
		
		
		for k in range(1,len(pat)):
			
			try:
				subg += puz[i+k][j+k]
				keyg = '.'.join((keyg, str(i+k), str(j+k)))
				if len(subg) == len(pat): subs[keyg] = subg
			except:
				pass
			
			if i-k < 0: continue
			else:
				try:
					subu += puz[i-k][j+k]
					keyu = '.'.join((keyu, str(i-k), str(j+k)))
					if len(subu) == len(pat): subs[keyu] = subu
				except:
					pass

# store the coordinates of the middle letter of the cross in a dictionary
cross = dict()
for k,v in subs.items():
	if v == pat:
		ijs = k.split('.')
		if (ijs[2], ijs[3]) not in cross: cross[(ijs[2], ijs[3])] = list()
		cross[(ijs[2], ijs[3])].append(k)
	elif v == patr:
		ijs = k.split('.')
		if (ijs[2], ijs[3]) not in cross: cross[(ijs[2], ijs[3])] = list()
		cross[(ijs[2], ijs[3])].append(k)

found = 0
for k in cross:
	if len(cross[k]) == 2: found +=1
	elif len(cross[k]) > 2: sys.exit()
	else: continue

print(found)