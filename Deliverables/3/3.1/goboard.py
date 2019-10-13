import json
import sys

class GoBoardComponent():
	def __init__(self, go_board=None, statements=None, responses=None, points=None):
		"""
		This class implements a Go board component that takes in a 19 x 19 go board and a
		statement from STDIN in the form [Board, Statement], and returns responses
		according to the following statements:

		Query Statements:
			["occupied?", Point] - returns true if a Stone at point, else false
			["occupies?", Stone, Point] - returns true if Stone at point, else false
			["reachable?", Point, MaybeStone] - returns true if exists path of vertical or horizontal
												adjacent points of same Stone from Stone at Point to MaybeStone,
												else false

		Command Statements:
			["place", Stone, Point] - returns updated Board with Stone at Point, error if invalid move
									  "This seat is taken!"
			["remove", Stone, Point] - returns updated Board with Stone removed from Point, error if invalid move
									  "I am just a board! I cannot remove what is not there"
			["get-points", MaybeStone] - returns JSON array of Points that has stored all Point positions of the given
									   MaybeStone input

		The 19 x 19 board contains only rows of MaybeStone where each row has 19 of MaybeStone,
		which can be Stone or Empty ("").

		Stone is one of "B" or "W", depending on whether it is a black or white stone.

		Point is represented by "N-N", where N is a natural number from 1 - 19, and represent
		coordinates for the Go coordinate system (1-1 top left corner, 19-19 bottom right corner)
		"""
		self.go_board = [ [""] * 19 for row in range(19)] if go_board is None else go_board
		self.statements = [] if statements is None else statements
		self.responses = [] if responses is None else responses
		self.points = [] if points is None else points



	############################################
	# PROCESS INPUT
	############################################

	# Reads [Board, Statement] JSON array from STDIN and
	# stores Board to self.go_board and Statements to self.statements
	def read_input(self):
		inputs = []
		reading_frame = ""
		for line in sys.stdin.readlines():
			reading_frame += (line.replace("\n","")).lstrip()
			try:
				while(len(reading_frame) >= 1):
					json_obj, end_idx = json.JSONDecoder().raw_decode(reading_frame)
					inputs.append(json_obj)
					reading_frame = reading_frame[end_idx:].lstrip()
			except ValueError:
				pass

		if(len(inputs[0]) != 2):
			raise Exception("Input must be in the form [Board, Statements]")

		if(self.check_board(inputs[0][0])):
			self.go_board = inputs[0][0]
		else:
			raise Exception("Go board must be 19 x 19 and hold only MaybeStones")

		if(self.check_statements(inputs[0][1])):
			self.statements = inputs[0][1]
		else:
			raise Exception("Statements must be Query{ occupied?, occupies?, reachable?} or Command{ place, remove, or get-points}. Check inputs to query or command.")

	# Iterates through statements and stores response from each corresponding action
	def execute_statements(self):
		f = open("wetried.txt","w+")

		for statement in self.statements:
			if(statement[0] == "occupied?"):
				f.write(str(self.occupied(statement[1])) + "*")
			elif (statement[0] == "occupies?"):
				f.write(str(self.occupies(statement[1], statement[2])) + "*")
			elif (statement[0] == "reachable?"):
				f.write(str(self.reachable(statement[1], statement[2])) + "*")
			elif (statement[0] == "place"):
				f.write(str(self.place(statement[1], statement[2])) + "*")
			elif (statement[0] == "remove"):
				f.write(str(self.remove(statement[1], statement[2])) + "*")
			elif (statement[0] == "get-points"):
				f.write(str(self.get_points(statement[1])) + "\n")
			else:
				raise Exception("Invalid Statement: Not a query or a command.")

		f.close()



	###########################################
	# HELPER FUNCTIONS
	###########################################

	# Converts point from "N-N" to indices
	def process_point(self,point):
		idx = point.split("-")
		for i in range(len(idx)):
			idx[i] = int(idx[i])

		return idx[0] - 1, idx[1] - 1

	# Adds "N-N" point position to self.points array
	def add_point(self, maybe_stone, x, y):
		str_point = str(x + 1) + "-" + str(y + 1)
		self.points.append(str_point)

	def responses_cat(self):
		f = open("wetried.txt","r")
		if f.mode == "r":
			contents = f.read()

		contents = contents.split("*")

		for element in contents:
			try:
				json_obj, end_idx = json.JSONDecoder().raw_decode(element.replace("\'","\""))
				self.responses.append(json_obj)
			except ValueError:
				pass

		return self.responses



	############################################
	# QUERIES
	###########################################

	# Occupied takes a point and returns True if
	# board at that point is not empty stone, else False
	def occupied(self, point):
		x, y = self.process_point(point)

		return True if (self.go_board[x][y] != "") else False

	# Occupies takes a point and returns True if
	# board at that point has that stone, else False
	def occupies(self, point, stone):
		x, y = self.process_point(point)

		return True if (self.go_board[x][y] == stone) else False

	# Return true if there is a path of adjacent points to Point
	# that have the same kind of MaybeStone as the given point and
	# the path reaches the given MaybeStone, else False
	def reachable(self, point, maybe_stone):
		pass



	###########################################
	# COMMANDS
	###########################################

	# Places a stone at the given point on go_board if not occupied
	def place(self, stone, point):
		if(self.occupied(point)):
			return "This seat is taken!"
		else:
			x, y = self.process_point(point)

			#temp_board = list(self.go_board)
			#temp_board[x][y] =
			self.go_board[x][y] = stone
			return self.go_board

	# Removes a stone from given point on go_board if occupied
	def remove(self, stone, point):
		if(self.occupied(point) == False):
			return "I am just a board! I cannot remove what is not there!"
		else:
			x, y = self.process_point(point)
			self.go_board[x][y] = ""
			return self.go_board

	# Returns array of points that maybe_stone occupies on go_board
	def get_points(self, maybe_stone):
		for x in range(len(self.go_board)):
			for y in range(len(self.go_board[0])):
				if(self.go_board[x][y] == maybe_stone):
					self.add_point("", x, y)

		# Gets points and resets self.points
		points = sorted(self.points)
		self.points = []

		return points



	################################################
	# TYPE ASSERTIONS PREDICATES
	################################################

	# Point must be in the format "N-N" where N is a value 1 to 19
	def check_point(self, point):
		parsed_point = point.split("-")
		if(len(parsed_point) == 2):
			pos_set = {"1", "2", "3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"}
			if( (parsed_point[0] in pos_set) and (parsed_point[1] in pos_set) ):
				return True
		return False


	# Stone must be "B" or "W"
	def check_stone(self, stone):
		if( (stone == "B") or (stone == "W") ):
			return True
		return False

	# MaybeStone must be a Stone or ""
	def check_maybe_stone(self, maybe_stone):
		if( self.check_stone(maybe_stone) or (maybe_stone == "") ):
			return True
		return False

	# Board must be 19 x 19 represented by an array of 19 rows
	# where each row contains 19 elements of type MaybeStone
	def check_board(self, board):
		if((len(board) == 19) and (len(board[0]) == 19)):
			check_all_stones = True
			for row in range(len(board[0])):
				for col in range(len(board[0][1])):
					if(self.check_maybe_stone(board[row][col]) == False):
						check_all_stones = False
			return check_all_stones
		else:
			return False

	# Statements must be array of one of
	# ["occupied?", Point], ["occupies?", Point, Stone], ["reachable?", Point, MaybeStone]
	# ["place", Stone, Point], ["remove", Stone, Point], ["get-points", MaybeStone]
	# with proper inputs for Point, Stone, and MaybeStone
	def check_statements(self, statements):
		for statement in statements:
			if(len(statement) == 2):

				if(statement[0] == "occupied?"):
					if(self.check_point(statement[1]) == False):
						print(1)
						return False
				elif(statement[0] == "get-points"):
					if(self.check_maybe_stone(statement[1]) == False):
						print(2)
						return False
				else:
					print("hi")
					return False

			elif(len(statement) == 3):

				if((statement[0] == "place") or (statement[0] == "remove")):
					if((self.check_stone(statement[1]) == False) or (self.check_point(statement[2]) == False)):
						print(4)
						return False
				elif(statement[0] == "occupies?"):
					if((self.check_point(statement[1]) == False) or (self.check_stone(statement[2]) == False)):
						print(5)
						return False
				elif(statement[0] == "reachable?"):
					if((self.check_point(statement[1]) == False) or (self.check_maybe_stone(statement[2]) == False)):
						print(6)
						return False
				else:
					print(7)
					return False

			else:
				print(8)
				return False

		return True
