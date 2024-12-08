from pexpect_ssh_walk import pexpect_ssh_walk, pexpect_ssh_parse_folder
from getpass import getpass
import pexpect

password = getpass()
file_location = "/home/server/Documents/"

child = pexpect.spawnu("ssh server@mainserver")
index = child.expect_exact(["server@mainserver's password: ", pexpect.TIMEOUT, pexpect.EOF, ], timeout=1)
if index == 0:
    child.sendline(password)
else:
    print('Failed to estabilish SSH connection.')
    exit()
    
for dirs, files in pexpect_ssh_walk(child, file_location):
    for file in files:
        print(file)
    for dir in dirs:
        print(dir)
        dirs2, files2 = pexpect_ssh_parse_folder(child, file_location+dir)
        for dir2 in dirs2:
            print("\t"+dir2)
        for file2 in files2:
            print("\t"+file2)