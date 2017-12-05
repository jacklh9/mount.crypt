# MountCrypt
Script to decrypt encrypted luks volumes and mount with multiple mount points


USAGE:

mountcrypt.py [options]


OPTIONS

    -c, --config <my-config.ini>    Configuration file
    -d, --decrypt                   Decrypt volumes [default]
    -D, --defaults                  Accept defaults for all Y/N prompts.
        NOTE: You may be prompted for decryption passphrase.
    -h, --help
    -u, --unmount                   Unmount volumes but don't close.
    -U, --close                     Unmount and close volumes.         

EXAMPLE CONFIG FILE:

    See mountcrypt.ini


SAMPLE RUN:

    root@hostbox # ./mountcrypt.sh
    Using config ./mountcrypt.ini
    
    Volume: backup_2.7T_1
    UUID: 217b80b0-1234-45bd-be92-627f61e65542
    Volume not present. Skipping...
    
    Volume: backup_2.7T_2
    UUID: 518788f9-1234-4cdf-8e77-aa7221391bb7
    Volume not present. Skipping...
    
    Volume: backup_7.3T_1
    UUID: 4a3ea0d2-abcd-49eb-b3f7-5bdfb7a73633
    Volume not present. Skipping...
    
    Volume: backup_7.3T_2
    UUID: 4cec462e-9887-1234-8006-cce6dc2b5f9b
    Decrypt? ([y],n):
    Enter passphrase:
    Mounting: /mnt/backup/backup_7.3T_2
    Mount? ([y],n):
    TASK: rm -f /mnt/backupfs;ln -s /mnt/backup/backup_7.3T_2 /mnt/backupfs
    Run the above task? ([y],n):
    
    Volume: backup_7.3T_3
    UUID: 761ee0a2-abcd-4164-8ecb-54b07a4f18fd
    Volume not present. Skipping...
    
    Volume: backup_7.3T_2016
    UUID: 9b4ecc2c-1234-4a8b-a0ae-984196659f52
    Volume not present. Skipping...
    
    Volume: backup_internal_3.6T_1
    UUID: 379cc93b-abcd-4589-a762-fba6caba379b
    Volume already decrypted.
    Mounting: /mnt/backup/backup_internal_3.6T_1
    Mount? ([y],n):
    No tasks to run for this volume.
    
    Volume: external-drive
    UUID: 309e8b83-abcd-4fbf-98fc-b56e2a0ba197
    Volume not present. Skipping...
    
    Volume: data
    UUID: 6b18acce-1234-4678-be71-2a181b3fb725
    Decrypt? ([y],n):
    Enter passphrase:
    Mounting: /mnt/data
    Mount? ([y],n):
    Mounting: /mnt/datafs
    Mount? ([y],n):
    Mounting: /opt/vbox
    Mount? ([y],n):
    TASK: lxc start testbox devbox
    Run the above task? ([y],n):
    TASK: lxc list
    Run the above task? ([y],n): n
    Skipping...
    TASK: VBoxManage list vms
    Run the above task? ([y],n): n
    Skipping...
    TASK: VBoxManage list runningvms
    Run the above task? ([y],n): n
    Skipping...
    
    
LICENSING

    jacklh9/mountcrypt is licensed under the GNU General Public
    License v3.0. See file LICENSE for details.
