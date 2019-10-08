from __future__ import print_function
from backend import BackEndComponent
import json
import sys

def test1():
	special_obj = json.load(sys.stdin)
	back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)

	sys.stdout.write(sorted_ten[0])

def testOne():
	with open('input1') as file:
		input = json.load(file)
	with open('output1') as file:
		output = json.load(file)

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(input)
	assert(sorted_ten == output)

def testTwo():
	with open('input2') as file:
		input = json.load(file)
	with open('output2') as file:
		output = json.load(file)

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(input)
	assert(sorted_ten == output)

def testThree():
	with open('input3') as file:
		input = json.load(file)
	with open('output3') as file:
		output = json.load(file)

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(input)
	assert(sorted_ten == output)

def testFour():
	with open('input4') as file:
		input = json.load(file)
	with open('output4') as file:
		output = json.load(file)

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(input)
	assert(sorted_ten == output)

def testFive():
	with open('input5') as file:
		input = json.load(file)
	with open('output5') as file:
		output = json.load(file)

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(input)
	assert(sorted_ten == output)

"""
def test_driver():
	special_obj = []
	all_obj = ""
	count = 0
	for line in sys.stdin.readlines():
		if count < 10:
			all_obj = all_obj + line
			count += 1
		else:
			break

	all_obj = all_obj.replace("\n"," ")
	while all_obj:
		try:
			data, idx = json.JSONDecoder().raw_decode(all_obj)
			special_obj.append(data)
			all_obj = all_obj[idx:]
		except ValueError:
			break 
	
	back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)

	print(sorted_ten, end='')
"""


def test_driver():
	special_obj = []
	count = 0
	temp = ""
	hold = sys.stdin.readlines()
	for line in hold:			
		rmvnl = line.replace("\n","")
		try:
			while(rmvnl):
				data, idx = json.JSONDecoder().raw_decode(temp + rmvnl)
				special_obj.append(data)
				if (idx == len(rmvnl)):
					break
				temp = temp[idx+1:]
				rmvnl = rmvnl[idx+1:]
		except ValueError:
			temp = temp + line
	back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)

	print(json.dumps(sorted_ten), end='')


"""
def test_driver():
	special_obj = []
	count = 0
	running = True
	temp = ""
	hold = []
	allines = sys.stdin.readlines()
	for i in range(len(allines)):
		if allines[i] != ' \n':
			hold.append(allines[i])

	for line in hold:
		ln = line.replace("\n","")
		try:
			while(running):
				ln = temp + ln
				data, idx = json.JSONDecoder().raw_decode(ln)
				special_obj.append(data)
				ln = ln[idx:]
				temp = ""
				if (idx == len(ln)):
					running = False

		except ValueError:
			temp = temp + ln

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)
	print(json.dumps(sorted_ten), end='')
"""

test_driver()
