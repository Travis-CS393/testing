from __future__ import print_function
from goboard import GoBoardComponent
import json
import sys

# Test Driver returns JSON array of response JSON values to STDOUT
def test_driver():
	go_board = GoBoardComponent()
	go_board.read_input()
	go_board.execute_statements()
	output = go_board.responses_cat()
	print(json.dumps(output))

test_driver()