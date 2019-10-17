from goboard import GoBoardComponent
import json

# Test Driver returns JSON array of response JSON values to STDOUT
def test_driver():
	output = []
	go_board = GoBoardComponent()
	go_board.read_input()
	for i in range(len(go_board.statements)):
		go_board.go_board = go_board.go_boards[i]
		output.append(go_board.execute_statement(go_board.statements[i]))
		
	print(json.dumps(output))

test_driver()