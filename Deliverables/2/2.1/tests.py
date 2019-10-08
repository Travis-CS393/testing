from __future__ import print_function
from backend import BackEndComponent
import json
import sys

"""
# Testing Input and Output Files
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

def test_driver_13():
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


def test_driver():
	special_obj = []
	reading_frame = ""
	for line in sys.stdin.readlines():
		reading_frame += line.replace("\n","")
		try:
			while(len(reading_frame) >= 1):
				json_obj, end_idx = json.JSONDecoder().raw_decode(reading_frame)
				if(len(special_obj) < 10):
					special_obj.append(json_obj)
					reading_frame = reading_frame[end_idx:].lstrip()
				else:
					break
		except ValueError:
			pass
	back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)

	print(json.dumps(sorted_ten), end='')

test_driver()
