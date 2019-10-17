import unittest
from goboard import GoBoardComponent

class TestFunctions(unittest.TestCase):

#============= HELPER FUNCTION TESTS=================
    def testProcessPoints(self):
        gb = GoBoardComponent()
        self.assertEqual(gb.process_point("1-1"), (0,0))
        self.assertEqual(gb.process_point("19-15"), (14,18))
        self.assertEqual(gb.process_point("4-9"), (8,3))

    def testAddPoints(self):
        gb = GoBoardComponent()
        gb.add_point(0, 0)
        self.assertEqual(gb.points[0], "1-1")
        gb.add_point(18, 4)
        self.assertEqual(gb.points[1], "19-5")
        gb.add_point(2, 7)
        self.assertEqual(gb.points[2], "3-8")

    def testFindNeighbors(self):
        gb = GoBoardComponent(go_board=gb1)
        # middle point
        self.assertEqual(sorted(gb.find_neighbors("3-2")), ["2-2", "3-1", "3-3", "4-2"])
        # corner points
        self.assertEqual(sorted(gb.find_neighbors("1-19")), ["1-18", "2-19"])
        self.assertEqual(sorted(gb.find_neighbors("1-1")), ["1-2", "2-1"])
        # point on edge
        self.assertEqual(sorted(gb.find_neighbors("1-6")), ["1-5", "1-7", "2-6"])

# ===================== TEST QUERIES ===================
    def testOccupied(self):
        gb = GoBoardComponent(go_board=gb1)
        self.assertTrue(gb.occupied("3-2"))
        self.assertFalse(gb.occupied("1-1"))

    def testOccupies(self):
        gb = GoBoardComponent(go_board=gb1)
        self.assertTrue(gb.occupies("W", "2-2"))
        self.assertTrue(gb.occupies("B", "3-2"))
        self.assertFalse(gb.occupies("W", "2-3"))
        self.assertFalse(gb.occupies("B", "2-2"))
        self.assertFalse(gb.occupies("W", "1-1"))
        self.assertFalse(gb.occupies("B", "1-1"))

    def testReachable(self):
        gb = GoBoardComponent(go_board=gb1)
        # point is the maybe stone
        self.assertTrue(gb.reachable("1-1", " "))
        self.assertTrue(gb.reachable("2-2", "W"))
        self.assertTrue(gb.reachable("2-3", "B"))

        # can reach through connected paths
        self.assertTrue(gb.reachable("1-6", "B"))
        self.assertTrue(gb.reachable("1-6", " "))
        self.assertTrue(gb.reachable("10-5", "W"))
        self.assertTrue(gb.reachable("10-5", " "))
        self.assertTrue(gb.reachable("1-5", "B"))
        self.assertTrue(gb.reachable("1-5", "W"))

        # cannot reach through connected paths
        self.assertFalse(gb.reachable("10-11", "W"))
        self.assertFalse(gb.reachable("1-19", "W"))
        self.assertFalse(gb.reachable("7-2", " "))

# ===================== TEST COMMANDS ===================
    def testPlace(self):
        gb = GoBoardComponent(go_board=gb1)
        # try to place where there is already something
        self.assertEqual(gb.place("W", "3-1"), "This seat is taken!")

        # place in empty spaces and check
        gb.place("W", "4-1")
        self.assertEqual(gb.go_board[0][3], "W")
        gb.place("B", "1-1")
        self.assertEqual(gb.go_board[0][0], "B")

    def testRemove(self):
        gb = GoBoardComponent(go_board=gb1)
        # try to remove something that is not there
        self.assertEqual(gb.remove("W", "1-1"), "I am just a board! I cannot remove what is not there!")
        self.assertEqual(gb.remove("B", "3-1"), "I am just a board! I cannot remove what is not there!")

        # remove stones already on there
        gb.remove("W", "3-1")
        self.assertEqual(gb.go_board[0][2], " ")
        gb.remove("B", "2-3")
        self.assertEqual(gb.go_board[2][1], " ")

    def testGetPoints(self):
        gb = GoBoardComponent(go_board=gb2)

        self.assertEqual(gb.get_points("W"), ["1-1", "1-10", "2-1", "2-5", "3-2", "4-1", "4-9"])
        self.assertEqual(gb.get_points("B"), ["1-6", "3-4", "3-6", "4-11", "4-3", "5-3", "5-7", "5-8", "6-10", "6-3", "6-6"])



# ================ TEST BOARD =========================
gb1 = [
[" ", " ", "W", " ", " ", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", "W", "B", "W", " ", "W", "B", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", "B", "B", " ", " ", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", "W", "W", " ", "B", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " "],
["W", "B", " ", " ", "B", "B", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", "B", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", "B", " ", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", "W", "W", " ", "B", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", "B", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", "B", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", "B", " ", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
["B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

gb2 = [
["W", "W", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", "B", "B", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
["B", " ", "B", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
["W", " ", " ", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

if __name__ == '__main__':
    unittest.main()
