#!/usr/bin/python3

import sys

with open(sys.argv[1], 'r') as fp:
	puz = []
	for line in fp.readlines():
		line = line.rstrip()
		puz.append(list(line))

pat = str(sys.argv[2])
patr = pat[::-1]
word = len(pat)

subs = dict()
for i, row in enumerate(puz):
	for j, char in enumerate(row):
		
		keyr = '.'.join((str(i),str(j)))
		keyd = '.'.join((str(i),str(j)))
		keyg = '.'.join((str(i),str(j)))
		keyu = '.'.join((str(i),str(j)))
		
		subr = puz[i][j]
		subd = puz[i][j]
		subg = puz[i][j]
		subu = puz[i][j]
		
		
		for k in range(1,len(pat)):
			
			try:
				subr += puz[i][j+k]
				keyr = '.'.join((keyr, str(i), str(j+k)))
				if len(subr) == len(pat): subs[keyr] = subr
			except:
				pass
			
			try: 
				subd += puz[i+k][j]
				keyd = '.'.join((keyd, str(i+k),str(j)))
				if len(subd) == len(pat): subs[keyd] = subd
			except:
				pass
			
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
					if len(subu) == len(pat):
						print(keyu)
						print(subu)
						subs[keyu] = subu
				except:
					pass

ans = puz

ans = [['.']*len(row) for row in puz]

for row in ans:
	print(''.join(row))
print()

found = 0
for k, v in subs.items():
	if v == pat:
		print(k, v)
		found += 1
		ijs = k.split('.')
		ijs = [int(ii) for ii in ijs]
		for i in range(0, len(ijs)-1, 2):
			ans[ijs[i]][ijs[i+1]] = puz[ijs[i]][ijs[i+1]]
		
	elif v == patr:
		print(k, v)
		found += 1
		ijs = k.split('.')
		ijs = [int(ii) for ii in ijs]
		for i in range(0, len(ijs)-1, 2):
			ans[ijs[i]][ijs[i+1]] = puz[ijs[i]][ijs[i+1]]
	else:
		continue

for row in ans:
	print(''.join(row))

print()
print(found)