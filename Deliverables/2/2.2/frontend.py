import json
import sys
sys.path.append('../')
from backend import BackEndComponent

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

	"""
	# Reads special JSON objects from .json file
	def read(self, filename):
		with open(filename) as file:
			data = json.load(file)
			for j in data:
				self.lst.append(j)


	# Reads array of special JSON objects with STDIN
	def read(self):
		self.lst = json.load(sys.stdin)
	"""

	# Reads special JSON objects with STDIN from command line
	def readCL(self):
		for line in sys.stdin.readlines():
			if line != "\n":
				self.lst.append(json.loads(line))

	# Reads special JSON objects with STDIN from file
	def readFile(self, filename):
		with open(filename) as f:
			for line in f:
				if line != "\n":
					self.lst.append(json.loads(line))


	# Partitions the list of special JSON objects into lists of 10
	def partition(self):
		start = 0
		end = 10
		tens = []
		while end <= len(self.lst):
			tens.append(self.lst[start:end])
			start += 10
			end += 10

		return tens

	# Sends each set of 10 special JSON objects to back-end for sorting
	# and stores sorted list in to array or arrays of special JSON objects
	def process(self):
		sorted_lsts = []
		partitioned_lst = self.partition(self.lst)
		back_service = BackEndComponent()
		for lst in partitioned_lst:
			sorted_lsts.append(back_service.sort(lst))

		#sys.stdout.write(sorted_lsts)
		print(sorted_lsts)
