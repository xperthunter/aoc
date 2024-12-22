#!/usr/bin/python3

import json
import sys

def safe_report(report, tolerate=False):
	
	uniq = {lvl:[] for lvl in report}
	for i, lvl in enumerate(report): uniq[lvl].append(i)
	duplicates = [lvl for lvl in uniq.keys() if len(uniq[lvl]) > 1]
	
	if len(duplicates) > 1: return False
	elif len(duplicates) == 1:
		if len(uniq[duplicates[0]]) > 2: return False
		else:
			if tolerate:
				modified = report.copy()
				del modified[uniq[duplicates[0]][0]]
				if safe_report(modified, tolerate=False):
					return True
				else:
					modified = report.copy()
					del modified[uniq[duplicates[0]][1]]
					if safe_report(modified, tolerate=False):
						return True
					else:
						return False
			else:
				return False
	else:
		if report[1] - report[0] <= 3 and report[1] - report[0] > 0:
			direction = 1
		elif report[0] - report[1] <= 3 and report[0] - report[1] > 0:
			direction = -1
		else:
			if tolerate:
				modified = report.copy()
				del modified[0]
				if safe_report(modified, tolerate=False):
					return True
				else:
					modified = report.copy()
					del modified[1]
					if safe_report(modified, tolerate=False):
						return True
					else:
						return False
			else:
				return False
		 
		for i, lvl in enumerate(report[:-1]):
			if direction*(report[i+1] - lvl) > 3 or direction*(report[i+1] - lvl) < 0:
				if tolerate:
					modified = report.copy()
					del modified[i]
					if safe_report(modified, tolerate=False):
						return True
					else:
						modified = report.copy()
						del modified[i+1]
						if safe_report(modified, tolerate=False):
							return True
						else:
							modified = report.copy()
							del modified[i-1]
							if safe_report(modified, tolerate=False):
								return True
							else:
								return False
				else:
					return False
	return True	
		

				
				


with open(sys.argv[1], 'r') as fp:
	reports = []
	for line in fp.readlines():
		line = line.rstrip()
		
		levels = line.split()
		levels = [int(level) for level in levels]
		
		reports.append(levels)


safe_reports = 0
for report in reports:
	
	if safe_report(report, tolerate=True):
		print(f"safe: {' '.join([str(item) for item in report])}")
		safe_reports += 1
	else:
		print(f"unsafe: {' '.join([str(item) for item in report])}")

print(safe_reports)



"""# 	sorted_lvs = sorted(report, reverse=False)
# 	
# 	safe = True
# 	tol  = True
# 	for i, (lvl, svl) in enumerate(zip(report[:-1], sorted_lvs[:-1])):
# 		print(lvl, svl, tol, safe)
# 		if lvl in report[:i]:
# 			if tol:
# 				if i > 0:
# 					if report[i+1] - report[i-1] > 3 or report[i+1] - report[i-1] == 0:
# 						print('1 nope')
# 						safe = False
# 						break
# 					else:
# 						tol = False
# 						continue
# 				else:
# 					print('2 nope')
# 					safe = False
# 					break
# 			else:
# 				print('3 nope')
# 				safe = False
# 				break
# 		else:
# 			if report[i+1] - lvl > 3 or lvl - report[i+1] == 0:
# 				
# 				if tol:
# 					if i > 0:
# 						if report[i+1] - report[i-1] > 3 or report[i+1] - report[i-1] == 0:
# 							print('4 nope')
# 							safe = False
# 							break
# 						else:
# 							tol = False
# 							continue
# 					else:
# 						print('5 nope')
# 						safe = False
# 						break
# 				else:
# 					print('6 nope')
# 					safe = False
# 					break
# 	if safe:
# 		safe_reports += 1
# 		print('safe:', ' '.join([str(lvl) for lvl in report]))
# 	else:
# 		print('unsafe:', ' '.join([str(lvl) for lvl in report]))
# 
# else:
# 	sorted_lvs = sorted(report, reverse=True)
# 	
# 	safe = True
# 	tol  = True
# 	for i, (lvl, svl) in enumerate(zip(report[:-1], sorted_lvs[:-1])):
# 		print(lvl, svl, tol, safe)
# 		if lvl in report[:i]:
# 			if tol:
# 				if i > 0:
# 					if report[i-1] - report[i+1] > 3 or report[i-1] - report[i+1] == 0:
# 						print('8 nope')
# 						safe = False
# 						break
# 					else:
# 						tol = False
# 						continue
# 				else:
# 					print('9 nope')
# 					safe = False
# 					break
# 			else:
# 				print('10 nope')
# 				safe = False
# 				break
# 		else:
# 			if lvl - report[i+1] > 3 or lvl - report[i+1] == 0:
# 				
# 				if tol:
# 					if i > 0:
# 						if report[i-1] - report[i+1] > 3 or report[i-1] - report[i+1] == 0:
# 							safe = False
# 							break
# 						else:
# 							tol = False
# 							continue
# 					else:
# 						safe = False
# 						break
# 				else:
# 					safe = False
# 					break
# 	
# 	if safe:
# 		safe_reports += 1
# 		print('safe:', ' '.join([str(lvl) for lvl in report]))
# 	else:
# 		print('unsafe:', ' '.join([str(lvl) for lvl in report]))

			if direction is not None:
				
		if report[-1] - report[0] > 0:
		#print('ascending')
		sorted_lvs = sorted(report, reverse=False)
		
		for i, (lvl, svl) in enumerate(zip(report[:-1], sorted_lvs[:-1])):
			if lvl != svl:
				if tolerate:
					modified = report.copy()
					del modified[i]
					if safe_report(modified, tolerate=False):
						return True
					else:
						modified = report.copy()
						modified.remove(svl)
						if safe_report(modified, tolerate=False):
							return True
						else:
							return False 
				else:
					return False
			else:
				if report[i+1] - lvl > 3 or lvl - report[i+1] == 0:
					if tolerate:
						modified = report.copy()
						del modified[i]
						if safe_report(modified, tolerate=False):
							return True
						else:
							modified = report.copy()
							del modified[i+1]
							if safe_report(modified, tolerate=False):
								return True
							else: 
								return False
					else:
						return False
	# descending order
	else:
		#print('descending')
		sorted_lvs = sorted(report, reverse=True)
		
		for i, (lvl, svl) in enumerate(zip(report[:-1], sorted_lvs[:-1])):
			#print(lvl, svl)
			if lvl != svl:
				if tolerate:
					modified = report.copy()
					del modified[i]
					if safe_report(modified, tolerate=False):
						return True
					else:
						modified = report.copy()
						modified.remove(svl)
						if safe_report(modified, tolerate=False):
							return True
						else:
							return False
				else:
					return False
			else:
				if lvl - report[i+1] > 3 or lvl - report[i+1] == 0:
					if tolerate:
						modified = report.copy()
						del modified[i]
						if safe_report(modified, tolerate=False):
							return True
						else:
							modified = report.copy()
							del modified[i+1]
							if safe_report(modified, tolerate=False):
								return True
							else:
								return False
					else:
						return False
	return True





"""