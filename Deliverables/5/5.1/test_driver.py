from go import GoBoard, GoPlayerMin
import json
import sys

#  this is a comment

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
# ["register"]
# ["receive-stones", Stone]
# ["make-a-move", Boards]
# where Boards is an array of Board with length from 1 to 3
def check_input(input, board_size):
	if ((len(input) == 1) and (input == ["register"])):
		return True
	elif ((len(input) == 2) and (input[0] == "receive-stones") and check_stone(input[1])):
		return True
	elif ((len(input) == 2) and (input[0] == "make-a-move") and ((len(input[1]) == 3) or (len(input[1]) == 2) or (len(input[1]) == 1))):
		return all(check_board(board, board_size) for board in input[1])
	else:
		return False

# Stone must be "B" or "W"
def check_stone(stone):
	return ((stone == "B") or (stone == "W"))

# MaybeStone must be a Stone or " "
def check_maybe_stone(maybe_stone):
	return (check_stone(maybe_stone) or (maybe_stone == " "))

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
	go_player = GoPlayerMin()

	for element in inputs:
		if(check_input(element, 19)):
			if(go_player.get_response(element) != None):
				outputs.append(go_player.get_response(element))
		else:
			raise Exception("Invalid Input.")

	print(print_output(outputs))

test_driver()
