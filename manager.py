"""

.. module:: 	DDWRT-RSA-MANAGER
   :platform: 	Unix
   :synopsis: 	This simple script updates the authorized SSH 
   			  	keys of a DD-WRT device from a JSON key database.

.. moduleauthor:: Gregory A. Lussier <greg@gregoryalussier.com>

"""

#!/usr/bin/python
import paramiko
import os
import simplejson as json

# SSH Connection Parameters
HOST					= "192.168.1.1" # YOUR DEVICE'S IP ADDRESS
PORT					= 22 # THE SSHD PORT
USERNAME 				= "root" # USERNAME (should be root)
PRIVATE_KEY_FILE_PATH 	= "~/.ssh/id_rsa" # YOUR ACTUAL PRIVATE KEY TO CONNECT TO THE DEVICE

# SSH Presets
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
privatekeyfile = os.path.expanduser(PRIVATE_KEY_FILE_PATH)
mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)

# SSH Connection
ssh.connect(HOST, username=USERNAME, pkey = mykey)
stdin, stdout, stderr = ssh.exec_command('nvram get sshd_authorized_keys')

# Keys Retrieval
keyList = stdout.readlines()

# Key Database
data = json.load(open("data.json"))

# Building Final String
finalString = ""
for user in data["users"]:
	print user["name"] + " : " + str(len(user["ssh-keys"])) + " keys"
	for key in user["ssh-keys"]:
		print "\t-> " + str(key.keys()[0])
		finalString = finalString + str(key[key.keys()[0]]) + "\n"
print finalString
f = open("data.txt","w")
f.write(finalString)
f.close()

# SFTP
transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USERNAME, pkey=mykey)
sftp = paramiko.SFTPClient.from_transport(transport)
remotePath = "/tmp/data.txt"
localPath = "data.txt"
sftp.put(localPath, remotePath)
sftp.close()
transport.close()

# SSH Connection and Command Execution
ssh.connect(HOST, username=USERNAME, pkey = mykey)
command = """sh -c 'nvram set sshd_authorized_keys="$(cat /tmp/data.txt)";' &&
 rm /tmp/data.txt && nvram commit"""
stdin, stdout, stderr = ssh.exec_command(command)