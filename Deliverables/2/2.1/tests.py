import unittest
import BackEndComponent

def test1():
	special_obj = json.load(sys.stdin)

    back_service = BackEndComponent()
	sorted_ten = back_service.sort(special_obj)

	sys.stdout.write(sorted_ten[0])