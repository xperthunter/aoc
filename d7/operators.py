#!/usr/bin/python3

import sys

with open(sys.argv[1], 'r') as fp:
	eqs = []
	for line in fp.readlines():
		line = line.rstrip()
		eqs.append(line)

tests = []
for eq in eqs:
	parts = eq.split()
	ans = int(parts[0][:-1])
	terms = parts[1:]
	terms = [int(term) for term in terms]
	
	eqn = dict()
	eqn['ans'] = ans
	eqn['terms'] = terms
	
	tests.append(eqn)

#sys.exit()
signs = ['+', '*', '|']
correct = 0
for i, test in enumerate(tests):
	
# 	minimum = 0
# 	for term in test['terms']: minimum += term
# 	maximum = 1
# 	for term in test['terms']: maximum *= term
	
# 	if test['ans'] < minimum and test['ans'] > maximum:
# 		print(minimum)
# 		print(maximum)
# 		print(f"{i+1} answer: {test['ans']}")
# 	#continue
	
	ops = [['+'],['*'], ['|']]
	for i in range(1,len(test['terms'])-1):
		
		for op in ops.copy():
			for sign in signs:
				new = op+[sign]
				ops.append(new)
		
		ops = [op for op in ops if len(op) == i+1]
	
	print()
	print(len(ops))
	print(3**(len(test['terms'])-1))
	print(test['terms'])
	print()
	
	if len(ops) != (3**(len(test['terms'])-1)):
		print('missing')
		print(ops)
		sys.exit()
	
	for order in ops:
		result = test['terms'][0]
		for i, (op,term) in enumerate(zip(order,test['terms'][1:])):
			
			if op == '+': result += term
			elif op == '*': result *= term
			elif op == '|': result = int(str(result)+str(term))
			else:
				print(op)
				sys.exit()
		
		if result == test['ans']:
			correct += test['ans']
			print(test['terms'])
			print(test['ans'])
			print(order)
			break

print(correct)
			 