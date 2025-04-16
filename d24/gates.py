#!/usr/bin/python3

import json
import sys

def adder(addrs=None, ws=None):
	
	while addrs:
		#print(len(list(addrs.keys())))
		for (k1, op, k2), out in addrs.copy().items():
			#print(k1, op, k2)
			if k1 in ws and k2 in ws:
				if op == 'AND':
					ws[out] = ws[k1] and ws[k2]
					del addrs[(k1,op,k2)]
				elif op == 'OR':
					ws[out] = ws[k1] or ws[k2]
					del addrs[(k1,op,k2)]
				elif op == 'XOR':
					ws[out] = ws[k1] ^ ws[k2]
					del addrs[(k1,op,k2)]
				else:
					print('not found')
					sys.exit()
	
	zeds = {z:v for z,v in ws.items() if z.startswith('z')}
	zeds = {k:v for k,v in sorted(zeds.items(), key=lambda x: x[0], reverse=True)}
	vals = [str(v) for v in zeds.values()]
	binary = ''.join(vals)
	integer = int(binary,base=2)
	binary = bin(integer)
	
	return binary, integer
	

wires = {}
operations = {}
out_wires = {}
with open(sys.argv[1], 'r') as fp:
	for line in fp.readlines():
		line = line.rstrip()
		if len(line) == 0: continue
		
		if ':' in line:
			in_wires = line.split(':')
			wires[in_wires[0]] = int(in_wires[1])
			
		else:
			ops = line.split()
			ops = [ops[0], ops[1], ops[2], ops[-1]]
			args = [ops[0], ops[2]]
			args = sorted(args)
			operations[(args[0], ops[1], args[1])] = ops[-1]

out_wires = {v:k for k,v in operations.items()}


# Part 1
zb,zi = adder(addrs=operations.copy(),ws=wires.copy())
print(f'Part 1: {zi}')


# Part 2
swaps = ['kfp','hbs','dhq','z18','pdg','z22','z27','jcp']
swaps = ','.join(sorted(swaps))
print(f'Part 2: {swaps}')
sys.exit()

# part 2 analysis
x = ''
y = ''
for wire, val in sorted(wires.items(), key=lambda x: x[0], reverse=True):
	#print(wire, val)
	if 'x' in wire:
		x += str(val)
	elif 'y' in wire:
		y += str(val)
	else:
		continue

print(int(x,base=2))
print(int(y,base=2))
ans = int(x,base=2) + int(y,base=2)
print(ans)
print(bin(ans))

bin_ans = bin(ans)

operations[('x09','XOR','y09')] = 'kfp'
operations[('x09','AND','y09')] = 'hbs'
operations[('x18','AND','y18')] = 'dhq'
operations[('fwt','XOR','pvk')] = 'z18'
operations[('bqp','OR','gkg')]  = 'pdg'
operations[('dbp','XOR','dcm')] = 'z22'
operations[('bch','XOR','ckj')] = 'z27'
operations[('bch','AND','ckj')] = 'jcp'

out_wires = {v:k for k,v in operations.items()}


zb,zi = adder(addrs=operations.copy(),ws=wires.copy())
for i,(ab,zz) in enumerate(zip(bin_ans[2:],zb[2:])):
	print(45-i,ab,zz)
print(zi)

swaps = ['kfp','hbs','dhq','z18','pdg','z22','z27','jcp']
swaps = ','.join(sorted(swaps))
print(swaps)



suspect = []
pool = operations.copy()
for i in range(46):
	counter = f'{i:02}'
	zed = 'z'+counter
	# x1 XOR cin -> zed
	zout = out_wires[zed]
	if zout[1] != 'XOR':
		suspect.append(zout)
		print(f'skipping {zed}')
		continue
	else:
		del pool[zout]
	
	# x1
	x1 = zout[0]
	# cin
	cin = zout[2]
	
	# A XOR B -> x1
	if x1 in out_wires:
		x1out = out_wires[x1]
		if x1out[1] != 'XOR':
			cino = out_wires[cin]
			if cino[1] == 'XOR':
				x1 = zout[2]
				cin = zout[0]
				x1out = out_wires[x1]
				del pool[x1out]
			else:
				suspect.append(zout)
				continue
		else:
			del pool[x1out]
	else:
		x1out = None
	
	# A AND B -> c1
	if x1out:
		a = x1out[0]
		b = x1out[2]
		args = [a,b]
		args = sorted(args)
		c1 = (args[0],'AND',args[1])
		if c1 in operations:
			c1out = operations[c1]
			del pool[c1]
		else:
			c1out = None
	else:
		a = None
		b = None
		c1out = None
		c1 = None
	
	# x1 and cin -> c2
	args = [x1, cin]
	args = sorted(args)
	c2 = (args[0],'AND',args[1])
	if c2 in operations:
		c2out = operations[c2]
		del pool[c2]
	else:
		c2out = None
	
	# c1 or c2 -> cout
	if c1out and c2out:
		args = [c1out, c2out]
		args = sorted(args)
		carry_out = (args[0],'OR',args[1])
		if carry_out in operations:
			cout = operations[carry_out]
			del pool[carry_out]
		else:
			cout = None
	else:
		cout = None
		carry_out = None
	
	print()
	print(f'zed: {zed}')
	print(f'zout: {zout}')
	print(f'x1: {x1} cin: {cin}')
	print(f'x1out: {x1out}')
	print(f'a: {a} b: {b}')
	print(f'c1: {c1}')
	print(f'c1out: {c1out}')
	print(f'c2: {c2}')
	print(f'c2out: {c2out}')
	print(f'carry_out: {carry_out}')
	print(f'cout: {cout}')
	print()
	
	#if zed == 'z01': sys.exit()

print(pool)
print(len(list(pool.keys())))



for k,v in pool.items():
	print(k,v)


print(suspect)
sys.exit()

"""
kfp should be
x09 xor y09 -> kfp
x09 and y09 -> hbs

y09 xor x09 -> kfp
x09 and y09 -> hbs

fwt is the x1
x18 xor y18 -> fwt
pvk xor fwt -> (dhq/z18)
pvk and fwt -> c2.... qdb
 c1 is dhq

x18 and y81 -> dhq

bqp or gkg -> z22

x22 xor y22 -> dbq (x1)

dcm xor dbq -> pdq (z22)

ckj is x1
bch in cin
ckj xor bch -> is jcp should be z27

x27 xor y27 -> ckj
knm is c1

ckj AND bch -> jcp





"""

