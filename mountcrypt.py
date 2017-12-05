#!python3

import configparser, csv, getopt, getpass, psutil, subprocess, sys, time
from os.path import basename
from pathlib import Path

class MountCrypt:
    
    def __init__(self, interactive=True):
        '''
        (self, bool)

        interactive: 
            True: user gets Y/N prompts.
            False: defaults are used at all prompts; however, user will
            still be prompted for passphrase when decrypting.
        '''
        self.version = "0.3b"
        # We explicity check if a valid booleans
        if interactive:
            self.interactive = True
        else:
            self.interactive = False

    def close_volume(self, volume):
        '''
        (self, string)

        This method is the inverse of decrypt_volume().
        Note that all mount points must be closed first.
        SEE: unmount_volume() and unmount_volumes()

        '''
        self._print_volume_info(volume)
        if self.is_decrypted(volume):
            if not self._response_yes("Close volume?", default=True):
                print("Leaving open...")
            else:
                try:
                    subprocess.Popen([self.cryptsetup, "close", volume],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
                    print("Successfully closed")
                except Exception as details:
                    print("Error closing volume.")
                    self._print_exception(details)
        else:
            print("Already closed. Skipping...")

    def close_volumes(self):
        print("Closing volumes...")
        for volume in self.volumes:
            self.close_volume(volume)

    def decrypt_volume(self, volume):
        ''' 
        (self, string, string) -> bool

        Runs the command-line program "cryptsetup open --type luks UUID=<device-UUID> <device-mapped-name>".
        Prompts the user to enter the passphrase to decrypt the volume.
        Returns True if successful, False otherwise.

        '''
        uuid = self._get_volume_uuid(volume)
        is_decrypted = False
        try:
            p = subprocess.Popen([self.cryptsetup, "open", "--type", "luks", "UUID=" + uuid, volume],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
            p.stdin.write(bytes(getpass.getpass("Enter passphrase: "), 'utf-8'))
            p.communicate()[0]
            if p.returncode == 0:
                is_decrypted = True
        except Exception as details:
            print("Error encountered during decryption attempt:")
            self._print_exception(details)
        finally:
            p.stdin.close()

        return is_decrypted

    def is_attached(self, volume):
        uuid = self._get_volume_uuid(volume)
        volume_uuid_path = Path("/".join(('/dev/disk/by-uuid', uuid)))
        return volume_uuid_path.exists()

    def is_decrypted(self, volume):
        # Decrypted device volumes appear in /dev/mapper/
        volume_mapper_path = Path("/".join(('/dev/mapper', volume)))
        return volume_mapper_path.exists()

    def is_mounted(self, mount_point):
        # object of all active system partitions
        partitions = psutil.disk_partitions()
        # Extract a list of existing mounted
        # mountpoints from partitions object...
        system_mounts = list([partition.mountpoint for partition in partitions])
        # ... and see if this particular mountpoint is already mounted.
        return mount_point in system_mounts

    def mount_mountpoint(self, mount_point):
        subprocess.Popen([self.mount, mount_point])

    def mount_volumes(self):
        print("Decrypting and mounting volumes...")
        for volume in self.volumes:
            self._print_volume_info(volume)
            num_errors = 0
            volume_mounts = self._get_volume_mounts(volume)

            # Ensure volume is attached to server else skip volume
            # NOTE: In case it's at an off-site backup location today
            if not self.is_attached(volume):
                print("Volume not present. Skipping...")
                continue 

            if not self.is_decrypted(volume):
                if not self._response_yes("Decrypt?", default=True):
                    print("Skipping...")
                    continue
                
                try:
                    is_decrypted = self.decrypt_volume(volume)
                except Exception as details:
                    self._print_exception(details)
                    is_decrypted = False
                finally:
                    if not is_decrypted:
                        num_errors += 1

            else:
                print("Volume already decrypted.")

            # Attempt mounting requested mount-points,
            # if volume successfully mounted earier.
            if (num_errors == 0):
                for mnt_pt in volume_mounts:
                    print("Mounting: {}".format(mnt_pt))
                    if self.is_mounted(mnt_pt):
                        print("Already mounted. Skipping...")
                        continue
                    else:
                        # See if the user even WANTS to mount this.
                        if not self._response_yes("Mount?", default=True):
                            print("Skipping...")
                            continue
                        else:
                            try:
                                self.mount_mountpoint(mnt_pt)
                            except Exception as details:
                                self._print_exception(details)
                                num_errors += 1

            # Did the volume or ANY of the mounts fail?
            if (num_errors == 0):
                self.run_mount_tasks(volume)
            else:
                print("Errors found! Did not run associated program(s).")


    def print_error(self, args=[]):
        CMD_LINE_SYNTAX_ERROR = 2 # By convention per sys.exit()

        if args:
            # stringify args
            print("Invalid argument(s): {}".format(' '.join([str(arg) for arg in args])))
        else:
            print ("No arguments specified!")

        print("For help, run: {program} {help_flag}".format(program=basename(__file__), help_flag="[-h | --help]"))
        sys.exit(CMD_LINE_SYNTAX_ERROR)

        
    def print_usage(self):
        usage_text="""{program} [options]

OPTIONS
    -c, --config <my-config.ini>    Configuration file
    -d, --decrypt                   Decrypt volumes [default]
    -D, --defaults                  Accept defaults for all Y/N prompts.
        NOTE: You may be prompted for decryption passphrase.
    -h, --help                      Print this help
    -u, --unmount                   Unmount volumes but don't close.
    -U, --close                     Unmount and close volumes. 

CONFIG FILE

EXAMPLE:

[DEFAULT]
cryptsetup=/sbin/cryptsetup
mount=/bin/mount
unmount=/bin/umount

# Mount Definitions:
# ------------------
# NOTE: The mapper-name and mount-points need to also be defined and
# match the entries for these respective drives in /etc/fstab.
# 
# Example /etc/fstab btrfs mount-point entries:
# 
# LABEL=data      /mnt/data     btrfs     compress=lzo,defaults,noatime,noauto,nodiratime,subvol=@data  0       0
# LABEL=data      /opt/vbox       btrfs     compress=lzo,defaults,noatime,noauto,nodiratime,subvol=@vbox 0       0
# 
# mount.crypt.ini entry format:
#
# [mapper-name]
# UUID=abc...def
# mounts=/mnt/mount-point,/mnt/other-mount-point,...
#
# Optionally include any commands to run after a successful mount
# and before an unmount.
# run_progs=my-script.sh --some-flag,my-other-script.sh
# run_progs_unmount=pkill -u testuser
# 
# NOTE: Lists MUST NOT have ANY spaces nor double-quotes 
# in-between the comma delimiter.
#

[backup]
UUID=123ab45c-de67-8901-a234-bcd5efab678c
mounts=/mnt/backup

[data]
UUID=456ab45c-de67-8901-a234-bcd5efab601d
mounts=/mnt/data,/opt/vbox
run_progs=lxc start testbox devbox,lxc list
run_progs_unmount=lxc stop testbox devbox,lxc list
"""
# End here-doc
        print(usage_text.format(program=sys.argv[0]))

        ### End print_usage()


    def print_version(self):
        print("Version: {version}".format(version=self.version))

    def read_config(self, config_file):
        print("Using config {}".format(config_file))
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.cryptsetup = self.config['DEFAULT']['cryptsetup']
        self.mount = self.config['DEFAULT']['mount']
        self.unmount = self.config['DEFAULT']['unmount']
        self.volumes = self.config.sections()

            
    def run_mount_tasks(self, volume):
        self._run_tasks(volume, 'run_progs')

    def run_unmount_tasks(self, volume):
        self._run_tasks(volume, 'run_progs_unmount')

    def unmount_mountpoint(self, mount_point):
        print("Mount point: ", mount_point)
        if not self._response_yes("Unmount?", default=True):
            print("Skipping...")
        else:
            try:
                subprocess.Popen([self.unmount, mount_point])
                print("Successfully unmounted")
            except Exception as details:
                print("Error encountered while unmounting.")
                self._print_exception(details)

    def unmount_volumes(self):
        print("Unmounting volumes...")
        for volume in self.volumes:
            if self.is_decrypted(volume):
                self._print_volume_info(volume)
                for mnt_pt in self._get_volume_mounts(volume):
                    if self.is_mounted(mnt_pt):
                        self.run_unmount_tasks(volume)
                        self.unmount_mountpoint(mnt_pt)

    ### Private Helper Methods ###

    def _get_volume_uuid(self, volume):
        return self.config[volume]['UUID']


    def _get_volume_mounts(self, volume):
        ''' 
        (self, volume) -> list of strings

        Returns the list of paths of requested mount-points to
        mount per the config file for the particular volume.
        '''
        return self.config[volume]['mounts'].split(',')


    def _print_exception(self, exception):
        print("Command error: {}".format(exception))


    def _print_volume_info(self, volume):
        uuid = self._get_volume_uuid(volume)
        print("\nVolume: {}".format(volume))
        print("UUID: {}".format(uuid))

    def _response_yes(self, question, default):
        '''
            (self, string, bool) -> bool

            Prompt the user for a yes/no response,
            indicating if YES is the default (True) choice
            or not (False).

            NOTE: A default choice is required and must
            always be explicitly set. The default choice
            will be returned if the user leaves the response
            blank and presses enter. The default response
            (e.g., if set to True) will be indicated to the 
            user as a capital letter, as follows:

                Do you agree? [Y/n] 

            Returns True if the answer was 'y' or 'yes' 
            (regardless of case) else False.
        '''
        if type(default) is not bool:
                print("A default boolean must be supplied")
                raise TypeError

        if default == True:
            prompt = question + " [Y/n] "
            if not self.interactive:
                return True
        elif default == False:
            prompt = question + " [y/N] "
            if not self.interactive:
                return False

        while True:
            response = input(prompt)
            if response.lower() == '':
                return default
            elif response.lower() in ['y','yes']:
                return True
            elif response.lower() in ['n','no']:
                return False
            else:
                print("Invalid response: ", response, "\n")

    def _run_tasks(self, volume, config_var):
        '''
        (self, string, string)

        config_var should be a string of either of the following:
            'run_progs', 'run_progs_unmount'

        The method will then pull the data from the config file, build
        a list and then iterate over the list and run each program.

        Returns nothing.

        '''
        if (self.config.has_option(volume,config_var)):
            for program in self.config[volume][config_var].split(','):
                print("TASK: {}".format(program));
                if self._response_yes("Run the above task?", default=True):
                    try:
                        subprocess.run([program], shell=True, check=True)
                    except Exception as details:
                        self._print_exception(details)
                else:
                    print("Skipping...")
        else:
            print("No tasks to run for this volume.")


def main(argv):
    '''
    interactive:
        See description for __init__.

    decrypt:
        True: decrypt volumes
        False: don't decrypt. Unmount volumes.

    close:
        False: If decrypt is False, then unmount all volumes but don't close.
        True: If decrypt is False, unmount AND close (undo decrypt) of all volumes.
    '''
    close=False
    decrypt=True
    interactive = True
    config = "mountcrypt.ini"

    try:
        opts, args = getopt.getopt(argv,"c:dDhuUV",
            ["config=", "close", "decrypt", "defaults", "help", "unmount", "version"])
    except getopt.GetoptError:
        MountCrypt().print_error(argv)

    for opt, arg in opts:
        if opt in ('-U', '--close'):
            decrypt = False
            close = True
        elif opt in ('-c', '--config'):
            config = arg
        elif opt in ('-d', '--decrypt'):
            decrypt = True
        elif opt in ('-D', '--defaults'):
            interactive = False
        elif opt in ('-h', '--help'):
            MountCrypt().print_usage()
            sys.exit()
        elif opt in ('-u', '--unmount'):
            decrypt = False
            close = False
        elif opt in ('-V', '--version'):
            MountCrypt().print_version()
            sys.exit()
        else:
            MountCrypt().print_error(opt)

    if not opts:
        MountCrypt().print_error(argv)

    mc = MountCrypt(interactive=interactive)
    mc.read_config(config)

    if decrypt:
        mc.mount_volumes()
    else:
        mc.unmount_volumes()
        if close:
            mc.close_volumes()

if __name__ == "__main__": main(sys.argv[1:])
