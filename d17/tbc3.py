#!/usr/bin/python3

class TBC():
	def __init__(self, registers=None, program=None):
		self.registers = registers
		assert(len(list(self.registers.keys())) == 3)
		assert('A' in self.registers)
		assert('B' in self.registers)
		assert('C' in self.registers)
		
		self.A = self.registers['A']
		self.B = self.registers['B']
		self.C = self.registers['C']
		
		self.operands = {0:0, 1:1, 2:2, 3:3, 4:self.A, 5:self.B, 6:self.C, 7:None}
		
		self.program = program
		
		self.opcodes = {
			0: self.adv,
			1: self.bxl,
			2: self.bst,
			3: self.jnz,
			4: self.bxc,
			5: self.out,
			6: self.bdv,
			7: self.cdv
		}
		
		self.returns = []
	
	def adv(self, operand):
		self.A = int(self.A / (2**self.operands[operand]))
		self.instruction_pointer += 2
		return
	
	def bxl(self, operand):
		self.B = self.B ^ operand
		self.instruction_pointer += 2
		return
	
	def bst(self, operand):
		self.B = self.operands[operand] % 8
		self.instruction_pointer += 2
		return
	
	def jnz(self, operand):
		if self.A == 0:
			self.instruction_pointer += 2
			return
		else:
			self.instruction_pointer = operand
			return
	
	def bxc(self, operand):
		self.B = self.B ^ self.C
		self.instruction_pointer += 2
		return
	
	def out(self, operand):
		self.returns.append(self.operands[operand] % 8)
		self.instruction_pointer += 2
		return
	
	def bdv(self, operand):
		self.B = int(self.A / (2**self.operands[operand]))
		self.instruction_pointer += 2
		return
	
	def cdv(self, operand):
		self.C = int(self.A / (2**self.operands[operand]))
		self.instruction_pointer += 2
		return
	
	def run(self):
		self.instruction_pointer = 0
		
		while self.instruction_pointer < len(self.program)-1:
			#print(self.program[self.instruction_pointer:self.instruction_pointer+2])
			self.opcodes[self.program[self.instruction_pointer]](self.program[self.instruction_pointer+1])
			self.operands = {0:0, 1:1, 2:2, 3:3, 4:self.A, 5:self.B, 6:self.C, 7:None}
			
			#print(f'A: {bin(self.A)}, B: {bin(self.B)}, C: {bin(self.C)}')
			#print(f'returns: {[bin(r) for r in self.returns]}')
			
					
		return self.returns
		
if __name__ == '__main__':
	
	"""
	Got the help of reddit posts:
		- https://www.reddit.com/r/adventofcode/comments/1hg38ah/2024_day_17_solutions/
		- https://www.reddit.com/r/adventofcode/comments/1hgcuw8/2024_day_17_part_2_any_hints_folks/
	
	The bit shifting on line 133 i learned from some of the responses above
	"""
	
	import sys
	import json
	
	import numpy as np
	
	registers = {'A': None, 'B': None, 'C': None}
	program = ''
	
	with open(sys.argv[1], 'r') as fp:
		for line in fp.readlines():
			line = line.rstrip()
			if len(line) == 0: continue
			if 'Register' in line:
				contents = line.split()
				registers[contents[1][0]] = int(contents[-1])
				continue
			
			if 'Program' in line:
				contents = line.split()
				program = contents[-1]
	
	print(json.dumps(registers,indent=2))
	print(program)
	
	program = program.split(',')
	program = [int(p) for p in program]
	
	possibles = [int(0)]
	
	for k, p in enumerate(program[::-1]):
		new_possibles = []
		for i in range(8):
			for p in possibles:
				a = (p << 3) | i
				
				registers['A'] = a
				tbc = TBC(registers=registers, program=program)
				
				output = tbc.run()
				print(output, k, i, a, p << 3)
				if len(output) != k+1: continue
				if output[0] == program[-(k+1)]:
					new_possibles.append(a)
		
		print(f'new possibles {new_possibles}')
		possibles = new_possibles

	print(np.min(np.array(possibles)))
	
	