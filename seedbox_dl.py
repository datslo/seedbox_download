from paramiko import SSHClient
from scp import SCPClient
import yaml
# import os 
# import glob

credentials = yaml.safe_load(open('credentials.yaml'))

host = credentials['seedbox']['host']
username = credentials['seedbox']['user']
password = credentials['seedbox']['password']
location = credentials['seedbox']['dl_location']

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, username=username, password=password)

files = []

stdin, stdout, stderr = ssh.exec_command('ls -tr ' + location)
for line in stdout:
    print(line.strip('\n'))

last_x_files = int(input("How many files do you want to download? (starting bottom up): "))
step = 0
stdin, stdout, stderr = ssh.exec_command('ls -tr ' + location + ' |tail -' + str(last_x_files))
for line in stdout:
    yes = line.strip('\n')
    files.append(location + yes)

while last_x_files > 0:
    file = files[step - 1]
    scp.get(file, recursive=True)
    last_x_files -= 1
    step -= 1

scp.close()
