import json
import yaml

class BackEndComponent():
	def __init__(self):
		"""
		This class implements a back-end component that takes in a list
		of 10 special JSON objects from a front-end component, sorts the JSON objects in
		ascending order, and returns the sorted list of 10 special JSON objects to the
		front-end component.

		Special JSON objects are sorted with the following ascending hierarchy:
		    1. Numbers least to greatest.
		    2. Strings in increasing lexographical order.
		    3. Objects sorted by the order of their name field values.
		"""

	# Sorts special JSON objects of type JSON objects by hierarchy
	def obj_sort(self, obj_lst):
		next_layer = []
		for i in range(len(obj_lst)):
			check_obj = obj_lst[i]
			layer_count = 1
			while isinstance(check_obj["name"], dict):
				layer_count += 1
				check_obj = check_obj["name"]
			next_layer.append((layer_count, isinstance(check_obj["name"],str), check_obj["name"], i))
		next_layer = sorted(next_layer, key=lambda cond:(cond[0], cond[1], cond[2]))

		sorted_obj_lst = []
		for i in range(len(obj_lst)):
			sorted_obj_lst.append(obj_lst[next_layer[i][3]])

		return sorted_obj_lst

    # Sorts and returns inputted list of 10 special JSON objects
	def sort(self, lst):
		num_lst = []
		str_lst = []
		obj_lst = []
		for s_obj in lst:
			if isinstance(s_obj, int):
				num_lst.append(s_obj)
			elif (isinstance(s_obj, str) or isinstance(s_obj, unicode)):
				str_lst.append(s_obj)
			elif isinstance(s_obj, dict):
				obj_lst.append(s_obj)
			else:
				print("Type Error: Special JSON object is one of int, str, or JSON obj")

		# return sorted(num_lst) + sorted(str_lst) + self.obj_sort(obj_lst)
		num_lst = sorted(num_lst)
		#stri = sorted(str_lst)
		#slist = json.dumps(stri)
		#obj = self.obj_sort(obj_lst)
		#olist = json.dumps(obj)
		str_lst = sorted(str_lst)
		obj_lst = self.obj_sort(obj_lst)

		sorted_lst = []
		for element in num_lst:
			sorted_lst.append(element)

		for element in str_lst:
			sorted_lst.append(json.dumps(element))

		for element in obj_lst:
			sorted_lst.append(json.dumps(element))

		return sorted_lst
