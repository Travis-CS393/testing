import queue as Queue
import copy

class GoPlayerCapture():
	def __init__(self, player_name=None, player_stone=None, board_size=None, strategy=None):
        """
        This class implements a Go Player component that will make 
        a legal move as a given stone based on its board history. 

        It will internally store the player's name, stone color, and have
        operations to check that the next move it makes is legal while
        its board history is valid. 

        If the history is invalid, player  will reply with "This history makes no sense!". 

        In the case that it is valud, the player will make a play to capture if 
        the number of liberties of opponent piece is less than our strategy n, otherwise
        it will make a play at the legal smallest col index primarily and legal smallest 
        row index primarily. If there are no legal moves, it will pass. 
        """
        self.player_name = "no name" if player_name is None else player_name
        self.player_stone = "B" if player_stone is None else player_stone
        self.board_size = 19 if board_size is None else board_size
        self.rules = GoBoard(self.board_size)
        self.strategy = 1 if strategy is None else strategy

        ##############################
		# GAMEPLAY RESPONSES DRIVER
		##############################

		# Returns appropriate play response given valid input 
		# Input is one of:
		#   - ["register"]
		#   - ["receive-stones", "B"], ["receive-stones", "W"]
		#   - ["make-a-move", Boards], where Boards is of length 1,  2, or 3 and
		#     describes the gameplay history for past three moves 
		def get_response(self, input):
		    if ((len(input) == 1) and (input == ["register"])):
		        return self.register()
		    elif ((len(input) == 2) and (input[0] == "receive-stones") and \
		        ((input[1] == "B") or (input[1] == "W"))):
		        return self.receive_stone(input[1])
		    elif ((len(input) == 2) and (input[0] == "make-a-move") and \
		        ((len(input[1]) == 1) or (len(input[1]) == 2) or (len(input[1]) == 3))):
		        return self.make_move(input[1])
		    else:
		        raise Exception("Invalid input has no appropriate response.")


	    # Returns the default player name, "no name"
	    def register(self):
	        return self.player_name

	    # Assigns player a stone 
	    def receive_stone(self, stone):
	        self.player_stone = stone

	    # Makes a legal move if possible, given board history 
	    def make_move(self, history):
	        if (self.rules.validate_history(self.player_stone, history)):
	            return self.find_capture(self.player_stone, history)
	        else:
	            return "This history makes no sense!"

		# Find first col, row point play that captures piece within strategy n moves
	    def find_capture(self, stone, history):

	        all_opponent = self.smallest_colrow(self.rules.get_points(self.rules.get_opponent(stone), history[0]))

	        for point in all_opponent:
	            col = point[0]
	            row = point[1]  
	            liberties, point = self.find_liberties((col, row), history[0])

	            try_place = self.rules.place(stone, point, history[0])

	            # Remove stones captured after play
	            visited = [ [False] * self.board_size for row in range(self.board_size) ]
	            neighbors = self.rules.find_neighbors(point)
	            q = Queue.Queue()
	            for n in neighbors:
	                if ((try_place[n[0]][n[1]] != stone) and (not self.rules.reachable(n, " ", try_place))):
	                    visited[n[0]][n[1]] = True
	                    q.put(n)

	            while (q.empty() != True):
	                check_point = q.get()
	                try_place = self.rules.remove(try_place[check_point[0]][check_point[1]], check_point, try_place)
	                n_neighbors = self.rules.find_neighbors(check_point)
	                for n in n_neighbors:
	                    if ((try_place[n[0]][n[1]] == self.rules.get_opponent(stone)) and (not visited[n[0]][n[1]])):
	                        visited[n[0]][n[1]] = True
	                        q.put(n)

	            if (len(history) == 3):
	                if (try_place != history[1]):
	                    if (liberties <= self.strategy):
	                        return self.rules.idx_to_point(point[1], point[0])

	            elif (len(history) != 3):
	                if (liberties <= self.strategy):
	                        return self.rules.idx_to_point(point[1], point[0])


	        return self.find_move(stone, history)

	    # Implements BFS to find number of liberties of stone at point,
	    # Returns the liberties, and min (col,row) point to start capture
	    def find_liberties(self, idx, board):
	        visited = [ [False] * self.board_size for row in range(self.board_size)]
	        liberties = 0
	        place_points = []

	        q = Queue.Queue()
	        q.put(idx)

	        while (q.empty() != True):
	            check_point = q.get()
	            if (board[check_point[0]][check_point[1]] == " "):
	                liberties += 1
	                place_points.append(check_point)
	            elif (self.rules.reachable(check_point, " ", board)):
	                neighbors = self.rules.find_neighbors(check_point)
	                for n in neighbors:
	                    if ((board[n[0]][n[1]] != self.player_stone) and (not visited[n[0]][n[1]])):
	                        visited[n[0]][n[1]] = True
	                        q.put(n)

	        place_points = sorted(place_points)
	        return liberties, place_points[0]

	    # Finds first legal move in min col, row coordinates, otherwise "pass"
	    def find_move(self, stone, history):

	        # Traverses matrix by column first
	        for row in range(self.board_size):
	            for col in range(self.board_size):

	                if (history[0][col][row] == " "):
	                    try_place = self.rules.place(stone, (col, row), history[0])

	                    # Remove stones captured after play
	                    visited = [ [False] * self.board_size for row in range(self.board_size) ]
	                    neighbors = self.rules.find_neighbors((col, row))
	                    q = Queue.Queue()
	                    for n in neighbors:
	                        if ((try_place[n[0]][n[1]] != stone) and (not self.rules.reachable(n, " ", try_place))):
	                            visited[n[0]][n[1]] = True
	                            q.put(n)

	                    while (q.empty() != True):
	                        check_point = q.get()
	                        try_place = self.rules.remove(try_place[check_point[0]][check_point[1]], check_point, try_place)
	                        n_neighbors = self.rules.find_neighbors(check_point)
	                        for n in n_neighbors:
	                            if ((try_place[n[0]][n[1]] == self.rules.get_opponent(stone)) and (not visited[n[0]][n[1]])):
	                                visited[n[0]][n[1]] = True
	                                q.put(n)

	                    # Continue if this move would violate Ko rule
	                    if (len(history) == 3):
	                        if (try_place != history[1]):
	                            if (self.rules.reachable((col, row), " ", try_place)):
	                                return self.rules.idx_to_point(row, col)

	                    elif (len(history) != 3):
	                        if (self.rules.reachable((col, row), " ", try_place)):
	                            return self.rules.idx_to_point(row, col)

	        return "pass"

	    def smallest_colrow(self, points):
	        idx_arr = []
	        for p in points:
	            col, row = self.rules.point_to_idx(p)
	            idx_arr.append((col, row))

	        idx_arr = sorted(idx_arr)
	        return idx_arr


