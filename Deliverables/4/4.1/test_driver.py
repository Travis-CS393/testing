from goboard import GoBoardComponent
import json
import sys

##########################################
# HELPER FUNCTIONS
##########################################

# Reads and returns array of [Board, Statement] JSON array elements from STDIN 
def read_input():
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
	return inputs

# Reads in outputs array and dumps it to JSONify outputs array
def print_output(output):
	return json.dumps(output)



###########################################
# TYPE ASSERTIONS PREDICATES
###########################################

# Checks that input is one of the valid types of input 
# Board
# [Stone Move] where Move is a "pass" or Play
#              and Play is of form [Point, Boards]
#			   and Bords is a JSON array of Board of length 1, 2, or 3
# 	- [Stone, "pass"]
# 	- [Stone, [Point, [Board]]]
# 	- [Stone, [Point, [Board, Board]]]
# 	- [Stone, [Point, [Board, Board, Board]]]
def check_input(input, board_size):
	if (len(input) == board_size):
		return check_board(input, board_size)
	elif ((len(input) == 2) and check_stone(input[0]) and (input[1] == "pass")):
		return True
	elif ((len(input) == 2) and check_stone(input[0]) and check_point(input[1][0]) \
		 and ((len(input[1][1]) == 3) or (len(input[1][1]) == 2) or (len(input[1][1]) == 1))):
		return all(check_board(board) for board in input[1][1])
	else:
		return False

# Stone must be "B" or "W"
def check_stone(stone):
	return ((stone == "B") or (stone == "W"))

# MaybeStone must be a Stone or " "
def check_maybe_stone(maybe_stone):
	return (check_stone(maybe_stone) or (maybe_stone == " "))

# Point must be in the format "N-N" where N is a value 1 to 19
def check_point(point):
	parsed_point = point.split("-")
	if(len(parsed_point) == 2):
		pos_set = {"1", "2", "3", "4", "5", "6", "7", "8", "9", \
				   "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"}
		return( (pared_point[0] in pos_set) and (parsed_point[1] in pos_set) )
	return False

# Board must be 19 x 19 represented by an array of 19 rows 
# where each row contains 19 elements of type MaybeStone
def check_board(board, board_size):
	check_all_stones = True
	for row in range(len(board[0])):
		if(len(board[row]) != board_size):
			return False
		for col in range(len(board[row])):
			if (check_maybe_stone(board[row][col]) == False):
				check_all_stones = False
	return check_all_stones


##########################################
# TEST DRIVER
##########################################

# Test Driver returns JSON array of response JSON values to STDOUT
def test_driver():
	inputs = read_input()
	outputs = []
	goboard = GoBoardComponent()

	for element in inputs:
		if(check_input(element, 19)):
			outputs.append(goboard.get_response(element))
		else:
			raise Exception("Invalid Input: Must be one of Board or [Stone, Move].")

	print(print_output(outputs))

test_driver()


