import unittest
import BackEndComponent
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

def test_driver():
	special_obj = []
	count = 0
	for line in sys.stdin.readlines():
		if count < 10:
			special_obj.append(json.loads(line))
			count += 1
		else:
			break

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)
     
    print("hello")
	print(sorted_ten)

test_driver()