class GoPlayerMin():
	def __init__(self, player_name=None, player_stone=None, board_size=None):
		"""
		This class implements a Go Player component that will make
		a legal move as a given stone given the board history.

		It will internally store the player name, player stone, and have
		operations to check that legal moves are valid. In the case that it is valid
		the player will play at the legal smallest col index primarily and
		legal smallest row index primarily. If there are no legal moves, it will
		pass. If the history is invalid, it will reply with "This history makes no sense!".

		If there are two consecutive passes, the player is given the score and the winner
		of the game.
		"""
		self.player_name = "no name" if player_name is None else player_name
		self.player_stone = "B" if player_stone is None else player_stone
		self.board_size = 19 if board_size is None else board_size
		self.rules = GoBoard(self.board_size)



	################################
	# GAMEPLAY RESPONSES
	################################

	# Returns appropriate responses given valid input
	def get_response(self, input):
		if ((len(input) == 1) and (input == ["register"])):
			return self.register()
		elif ((len(input) == 2) and (input[0] == "receive-stones") and ((input[1] == "B") or (input[1] == "W"))):
			self.receive_stone(input[1])
		elif ((len(input) == 2) and (input[0] == "make-a-move") and ((len(input[1]) == 1) or (len(input[1]) == 2) or (len(input[1]) == 3))):
			return self.make_move(input[1])
		else:
			raise Exception("Invalid input has no appropriate response")

	# Internally stores player name, default "no name"
	def register(self):
		return self.player_name

	# Initiates game, assigns player a stone and clears previous game board
	def receive_stone(self, stone):
		self.player_stone = stone

	# Update go_board state if board history is valid
	def make_move(self, boards_arr):
		if (self.rules.validate_history(self.player_stone, boards_arr)):
			return self.find_move(self.player_stone, boards_arr[0], boards_arr)
		else:
			return "This history makes no sense!"

	# Finds first valid move in a min col, row coordinate, otherwise "pass"
	def find_move(self, stone, board, history):
		for row in range(self.board_size):
			for col in range(self.board_size):
				# Searches col first and then row
				try_place = board
				if (board[col][row] == " "):
					try_place = self.rules.place(stone, (col, row), history[0])
					visited = [ [False] * self.board_size for row in range(self.board_size) ]
					neighbors = self.rules.find_neighbors((col, row))
					q = Queue.Queue()
					for n in neighbors:
						if ((try_place[n[0]][n[1]] != stone) and (not self.rules.reachable(n, " ", try_place))):
							visited[n[0]][n[1]] = True
							q.put(n)

					while (q.empty() != True):
						check_point = q.get()
						try_place = self.rules.remove(try_place[check_point[0]][check_point[1]], check_point, try_place)
						n_neighbors = self.rules.find_neighbors(check_point)
						for n in n_neighbors:
							if ((try_place[n[0]][n[1]] == self.rules.get_opponent(stone)) and (not visited[n[0]][n[1]])):
								visited[n[0]][n[1]] = True
								q.put(n)

					if (len(history) == 3):
						if (try_place != history[1]):
							# If liberties present then valid move
							if (self.rules.reachable((col, row), " ", try_place)):
								return self.rules.idx_to_point(row, col)

					if (len(history) != 3):
						if (self.rules.reachable((col, row), " ", try_place)):
							return self.rules.idx_to_point(row, col)

		return "pass"


	
