# mount.crypt
Script to decrypt encrypted luks volumes and mount with multiple mount points

USAGE:

mount.crypt.py [options]

OPTIONS
    -c, --config <my-config.ini>     Configuration file
    -h, --help                    Print this help

EXAMPLE CONFIG FILE:

[DEFAULT]
cryptsetup=/sbin/cryptsetup
mount=/bin/mount

### Mount Definitions:
### ------------------
### NOTE: The mapper-name and mount-points need to also be defined and
### match the entries for these respective drives in /etc/fstab.
### 
### Example /etc/fstab btrfs mount-point entries:
### 
### LABEL=data      /mnt/data     btrfs     compress=lzo,defaults,noatime,noauto,nodiratime,subvol=@data  0       0
### LABEL=data      /opt/vbox       btrfs     compress=lzo,defaults,noatime,noauto,nodiratime,subvol=@vbox 0       0
### 
### mount.crypt.ini entry format:
###
### [mapper-name]
### UUID = abc...def
### mounts = /mnt/mount-point,/mnt/other-mount-point,...
###
### Optionally include any commands to run after a successful mount
### run_progs = my-script.sh --some-flag,my-other-script.sh
### 
### NOTE: Lists MUST NOT have ANY spaces nor double-quotes 
### in-between the comma delimiter.
###

[backup]
UUID=123ab45c-de67-8901-a234-bcd5efab678c
mounts=/mnt/backup

[data]
UUID=456ab45c-de67-8901-a234-bcd5efab601d
mounts=/mnt/data,/opt/vbox
run_progs=lxc start testbox devbox,lxc list


