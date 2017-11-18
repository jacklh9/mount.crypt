# mount.crypt
Script to decrypt encrypted luks volumes and mount with multiple mount points


USAGE:

mount.crypt.py [options]


OPTIONS

    -c, --config <my-config.ini>     Configuration file
    
    -h, --help                    Print this help
    

EXAMPLE CONFIG FILE:

    See mount.crypt.ini


SAMPLE RUN:

Using config ./mount.crypt.ini

Volume: backup_2.7T_1
UUID: 217b80b0-9450-45bd-be92-627f61e65542
Volume not present. Skipping...

Volume: backup_2.7T_2
UUID: 518788f9-3745-4cdf-8e77-aa7221391bb7
Volume not present. Skipping...

Volume: backup_7.3T_1
UUID: 4a3ea0d2-33cd-49eb-b3f7-5bdfb7a73633
Volume already decrypted.
Mounting: /mnt/backup/backup_7.3T_1
Already mounted. Skipping...
TASK: rm -f /mnt/backupfs;ln -s /mnt/backup/backup_7.3T_1 /mnt/backupfs
Run the above task? ([y],n): 

Volume: backup_7.3T_2
UUID: 4cec462e-9887-4026-8006-cce6dc2b5f9b
Volume not present. Skipping...

Volume: backup_7.3T_3
UUID: 761ee0a2-016a-4164-8ecb-54b07a4f18fd
Volume not present. Skipping...

Volume: backup_7.3T_2016
UUID: 9b4ecc2c-1770-4a8b-a0ae-984196659f52
Volume not present. Skipping...

Volume: backup_internal_3.6T_1
UUID: 379cc93b-cc72-4589-a762-fba6caba379b
Volume already decrypted.
Mounting: /mnt/backup/backup_internal_3.6T_1
Already mounted. Skipping...
No tasks to run for this volume.

Volume: external-nr
UUID: 309e8b83-a077-4fbf-98fc-b56e2a0ba197
Volume not present. Skipping...

Volume: data
UUID: 6b18acce-1bc9-46e6-be71-2a181b3fb725
Volume already decrypted.
Mounting: /mnt/data
Already mounted. Skipping...
Mounting: /mnt/datafs
Already mounted. Skipping...
Mounting: /opt/vbox
Already mounted. Skipping...
TASK: lxc start morpheus trinity
Run the above task? ([y],n): n
Skipping...
TASK: lxc list
Run the above task? ([y],n): n
Skipping...
TASK: VBoxManage list vms
Run the above task? ([y],n): 
TASK: VBoxManage list runningvms
Run the above task? ([y],n): 
[1m[3m#[23m[1m[0m                                                                                   [0m[23m[24m[Jthe-matrix# [K[?1h=[?2004h[?2004l

Script done on Sat 18 Nov 2017 01:06:28 AM PST