class GoBoard():
	def __init__(self, board_size=None):
		"""
		This class implements a Go board component that returns a response
		based on a statement executed on a given 19 x 19 Go board. The
		statements are as follows:

		Query Statements:
			["occupied?", Point] - returns True if a Stone at point, else False
			["occupies?", Stone, Point] - returns True if stone at point, else False
			["reachable?", Point, MaybeStone] - returns True if exists path of vertical
						or horizontal adjacent points of same Stone from Stone at Point to
						Maybestone, else False. Implemented BFS with queue

		Command Statements:
			["place", Stone, Point] - returns updated Board with Stone at Point,
						error if invalid move "This seat is taken!"
			["remove", Stone, Point] - returns updated Board with Stone removed from
						Point, error if invalid "I am just a board! I cannot remove
						what is not there!"
			["get-points", MaybeStone] - returns array of Points that has stored all
						Point positions of the given MaybeStone input in the Go board,
						sorted in increasing lexicographic order.
		"""
		self.board_size = 19 if board_size is None else board_size


	###############################
	# BOARD RESPONSES
	###############################

	# Returns appropriate response given a valid input form
	def get_response(self, input):
		if (len(input) == self.board_size):
			return self.get_score(input)
		elif ((len(input) == 2) and (input[1] == "pass")):
			return self.pass_turn(input[0])
		elif (len(input) == 2):
			return self.get_validity(input[0], self.point_to_idx(input[1][0]), input[1][1])
		else:
			raise Exception("Invalid input has no appropriate response")

	# Returns the score of "B" and "W" given a final board state.
	def get_score(self, board):
		black_area = len(self.get_points("B", board))
		white_area = len(self.get_points("W", board))
		neutral = 0

		all_empty = self.get_points(" ", board)
		for intersection in all_empty:
			point = self.point_to_idx(intersection)
			if ((not self.reachable(point, "W", board)) and (not self.reachable(point, "B", board))):
				neutral += 1
			elif (not self.reachable(point, "W", board)):
				black_area += 1
			elif (not self.reachable(point, "B", board)):
				white_area += 1
			else:
				neutral += 1

		if ((black_area + white_area + neutral) == (self.board_size * self.board_size)):
			return {"B": black_area, "W": white_area}
		else:
			raise Exception("Invalid scoring, sum of black, white, and neutral must be intersection total.")



	###############################
	# RULE CHECKER INVARIANTS
	###############################
	"""
	1.  Go is a game between two players, called Black and White.
	2.  Go is played on a plane grid of horizontal and vertical lines, called a board.
		 - Points on the board are intersections between lines.
		 - Points are adjacent if they are distinct and connected by a line
		  with no other intersections between them.
	3.  Go is played with tokens know as stones. Each player has at their
		disposal an adequate supply of their color stone.
	4. 	At any time in the game, each intersection may only be Empty,
		occupied by white or occupied by black stone.
	5.	At the beginning of the game, the board is empty.
	6.	Black moves first, the player then alternate moves.
	7.	Moves are either "pass" or Play.
		- Can only play at empty intersections.
		- Can only play if stone will still have liberties after play.
		- Liberties counted by chained stones.
		- Stones without liberties after play are removed from board.
	8. A Play is illegal if it would repeat a previously played position (Ko).
	9. The game ends when both players have pass consecutive.
	10. The player with the higher score wins, otherwise drawn game.
	"""

	# Validates history only, independent of requested move
	def validate_history(self, stone, boards_arr):

		# Board history len 1 means just started, board is empty, black to move
		if (len(boards_arr) == 1):
			if (stone != "B"):
				return False
			if (len(self.get_points(" ", boards_arr[0])) != (self.board_size * self.board_size)):
				return False

		# Board history len 2, first is empty board, black moved once, it's white's turn
		elif (len(boards_arr) == 2):
			if (stone != "W"):
				return False
			if ((len(self.get_points("B", boards_arr[0])) > 1) or (len(self.get_points("W", boards_arr[0])) != 0)):
				return False
			if (len(self.get_points(" ", boards_arr[1])) != (self.board_size * self.board_size)):
				return False

		# Board history len 3
		elif (len(boards_arr) == 3):

			# Check board history for Ko rule
			if (boards_arr[0] == boards_arr[2]):
				return False

			# Check game over because 2 consecutive passes
			if ((boards_arr[0] == boards_arr[1]) and (boards_arr[0] == boards_arr[2])):
				return False
			if ((boards_arr[1] == boards_arr[2]) and (len (self.get_points(" ", boards_arr[1])) == (self.board_size * self.board_size)) and (len (self.get_points(" ", boards_arr[2])) == (self.board_size * self. board_size)) and (len (self.get_points("W", boards_arr[0])) != 1)):
				return False

			# Check Board history contains no dead stones
			if ((not self.check_dead_removed(boards_arr[0])) or (not self.check_dead_removed(boards_arr[1])) or (not self.check_dead_removed(boards_arr[2]))):
				return False

			# Check that players are alternating plays between "B" and "W"
			if (not self.get_player_order(boards_arr[0], boards_arr[1], boards_arr[2], stone)):
				return False

			# Check Board history contains only valid moves
			if ((not self.get_move_validity(boards_arr[2], boards_arr[1])) or (not self.get_move_validity(boards_arr[1], boards_arr[0]))):
				return False

		else:
			raise Exception("Board history length should be 1 to 3.")

		return True


	# Returns the validity of a Move given a [Stone, [Point, Boards]] valid input w/ board history
	def get_validity(self, stone, point, boards_arr):

		# Board history len 1 means just started, board is empty, black to move
		if (len(boards_arr) == 1):
			if (stone != "B"):
				return False

			if (len(self.get_points(" ", boards_arr[0])) != (self.board_size * self.board_size)):
				return False

		# Board history len 2, first is empty board, black moved once, it's white's turn
		elif (len(boards_arr) == 2):
			if (stone != "W"):
				return False
			if ((len(self.get_points("B", boards_arr[0])) > 1) or (len(self.get_points("W", boards_arr[0])) != 0)):
				return False
			if (len(self.get_points(" ", boards_arr[1])) != (self.board_size * self.board_size)):
				return False

			# Check if requested play is valid
			try_place = self.place(stone, point, boards_arr[0])
			if (try_place == "This seat is taken!"):
				return False
			else:
				if ((not self.get_move_validity(boards_arr[0], try_place))):
					return False

		# Board history len 3, check moves valid between them, check current move
		elif (len(boards_arr) == 3):

			################################
			# Check board history
			################################

			# Check board history for Ko rule
			if (boards_arr[0] == boards_arr[2]):
				return False

			# Check game over because 2 consecutive passes
			if ((boards_arr[0] == boards_arr[1]) and (boards_arr[0] == boards_arr[2])):
				return False
			if ((boards_arr[1] == boards_arr[2]) and (len (self.get_points(" ", boards_arr[1])) == (self.board_size * self.board_size)) and (len (self.get_points(" ", boards_arr[2])) == (self.board_size * self. board_size)) and (len (self.get_points("W", boards_arr[0])) != 1)):
				return False

			# Check Board history contains no dead stones
			if ((not self.check_dead_removed(boards_arr[0])) or (not self.check_dead_removed(boards_arr[1])) or (not self.check_dead_removed(boards_arr[2]))):
				return False

			# Check that players are alternating plays between "B" and "W"
			if (not self.get_player_order(boards_arr[0], boards_arr[1], boards_arr[2], stone)):
				return False

			# Check Board history contains only valid moves
			if ((not self.get_move_validity(boards_arr[2], boards_arr[1])) or (not self.get_move_validity(boards_arr[1], boards_arr[0]))):
				return False


			#############################
			# Check move against history
			#############################

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

				if (not self.get_move_validity(boards_arr[0],try_place)):
					return False
			else:
				if (not self.get_move_validity(boards_arr[0],try_place)):
					return False

			# Check that requested move doesn't violate Ko rule
			if (boards_arr[1] == try_place):
				return False

		else:
			raise Exception("Board history length should be 1 to 3.")

		return True

	# Check that a move is valid between previous and current board
	def get_move_validity(self, prev_board, curr_board):

		# Get all the difference between state
		placed = []
		removed = []
		dead_removed = []

		for row in range(self.board_size):
			for col in range(self.board_size):
				if (prev_board[row][col] != curr_board[row][col]):
					if (prev_board[row][col] == " "):
						placed.append([curr_board[row][col], (row, col)])
					elif ((prev_board[row][col] == "B") and (curr_board[row][col] == " ")):
						removed.append([prev_board[row][col], (row, col)])
					elif ((prev_board[row][col] == "W") and (curr_board[row][col] == " ")):
						removed.append([prev_board[row][col], (row, col)])
					# Unexplained changes in board state
					elif ((prev_board[row][col] == "B") and (curr_board[row][col] == "W")):
						print(1)
						return False
					elif ((prev_board[row][col] == "W") and (curr_board[row][col] == "B")):
						return False

		# Move was a pass, boards should be identical
		if (len(placed) == 0):
			if (len(removed) != 0):
				return False
			if (prev_board != curr_board):
				return False

		# Check if place on board has liberties, and for removed dead stones
		if (len(placed) == 1):
			try_place = self.place(placed[0][0], placed[0][1], prev_board)
			if (try_place == "This seat is taken!"):
				return False
			else:
				white_b4 = len(self.get_points("W", prev_board))
				black_b4 = len(self.get_points("B", prev_board))
				stone = placed[0][0]

				visited = [ [False] * self.board_size for row in range(self.board_size) ]
				neighbors = self.find_neighbors(placed[0][1])
				q = Queue.Queue()
				for n in neighbors:
					if ((try_place[n[0]][n[1]] == self.get_opponent(stone)) and (not self.reachable(n, " ", try_place))):
						visited[n[0]][n[1]] = True
						q.put(n)

				while (q.empty() != True):
					check_point = q.get()
					dead_removed.append([try_place[check_point[0]][check_point[1]], check_point])
					try_place = self.remove(try_place[check_point[0]][check_point[1]], check_point, try_place)
					n_neighbors = self.find_neighbors(check_point)
					for n in n_neighbors:
						if ((try_place[n[0]][n[1]] == self.get_opponent(stone)) and (not visited[n[0]][n[1]])):
							visited[n[0]][n[1]] = True
							q.put(n)
				# Check that all things that things that shouldn't be removed weren't removed
				removed_sorted = sorted(removed)
				dead_removed_sorted = sorted(dead_removed)

				if (removed_sorted != dead_removed_sorted):
					return False

				if ((stone == "B") and (len(removed_sorted) == 0) and (white_b4 != len(self.get_points("W", try_place)))):
					return False

				if ((stone == "W") and (len(removed_sorted) == 0) and (black_b4 != len(self.get_points("B", try_place)))):
					return False


				# If still no liberties present after removal of dead, then invalid move
				if (not self.reachable(placed[0][1], " ", try_place)):
					return False

		# Can only add one stone every turn or pass
		if (len(placed) > 1):
			return False

		return True



	###############################
	# QUERIES
	###############################

	# Occupied takes an index tuple and returns True
	# if board at that point is not Empty (" "), else False
	def occupied(self, idx, board):
		return (board[idx[0]][idx[1]] != " ")

	# Occupies takes an index tuple and returns True if
	# board at that point has that Stone, else False
	def occupies(self, stone, idx, board):
		return (board[idx[0]][idx[1]] == stone)

	# Return True if there is a path of adjacent points to Point
	# that have the same kind of MaybeStone as the given point and
	# the path reaches the given MaybeStone, else False
	def reachable(self, idx, maybe_stone, board):
		visited = [ [False] * self.board_size for row in range(self.board_size)]

		start_type = board[idx[0]][idx[1]]
		if (start_type == maybe_stone):
			return True

		q = Queue.Queue()
		q.put(idx)

		while (q.empty() != True):
			check_point = q.get()
			if (not visited[check_point[0]][check_point[1]]):
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



	###############################
	# COMMANDS
	###############################

	# Passes turn
	def pass_turn(self, player):
		return True

	# Places a stone at the given point on a go_board if not occupied
	def place(self, stone, idx, board):
		if (self.occupied(idx, board)):
			return "This seat is taken!"
		else:
			new_board = [ [" "] * self.board_size for row in range(self.board_size)]
			for row in range(self.board_size):
				for col in range(self.board_size):
					new_board[row][col] = board[row][col]
			new_board[idx[0]][idx[1]] = stone
			
			return new_board

	# Removes a stone from given point on go_board if occupied
	def remove(self, stone, idx, board):
		if ((self.occupied(idx, board) == False) or (not self.occupies(stone, idx, board))):
			return "I am just a board! I cannot remove what is not there!"
		else:
			new_board = [ [" "] * self.board_size for row in range(self.board_size)]
			for row in range(self.board_size):
				for col in range(self.board_size):
					new_board[row][col] = board[row][col]
			new_board[idx[0]][idx[1]] = " "
			
			return new_board

	# Returns array of points that maybe_stone occupies on go_board
	def get_points(self, maybe_stone, board):
		points = []
		for x in range(self.board_size):
			for y in range(self.board_size):
				if (board[x][y] == maybe_stone):
					points.append(self.idx_to_point(y, x))
		points = sorted(points)
		return points



	###############################
	# HELPER FUNCTIONS
	###############################
	# Converts point from "N-N" to indices
	def point_to_idx(self, point):
		idx = point.split("-")
		for i in range(len(idx)):
			idx[i] = int(idx[i])

		return idx[1] - 1, idx[0] - 1

	# Converts indices to "N-N" point position
	def idx_to_point(self, x, y):
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
				point_idx = (n_x, n_y)
				neighbors.append(point_idx)

		return neighbors

	# Gets other player
	def get_opponent(self, curr_player):
		return "W" if (curr_player == "B") else "B"

	# Gets player move order
	def get_player_order(self, board0, board1, board2, curr_player):
		order = []

		if (board1 == board2):
			order.append(curr_player)
		else:
			for row in range(self.board_size):
				for col in range(self.board_size):
					if (board2[row][col] != board1[row][col]):
						if (board2[row][col] == " "):
							order.append(board1[row][col])


		if (self.get_points(" ", board0) == self.get_points(" ", board1)):
			order.append(self.get_opponent(curr_player))
		else:
			for row in range(self.board_size):
				for col in range(self.board_size):
					if (board1[row][col] != board0[row][col]):
						if (board1[row][col] == " "):
							order.append(board0[row][col])
		order.append(curr_player)

		if (len(order) == 3):
			if ((order[0] != order[2]) or (order[0] == order[1]) or (order[1] == order[2])):
				return False

		return True

	# Checks that all stones w/out liberties removed from board
	def check_dead_removed(self, board):
		for row in range(self.board_size):
			for col in range(self.board_size):
				if ((board[row][col] == "B") and (not self.reachable((row, col), " ", board))):
					return False
				elif ((board[row][col] == "W") and (not self.reachable((row, col), " ", board))):
					return False

		return True

