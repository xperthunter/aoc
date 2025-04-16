#!/usr/bin/python3

import json
import sys


def correct_operators(tests, operations):
	
	signs = operations
	start_ops = [[op] for op in operations]
	correct = 0
	
	for i, test in enumerate(tests):
		ops = start_ops.copy()
		for i in range(1,len(test['terms'])-1):
			
			for op in ops.copy():
				for sign in signs:
					new = op+[sign]
					ops.append(new)
			
			ops = [op for op in ops if len(op) == i+1]
		
		if len(ops) != (len(signs)**(len(test['terms'])-1)):
			print('missing')
			print(ops)
			print(len(test['terms']))
			print(len(signs))
			print(len(ops))
			print(len(signs)**(len(test['terms'])-1))
			print(json.dumps(test,indent=2))
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
				break
	
	return correct
	


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

signs = ['+', '*']
correct = correct_operators(tests, signs)
print(f'Part 1: {correct}')


signs = ['+', '*', '|']
correct = correct_operators(tests, signs)
print(f'Part 2: {correct}')

			 