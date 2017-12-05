import sys, unittest
from unittest.mock import patch

# local modules
sys.path.append(".")
from mountcrypt import MountCrypt


class MountCryptMock:

	def close_volume(self, volume):
		print("Mocking closing of volume.")
		return True

	def decrypt_volume(self, volume):
		print("Mocking decryption of volume.")
		return True

	def subprocess_run(*args, **kwargs):
		print("Mocking running of tasks.")

	def is_attached(self, volume):
		print("Mocking device is attached.")
		return True

	def is_decrypted_false(self, volume):
		print("Mocking device not already decrypted.")
		return False

	def is_decrypted_true(self, volume):
		print("Mocking device already decrypted.")
		return True

	def is_mounted_true(self, volume):
		print("Mocking device currently mounted.")
		return True

	def mount_mountpoint(self, mount_point):
		print("Mocking volume successfully mounted.")

	def unmount_mountpoint(self, mount_point):
		print("Unmounting ", mount_point)
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
		print("Version test...")
		obj = self.mc.version
		cls = type("string class")
		self.assertIsInstance(obj, cls, "Version not in string format")

        
class MountCryptDecryptTests(unittest.TestCase):

	@patch('mountcrypt.MountCrypt.close_volume', MountCryptMock.close_volume)
	@patch('mountcrypt.MountCrypt.decrypt_volume', MountCryptMock.decrypt_volume)
	@patch('mountcrypt.MountCrypt.mount_mountpoint', MountCryptMock.mount_mountpoint)
	@patch('mountcrypt.MountCrypt.unmount_mountpoint', MountCryptMock.unmount_mountpoint)
	@patch('subprocess.run', MountCryptMock.subprocess_run)
	@patch('mountcrypt.MountCrypt.is_attached', MountCryptMock.is_attached)
	@patch('mountcrypt.MountCrypt.is_decrypted', MountCryptMock.is_decrypted_false)
	def testRun(self):
		print("Testing decryption methods...")
		mc = MountCrypt(interactive=False)
		mc.read_config("./mountcrypt.ini")
		mc.mount_volumes()


class MountCryptCloseTests(unittest.TestCase):

	@patch('mountcrypt.MountCrypt.close_volume', MountCryptMock.close_volume)
	@patch('mountcrypt.MountCrypt.decrypt_volume', MountCryptMock.decrypt_volume)
	@patch('mountcrypt.MountCrypt.mount_mountpoint', MountCryptMock.mount_mountpoint)
	@patch('mountcrypt.MountCrypt.unmount_mountpoint', MountCryptMock.unmount_mountpoint)
	@patch('subprocess.run', MountCryptMock.subprocess_run)
	@patch('mountcrypt.MountCrypt.is_attached', MountCryptMock.is_attached)
	@patch('mountcrypt.MountCrypt.is_decrypted', MountCryptMock.is_decrypted_true)
	@patch('mountcrypt.MountCrypt.is_mounted', MountCryptMock.is_mounted_true)
	def testRun(self):
		print("Testing unmount and close methods...")
		mc = MountCrypt(interactive=False)
		mc.read_config("./mountcrypt.ini")
		print("Testing unmounting...")
		mc.unmount_volumes()
		print("Testing closing...")
		mc.close_volumes()

if __name__ == "__main__":
	unittest.main()
