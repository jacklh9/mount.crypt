import unittest, mountcrypt

class MountCryptTest(unittest.TestCase):

	def setUp(self):
		mc = mountcrypt.MountCrypt()
		mc.read_config(mountcrypt.ini)
		print ("setUp executed!")

	def testVersion(self):
		obj = "Test"
		cls = type(obj)
		obj = 2
		self.assertIsInstance(obj, cls, "Version not in string format")

	def tearDown(self):
		print ("tearDown executed!")

if __name__ == "__main__":
	unittest.main()
