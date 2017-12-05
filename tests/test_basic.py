import sys, unittest
from unittest.mock import patch

# local modules
sys.path.append(".")
from mountcrypt import MountCrypt


class MountCryptMethodTests(unittest.TestCase):

	def setUp(self):
		self.mc = MountCrypt()
		self.mc.read_config("./mountcrypt.ini")
		print ("setUp executed!")

	def tearDown(self):
		print ("tearDown executed!")

	### TESTS ###

	def testVersion1(self):
		obj = self.mc.version
		cls = type("string class")
		self.assertIsInstance(obj, cls, "Version not in string format")

        
class MountCryptTest(unittest.TestCase):

	### MOCK METHODS ###

	def mock_close_volume(self, volume):
		print("Mocking closing of volume.")
		return True

	def mock_decrypt_volume(self, volume, uuid):
		print("Mocking decryption of volume.")
		return True

	def mock_subprocess_run(*args, **kwargs):
		print("Mocking running of tasks.")

	def mock_is_attached(self, uuid):
		print("Mocking device is attached.")
		return True

	def mock_is_decrypted(self, volume):
		print("Mocking device not already decryted.")
		return False

	def mock_mount_volume(self, mount_point):
		print("Mocking volume successfully mounted.")

	def mock_unmount_volume(self, mount_point):
		print("Mocking volume successfully unmounted.")

	### TESTS ###

	@patch('mountcrypt.MountCrypt.close_volume', mock_close_volume)
	@patch('mountcrypt.MountCrypt.decrypt_volume', mock_decrypt_volume)
	@patch('mountcrypt.MountCrypt.mount_volume', mock_mount_volume)
	@patch('mountcrypt.MountCrypt.unmount_volume', mock_unmount_volume)
	@patch('subprocess.run', mock_subprocess_run)
	@patch('mountcrypt.MountCrypt.is_attached', mock_is_attached)
	@patch('mountcrypt.MountCrypt.is_decrypted', mock_is_decrypted)
	def testRun(self):
		mc = MountCrypt(interactive=False)
		mc.read_config("./mountcrypt.ini")
		mc.mount_volumes()
		mc.unmount_volumes()
		mc.close_volumes()

if __name__ == "__main__":
	unittest.main()
