from pexpect_ssh_walk import pexpect_ssh_walk, pexpect_ssh_walk_list
from getpass import getpass
import pexpect
from time import sleep

password = getpass("Password for SSH to server: ")
file_location = "/home/server/Documents"

child = pexpect.spawnu("ssh server@mainserver")
index = child.expect_exact(["server@mainserver's password: ", pexpect.TIMEOUT, pexpect.EOF, ], timeout=1)
if index == 0:
    child.sendline(password)
    sleep(0.5) # wait for a moment to allow the terminal SSH output to get saved to the buffer
else:
    print('Failed to estabilish SSH connection.')
    exit()

for root, dirs, files in pexpect_ssh_walk(child, file_location):
    print(root)
    for file in files:
        print('\t'+file)
    for dir in dirs:
        print('\t'+dir)