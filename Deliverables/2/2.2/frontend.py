from __future__ import print_function
from backend import BackEndComponent
import json
import sys


class FrontEndComponent():
	def __init__(self, lst=None):
		"""
		This class implements a front-end component that reads in special JSON
		objects from STDIN, passes lists of 10 JSON objects to the back-end
		component to be sorted, and returns the array of arrays of 10 sorted
		special JSON objects with STDOUT.

		Arguments:
			lst (list): List of the special JSON objects. Used to partition
			and send the special JSON objects in lists of 10 to back-end
			component for sorting.
		"""

		self.lst = [] if lst is None else lst

	# Reads special JSON objects from STDIN into self.lst
	def read(self):
		reading_frame = ""
		for line in sys.stdin.readlines():
			reading_frame += (line.replace("\n","")).lstrip()
			try:
				while(len(reading_frame) >= 1):
					json_obj, end_idx = json.JSONDecoder().raw_decode(reading_frame)
					self.lst.append(json_obj)
					reading_frame = reading_frame[end_idx:].lstrip()
			except ValueError:
				pass

	# Partitions the list of special JSON objects into lists of 10
	def partition(self):
		start = 0
		end = 10
		sets_of_tens = []
		while end <= len(self.lst):
			sets_of_tens.append(self.lst[start:end])
			start += 10
			end += 10

		return set_of_tens


def test_driver():
	sorted_lsts = list()

	tester = FrontEndComponent()
	tester.read()
	partitioned_lst = tester.partition()
	
	back_service = BackEndComponent()
	for lst in partitioned_lst:
		sorted_lsts.append(json.loads(back_service.sort(lst)))

	print(json.dumps(sorted_lsts), end='')

test_driver()
