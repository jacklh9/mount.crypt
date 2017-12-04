import unittest
from unittest.mock import patch
from mountcrypt import MountCrypt

class MountCryptTest(unittest.TestCase):

	def setUp(self):
		self.mc = MountCrypt()
		self.mc.read_config("mountcrypt.ini")
		print ("setUp executed!")

	def tearDown(self):
		print ("tearDown executed!")


### MOCK METHODS ###

	def mock_decrypt_volume(volume, uuid):
		print("Mocking decryption of volume.")

	def mock_subprocess_run(*args, **kwargs):
		print("Mocking running of tasks.")

	def mock_path_exists(self):
		print("Mocking path exists.")
		return True

	def mock_mount_volume(self, mount_point):
		print("Mocking volume mount.")

### TESTS ###

	def testVersion1(self):
		obj = self.mc.version
		cls = type("string class")
		self.assertIsInstance(obj, cls, "Version not in string format")

	@patch('mountcrypt.MountCrypt.decrypt_volume', mock_decrypt_volume)		
	@patch('mountcrypt.MountCrypt.mount_volume', mock_mount_volume)
	@patch('subprocess.run', mock_subprocess_run)
	@patch('pathlib.Path.exists', mock_path_exists)
	def testRun(self):
		mc = MountCrypt(interactive=False)
		mc.read_config("./mountcrypt.ini")
		mc.mount_volumes()


if __name__ == "__main__":
	unittest.main()
