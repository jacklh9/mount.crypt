 #!python3

import configparser, csv, getopt, getpass, psutil, subprocess, sys, time
from os.path import basename
from pathlib import Path

class MountCrypt:
    
    def __init__(self, interactive=True):
        self.version = "0.2.3b"
        # We explicity check if a valid boolean
        if interactive == True:
            self.interactive = True
        else:
            self.interactive = False

    def is_decrypted(self, volume):
        # Decrypted device volumes appear in /dev/mapper/
        volume_mapper_path = Path("/".join(('/dev/mapper', volume)))
        return volume_mapper_path.exists()

    def print_version(self):
        print("Version: {version}".format(version=self.version))

    def read_config(self, config_file):
        print("Using config {}".format(config_file))
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.cryptsetup = self.config['DEFAULT']['cryptsetup']
        self.mount = self.config['DEFAULT']['mount']
        self.volumes = self.config.sections()

    def mount_volumes(self):
        for volume in self.volumes:
            uuid = self.config[volume]['UUID']
            print("\nVolume: {}".format(volume))
            print("UUID: {}".format(uuid))
            num_errors = 0
            mounts = self.config[volume]['mounts'].split(',')

            # Ensure volume is attached to server else skip volume
            # NOTE: In case it's at an off-site backup location today
            volume_uuid_path = Path("/".join(('/dev/disk/by-uuid', uuid)))
            if not volume_uuid_path.exists():
                print("Volume not present. Skipping...")
                continue 

            if not self.is_decrypted(volume):
                if not self._response_yes("Decrypt?", default=True)
                    print("Skipping...")
                    continue
                
                try:
                    # Decrypt volume
                    p = subprocess.Popen([self.cryptsetup, "open", "--type", "luks", "UUID=" + uuid, volume],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
                    p.stdin.write(bytes(getpass.getpass("Enter passphrase: "), 'utf-8'))
                    p.communicate()[0]
                    p.stdin.close()
                except Exception as details:
                    print("Command error: {}".format(details))
                    num_errors += 1

            else:
                print("Volume already decrypted.")

            # Attempt mounting requested mount-points,
            # if volume successfully mounted earier.
            if (num_errors == 0):
                partitions = psutil.disk_partitions()

                for mnt_pt in mounts:
                    print("Mounting: {}".format(mnt_pt))

                    # Extract a list of existing mounted
                    # mountpoints from partitions object...
                    mounts = list([partition.mountpoint for partition in partitions])
                    # ... and see if this particular mountpoint is already mounted.
                    if mnt_pt in mounts:
                        print("Already mounted. Skipping...")
                        continue
                    else:
                        # See if the user even WANTS to mount this.
                        if self._response_yes("Mount?", default=True):
                            print("Skipping...")
                            continue
                        else:
                            try:
                                # Mount volume
                                subprocess.Popen([self.mount, mnt_pt])
                            except Exception as details:
                                print("Command error: {}".format(details))
                                num_errors += 1

            # Did the volume or ANY of the mounts fail?
            if (num_errors == 0):
                self.run_programs(volume)
            else:
                print("Errors found! Did not run associated program(s).")

    def unmount_volumes(self):
        pass
        #for volume in self.volumes:
            #is volume decrypted
                # for each volume mount
                    # is mounted
                        # ask to unmount
        

    def run_programs(self, volume):
        if (self.config.has_option(volume,'run_progs')):
            for program in self.config[volume]['run_progs'].split(','):
                print("TASK: {}".format(program));
                if self._response_yes("Run the above task?", default=True):
                    try:
                        subprocess.run([program], shell=True, check=True)
                    except Exception as details:
                        print("Error: {}".format(details))
                else:
                    print("Skipping...")
        else:
            print("No tasks to run for this volume.")

            
    def print_usage(self):
        usage_text="""{program} [options]

OPTIONS
    -c, --config <my-config.ini>    Configuration file
    -n, --non-interactive           Non-interactive mode
        NOTE: You will still be prompted for decryption passphrase, if needed.
    -i, --interactive               Interactive mode [default]
    -h, --help                      Print this help

CONFIG FILE

EXAMPLE:

[DEFAULT]
cryptsetup=/sbin/cryptsetup
mount=/bin/mount

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
# UUID = abc...def
# mounts = /mnt/mount-point,/mnt/other-mount-point,...
#
# Optionally include any commands to run after a successful mount
# run_progs = my-script.sh --some-flag,my-other-script.sh
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

"""
# End here-doc
        print(usage_text.format(program=sys.argv[0]))

        ### End print_usage()


    def print_error(self, args=[]):
        CMD_LINE_SYNTAX_ERROR = 2 # By convention per sys.exit()

        if args:
            # stringify args
            print("Invalid argument(s): {}".format(' '.join([str(arg) for arg in args])))
        else:
            print ("No arguments specified!")

        print("For help, run: {program} {help_flag}".format(program=basename(__file__), help_flag="[-h | --help]"))
        sys.exit(CMD_LINE_SYNTAX_ERROR)

        
    def _response_yes(self, question, default):
        if default not in [True, False]:
                print "A default boolean must be supplied"
                raise

        if default = 'n':
            prompt = question + " (yN): "
            if self.interactive:
                return False
        elif default = 'y':
            prompt = question + " ("Yn"): "
            if self.interactive:
                return True

        while True:
            response = input(prompt)
            if response.lower() == '':
                return default
            elif response.lower == 'n':
                return False
            elif response.lower == 'y':
                return True
            else:
                print("Invalid response: ", response, "\n")


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"c:hinv", 
            ["config=", "help", "interactive", "non-interactive", "version"])
    except getopt.GetoptError:
        MountCrypt().print_error(argv)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            MountCrypt().print_usage()
            sys.exit()
        elif opt in ('-v', '--version'):
            MountCrypt().print_version()
            sys.exit()
        elif opt in ('-c', '--config'):
            if opt in ('-n', '--non-interactive'):
                mc = MountCrypt(interactive=False)
            else:
                mc = MountCrypt()
            mc.read_config(arg)
            mc.mount_volumes()
        else:
            MountCrypt().print_error(opt)

    if not opts:
        MountCrypt().print_error(argv)


if __name__ == "__main__": main(sys.argv[1:])
