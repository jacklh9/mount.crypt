import unittest
from unittest.mock import patch
from mountcrypt import MountCrypt

class MountCryptTest(unittest.TestCase):

	def setUp(self):
		self.mc = MountCrypt()
		self.mc.read_config("mountcrypt.ini")
		print ("setUp executed!")

	def testVersion1(self):
		obj = self.mc.version
		cls = type("string class")
		self.assertIsInstance(obj, cls, "Version not in string format")

	def tearDown(self):
		print ("tearDown executed!")


if __name__ == "__main__":
	unittest.main()
