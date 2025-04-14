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
			if tolerate: # needed for part 2
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
			if tolerate: # needed for part 2
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
				if tolerate: # needed for part 2
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


# Part 1
safe_reports = 0
for report in reports:
	
	if safe_report(report, tolerate=False):
#		print(f"safe: {' '.join([str(item) for item in report])}")
		safe_reports += 1
	else:
		continue
#		print(f"unsafe: {' '.join([str(item) for item in report])}")

print(f'Part 1: {safe_reports}')


safe_reports = 0
for report in reports:
	if safe_report(report, tolerate=True):
#		print(f"safe: {' '.join([str(item) for item in report])}")
		safe_reports += 1
	else:
		continue
#		print(f"unsafe: {' '.join([str(item) for item in report])}")

print(f'Part 2: {safe_reports}')