import queue as Queue

class GoBoardComponent():
	def __init__(self, board_size=None):
		"""
		This class implements a Go board component that returns a response 
		based on a statement executed on a given 19 x 19 go board. The 
		statements are as follows:

		Query Statements:
			["occupied?", Point] - returns True if a Stone at point, else False
			["occupies?", Stone, Point] - returns True if stone at point, else False
			["reachable?", Point, MaybeStone] - returns True if exists path of vertical
						or horizontal adjacent points of same Stone form Stone at Point to
						Maybestone, else False. Implemented BFS with queue

		Command Statements:
			["place", Stone, Point] - returns updated Board with Stone at Point, error if invalid move 
						"This seat is taken!"
			["remove", Stone, Point] - returns updated Board with Stone removed from Point, error if invalid 
						"I am just a board! I cannot remove what is not there!"
			["get-points", MaybeStone] - returns array of Points that has stored all Point positions of the 
						given MaybeStone input in the go board, sorted in increasing lexicographic order

		A Stone is one of "B" or "W", depending on whether it is a black or white stone. 
		
		A MaybeStone is one of Stone or Empty (" ").

		The 19 x 19 board contains only rows of MaybeStone where each row has 19 of MaybeStone. 

		A Point is represented by "N-N", where N is a natural number from 1-19, and represents the 
		cooordinates for the Go coordinate system (1-1 top left corner, 19-19 bottom right corner).
		"""
		self.board_size = 19 if board_size is None else board_size

	########################################
	# INPUT DRIVER
	########################################

	# Returns appropriate response given a valid input form 
	def get_response(self, input):
		if (len(input) == self.board_size):
			return self.get_score(input)
		elif ((len(input) == 2) and (input[1] == "pass")):
			return self.pass_turn(input[0])
		elif ((len(input) == 2)):
			return self.get_validity(input[0],self.process_point(input[1][0]),input[1][1])
		else:
			raise Exception("Invalid input has no appropriate response.")

	# Returns the score of "B" and "W" given a final board state.
	def get_score(self, board):
		black_area = 0
		white_area = 0
		neutral = 0

		for row in range(self.board_size):
			for col in range(self.board_size):
				if ((not self.reachable((row, col),"W",board)) and (not self.reachable((row, col), "B", board))):
					neutral += 1
				elif ((board[row][col] == " ") and (not self.reachable((row, col),"W", board))):
					black_area += 1
				elif ((board[row][col] == " ") and (not self.reachable((row, col), "B", board))):
					white_area += 1
				else:
					neutral += 1

		if ((black_area + white_area + neutral) == (self.board_size * self.board_size)):
			return {"B": len(self.get_points("B",board)) + black_area, "W": len(self.get_points("W",board)) +white_area }
		else:
			raise Exception("Invalid scoring, sum of black, white, and neutral points must be total intersections.")



	########################################
	# RULE CHECKER INVARIANTS
	#######################################
	"""
	1. Go is a game between two players, called Black and White.
		- Choice of who goes first: nigiri
	2. Go is played on a plane grid of 19 horizontal and 19 verical lines, called a board.
		- Points on the boards are intersection so fthe lines. 
		- Points adjacent if they are distinct and connected by a horizontal or
		  vertical line with no other intersections between them. 
	3. Go is played with playing tokens known as stones. Each player has at their disposal
	   an adequate supply of stones of their color. 
	4. At any time in the game, each intersection on the board is in one and only one
	   of the following tree states:
	   	- Empty
	   	- Occupied by Black stone
	   	- Occupied by White stone
	   and a position indicates the state of each intersection.
	   - Two stones of the same color or empty are connected if draw path 
	     only draws with same stone through adjacents
	   - Liberties are empty adjacent to connected chains 
	 5. At the beginning of the game, the board is empty. 
	 6. Black moves first. The players alternate thereafter.

	 7. Moves are either "pass" or Play 
	 	-
	 8. A Play is illegal if it would repeat a previously played position.  Recreation. 

	 9. The game ends when both players have passed consecutively. 
	 10. The player with the higher score wins, otherwise the game is a draw. 

	"""
	# Returns the validity of a Move given a [Stone, [Point, Boards]] valid input
	def get_validity(self, stone, point, boards_arr):

		# If no one has moved then board should be all Empty
		# If only one move in history, boards should be last move and Empty
		if ((len(boards_arr) == 1 and (len(self.get_points(" ", boards_arr[0])) != (self.board_size * self.board_size))) or \
			(len(boards_arr) == 2 and (len(self.get_points(" ", boards_arr[1])) != (self.board_size * self.board_size)))):
			return False

		# Black goes first
		if ((len(boards_arr) == 1) and (stone == "W")):
			return False

		# Game Over you cannot make a play because players have passed consecutively already
		if ((len(boards_arr) == 3) and (boards_arr[0] == boards_arr[1]) and (boards_arr[0] == boards_arr[2])):
			return False

		# Check board history validity 

		#####################################
		# SEE IF YOU CAN PLACE STONE AT POINT
		#####################################
		try_place = self.place(stone, point, boards_arr[0])

		# Another stone already occupies that point
		if (try_place == "This seat is taken!"):
			return False

		# You can't place a stone if it won't have any liberties after turn
		# Remove all dead pieces to get new liberties intersections 
		neighbors = self.find_neighbors(point)
		for i in neighbors:
			if (try_place[i[0]][i[1]] != stone and (not self.reachable(point, " ", try_place))):
				try_place = self.remove(stone, point, try_place)

		# If no liberties after removal, then invalid move
		if (not self.reachable(point, " ", try_place)):
			return False

		# Check Ko


		return True 



	########################################
	# QUERIES
	########################################

	# Occupied takes an index tuple and returns True 
	# if board at that point is not empty stone " ", else False
	def occupied(self, idx, board):
		return (board[idx[0]][idx[1]] != " ")

	# Occupies takes an index tuple and returns True if 
	# board at that point has that Stone, else False
	def occupies(self, stone, idx, board):
		return (board[idx[0]][idx[1]] == stone)

	# Return True if there is a path of adjacent ponts to Point
	# that have the same kind of MaybeStone as the given point and
	# the path reaches the given MaybeStone, else False
	def reachable(self, idx, maybe_stone, board):
		visited = [ [False] * 19 for row in range(19) ]

		start_type = board[idx[0]][idx[1]]
		if (start_type == maybe_stone):
			return True

		q = Queue.Queue()
		q.put(idx)

		while (q.empty() != True):
			check_point = q.get()
			if (visited[check_point[0]][check_point[1]] == False):
				visited[check_point[0]][check_point[1]] = True
				neighbors = self.find_neighbors(check_point)
				for n in neighbors:
					row = n[0]
					col = n[1]
					if (board[row][col] == maybe_stone):
						return True
					if (board[row][col] == start_type):
						q.put(n)
		return False

	###########################################
	# COMMANDS
	###########################################

	# Places a stone at the given point on go_board if not occupied
	def place(self, stone, idx, board):
		if (self.occupied(idx, board)):
			return "This seat is taken!"
		else:
			board[idx[0]][idx[1]] = stone
			return board

	# Removes a stone form given poin on go_board if occupied
	def remove(self, stone, idx, board):
		if ((self.occupied(idx, board) == False) or (self.occupies(stone, idx, board) == False)):
			return "I am just a board! I cannot remove what is not there!"
		else:
			board[idx[0]][idx[1]] = " "
			return board

	# Pass turn 
	def pass_turn(self, player):
		return True

	# Returns array of points that maybe_stone occupies on go_board
	def get_points(self, maybe_stone, board):
		points = []
		for x in range(self.board_size):
			for y in range(self.board_size):
				if(board[x][y] == maybe_stone):
					points.append(self.get_str_point(y, x))

		# Gets pints and resets self.points
		points = sorted(points)
		return points




	############################################
	# HELPER FUNCTIONS
	############################################

	# Converts point from "N-N" to indices
	def process_point(self, point):
		idx = point.split("-")
		for i in range(len(idx)):
			idx[i] = int(idx[i])

		return idx[1] - 1, idx[0] - 1

	# Converts indices to "N-N" point position 
	def get_str_point(self, x, y):
		return str(x + 1) + "-" + str(y + 1)

	# Finds all the adjacent neighbors to a given point
	def find_neighbors(self, idx):
		neighbors = []
		x_pos = [-1, 0, 1, 0]
		y_pos = [0, 1, 0, -1]

		for i in range(4):
			n_x = idx[0] + x_pos[i]
			n_y = idx[1] + y_pos[i]
			if ((n_x >= 0 and n_x <= 18) and (n_y >= 0 and n_y <= 18)):
				point_idx = (n_x , n_y)
				neighbors.append(point_idx)

		return neighbors