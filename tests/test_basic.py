import sys, unittest
from unittest.mock import patch

# local modules
sys.path.append(".")
from mountcrypt import MountCrypt


class MountCryptMock:

	def close_volume(self, volume):
		print("Mocking closing of volume.")
		return True

	def decrypt_volume(self, volume, uuid):
		print("Mocking decryption of volume.")
		return True

	def subprocess_run(*args, **kwargs):
		print("Mocking running of tasks.")

	def is_attached(self, uuid):
		print("Mocking device is attached.")
		return True

	def is_decrypted_false(self, volume):
		print("Mocking device not already decryted.")
		return False

	def is_decrypted_true(self, volume):
		print("Mocking device not already decryted.")
		return False

	def mount_volume(self, mount_point):
		print("Mocking volume successfully mounted.")

	def unmount_volume(self, mount_point):
		print("Mocking volume successfully unmounted.")


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

        
class MountCryptDecryptTests(unittest.TestCase):

	@patch('mountcrypt.MountCrypt.close_volume', MountCryptMock.close_volume)
	@patch('mountcrypt.MountCrypt.decrypt_volume', MountCryptMock.decrypt_volume)
	@patch('mountcrypt.MountCrypt.mount_volume', MountCryptMock.mount_volume)
	@patch('mountcrypt.MountCrypt.unmount_volume', MountCryptMock.unmount_volume)
	@patch('subprocess.run', MountCryptMock.subprocess_run)
	@patch('mountcrypt.MountCrypt.is_attached', MountCryptMock.is_attached)
	@patch('mountcrypt.MountCrypt.is_decrypted', MountCryptMock.is_decrypted_false)
	def testRun(self):
		mc = MountCrypt(interactive=False)
		mc.read_config("./mountcrypt.ini")
		mc.mount_volumes()


class MountCryptCloseTests(unittest.TestCase):

	@patch('mountcrypt.MountCrypt.close_volume', mock_close_volume)
	@patch('mountcrypt.MountCrypt.decrypt_volume', mock_decrypt_volume)
	@patch('mountcrypt.MountCrypt.mount_volume', mock_mount_volume)
	@patch('mountcrypt.MountCrypt.unmount_volume', mock_unmount_volume)
	@patch('subprocess.run', mock_subprocess_run)
	@patch('mountcrypt.MountCrypt.is_attached', mock_is_attached)
	@patch('mountcrypt.MountCrypt.is_decrypted', mock_is_decrypted_true)
	def testRun(self):
		mc = MountCrypt(interactive=False)
		mc.read_config("./mountcrypt.ini")
		mc.unmount_volumes()
		mc.close_volumes()

if __name__ == "__main__":
	unittest.main()
