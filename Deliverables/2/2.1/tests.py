import unittest
import BackEndComponent
import json

def test1():
	special_obj = json.load(sys.stdin)

    back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)

	sys.stdout.write(sorted_ten[0])

def testOne():
	with open('input1.json') as file:
		input = json.load(file)
	with open('output1.json') as file:
		output = json.load(file)

	back_service = BackEndComponent()
	sorted_ten = back_service.sort(input)
	assert(sorted_ten == output)
