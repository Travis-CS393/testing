import Queue

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
		black_area = len(self.get_points("B", board))
		white_area = len(self.get_points("W", board))
		neutral = 0
	

		all_empty = self.get_points(" ", board)
		for intersection in all_empty:
			if ((not self.reachable(self.process_point(intersection), "W", board)) and (not self.reachable(self.process_point(intersection), "B", board))):
				neutral += 1
			elif (not self.reachable(self.process_point(intersection), "W", board)):
				black_area += 1
			elif (not self.reachable(self.process_point(intersection), "B", board)):
				white_area += 1
			else:
				neutral += 1

				
		if ((black_area + white_area + neutral) == (self.board_size * self.board_size)):
			return {"B": black_area, "W": white_area }
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

		####################################
		# Check board history validity 
		####################################

		# Board history len 1 means game just started 
		if (len(boards_arr) == 1):
			# Black must go first
			if (stone != "B"):
				return False

			# Board should contain no stones
			if (len(self.get_points(" ", boards_arr[0])) != (self.board_size * self.board_size)):
				return False
		

		# Board history has len 2, first is empty board, black moved once, it's white's turn 
		if (len(boards_arr) == 2):
			if (len(self.get_points(" ", boards_arr[1])) != (self.board_size * self.board_size)):
				return False
			if ((len(self.get_points("B", boards_arr[0])) > 1) or (len(self.get_points("W", boards_arr[0])) != 0)):
				return False
			if (stone != "W"):
				return False
			try_place = self.place(stone, point, boards_arr[0])
			if (try_place == "This seat is taken!"):
				return False
			else:			
				if ((not self.get_move_validity(boards_arr[0], try_place))):
					return False

		

		# Three boards in history, check that moves were valid between them
		if (len(boards_arr) == 3):

			# Check Ko rule, cannot repeat immediate position on play w/out pass
			if (boards_arr[0] == boards_arr[2]):
				return False

			# Game Over you cannot make a play because players have passed consecutively already
			if ((boards_arr[0] == boards_arr[1]) and (boards_arr[0] == boards_arr[2])):
				return False

			if ((boards_arr[1] == boards_arr[2]) and (len (self.get_points(" ", boards_arr[1])) == (self.board_size * self.board_size)) and (len (self.get_points(" ", boards_arr[2])) == (self.board_size * self. board_size)) and (len (self.get_points("W", boards_arr[0])) != 1)):
				return False

			# Board history contains dead stones
			if ((not self.check_dead_removed(boards_arr[0])) or (not self.check_dead_removed(boards_arr[1])) or (not self.check_dead_removed(boards_arr[2]))):
				return False

			# Board history contains other invalid moves
			if ((not self.get_move_validity(boards_arr[2], boards_arr[1])) or (not self.get_move_validity(boards_arr[1], boards_arr[0]))):
				return False

			# Check that players are alternating plays between "B" and "W"
			player_order = self.get_player_order(boards_arr, stone)
			if ((player_order[0] != player_order[2]) or (player_order[1] != player_order[3])):
				return False


			# See if the requested play is valid 
			try_place = self.place(stone, point, boards_arr[0])
			if (try_place == "This seat is taken!"):
				return False
			elif (not self.reachable(point, " ", try_place)):
				visited = [ [False] * self.board_size for row in range(self.board_size) ]
				neighbors = self.find_neighbors(point)
				q = Queue.Queue()
				for n in neighbors:
					if ((try_place[n[0]][n[1]] != stone) and (not self.reachable(n, " ", try_place))):
						q.put(n)

				while (q.empty() != True):
					check_point = q.get()
					try_place = self.remove(try_place[check_point[0]][check_point[1]], check_point, try_place)
					n_neighbors = self.find_neighbors(check_point)
					for n in n_neighbors:
						if ((try_place[n[0]][n[1]] == try_place[check_point[0]][check_point[1]]) and (not visited[check_point[0]][check_point[1]])):
							visited[check_point[0]][check_point[1]] = True
							q.put(n)

				if (not self.reachable(point, " ", try_place)):				
					return False
			else:
				if (not self.get_move_validity(boards_arr[0], try_place)):
					return False

			if (boards_arr[1] == try_place):
				return False

			if (self.check_alive_removed(boards_arr[2], boards_arr[1]) or self.check_alive_removed(boards_arr[1], boards_arr[0])):
				return False

		return True


	def get_move_validity(self, prev_board, curr_board):
		placed = []
		removed = []
		check_removed = []

		for row in range(self.board_size):
			for col in range(self.board_size):
				if (prev_board[row][col] != curr_board[row][col]):
					if (prev_board[row][col] == " "):
						placed.append([curr_board[row][col], (row,col)])
					elif ((prev_board[row][col] == "B") and (curr_board[row][col] == " ")):
						removed.append([curr_board[row][col], (row, col)])
					elif ((prev_board[row][col] == "W") and (curr_board[row][col] == " ")):
						removed.append([curr_board[row][col], (row, col)])	

		# Can only add one stone every turn or pass
		if (len(placed) > 1):
			return False

		# Cannot capture pieces if you didn't make a play 
		if (len(placed) == 0 and len(removed) != 0):
			return False

		# Pass move means boards are identical
		if (len(placed) == 0 and (prev_board != curr_board)):
			return False
		else:
			return True

		# Check if placing the play was valid
		try_place = self.place(placed[0][0], placed[0][1], prev_board)
		#if (not self.reachable(placed[0][1], " ", try_place)):
		#	return False

		visited = [ [False] * self.board_size for row in range(self.board_size) ]
		neighbors = self.find_neighbors(placed[0][1])
		q = Queue.Queue()
		for n in neighbors:
			if ((try_place[n[0]][n[1]] != placed[0][0]) and (not self.reachable(n, " ", try_place))):
				q.put(n)

		while (q.empty() != True):
			check_point = q.get()
			try_place = self.remove(try_place[check_point[0]][check_point[1]], check_point, try_place)
			check_removed.append([try_place[check_point[0]][check_point[1]], check_point])
			n_neighbors = self.find_neighbors(check_point)
			for n in n_neighbors:
				if ((try_place[n[0]][n[1]] == try_place[check_point[0]][check_point[1]]) and (not visited[check_point[0]][check_point[1]])):
					visited[check_point[0]][check_point[1]] = True
					q.put(n)

		# Check that all things that things that shouldn't be removed weren't removed
		if (removed != check_removed):
			return False

		# If still no liberties present after removal of dead, then invalid move 
		if (not self.reachable(placed[0][1], " ", try_place)):
			return False

		# See if there were other things that were removed for fun 
		test_board = self.place(placed[0][0], placed[0][1], prev_board)
		for s in removed:
			if (self.reachable(s[1], " ", test_board)):
				return False

		return True

	def check_removed(self, removed_arr, stone_point):
		for element in removed_arr:
			if (element == stone_point):
				return True
		return False

	def get_player_order(self, boards_arr, curr_player):
		
		last_move = curr_player
		
		order = []
		order.append(last_move)

		if (boards_arr[0] == boards_arr[1]):
			order.append(self.get_other_player(last_move))
			last_move = self.get_other_player(last_move)
		else:
			for row in range(self.board_size):
				for col in range(self.board_size):
					if (boards_arr[1][row][col] != boards_arr[0][row][col]):
						if (boards_arr[1][row][col] == " "):
							order.append(boards_arr[0][row][col])
							last_move = boards_arr[0][row][col]


		if (boards_arr[1] == boards_arr[2]):
			order.append(self.get_other_player(last_move))
			last_move = self.get_other_player(last_move)
		else:
			for row in range(self.board_size):
				for col in range(self.board_size):
					if (boards_arr[2][row][col] != boards_arr[1][row][col]):
						if (boards_arr[2][row][col] == " "):
							order.append(boards_arr[1][row][col])
							last_move = boards_arr[1][row][col]

		b2_black = len(self.get_points("B", boards_arr[2]))
		b2_white = len(self.get_points("W", boards_arr[2]))

		b1_black = len(self.get_points("B", boards_arr[1]))
		b1_white = len(self.get_points("W", boards_arr[1]))

		if((b1_black - b2_black) == 1):
			order.append("W")
		else:
			order.append("B")						

		return order

	def get_other_player(self, curr_player):
		if (curr_player == "B"):
			return "W"
		else:
			return "B"

	def check_dead_removed(self, board):
		for row in range(self.board_size):
			for col in range(self.board_size):
				if (board[row][col] == "B" and (not self.reachable((row, col), " ", board))):
					return False
				elif (board[row][col] == "W" and (not self.reachable((row, col), " ", board))):
					return False

		return True 

	def check_alive_removed(self, prev_board, curr_board):
		placed = []
		removed = []
		for row in range(self.board_size):
			for col in range(self.board_size):
				if ((prev_board[row][col] == "B") and (curr_board[row][col] == " ")):
					removed.append((row, col))
				elif ((prev_board[row][col] == "W") and (curr_board[row][col] == " ")):
					removed.append((row, col))
				elif (prev_board[row][col] == " " and (curr_board[row][col] != " ")):
					placed.append([curr_board[row][col],(row, col)])

		if (len(placed) != 0):
			test_board = self.place(placed[0][0], placed[0][1], prev_board)
			for s in removed:
				if (self.reachable(s, " ", test_board)):
					return True

		return False

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