import pexpect


def pexpect_ssh_walk(terminal, directory):
    
    yield pexpect_ssh_parse_folder(terminal, directory)
        

def pexpect_ssh_parse_folder(terminal, directory):
    
    filelist = []
    folderlist = []

    terminal.sendline('cd "'+directory+'"')
    index = terminal.expect(["No such file or directory",  pexpect.TIMEOUT, ], timeout=0.5)
    if index == 0:
        print(directory+" does not exist!")
        
    else:
        dir_command = 'dir -N -p -1'
        terminal.sendline(dir_command)
        start_parsing = False
        while True:
            index = terminal.expect([r'(.*?\n)', pexpect.TIMEOUT, ], timeout=0.5)
            if index == 1:
                break
            match_file = terminal.match.groups()
            if dir_command in match_file[0]:
                start_parsing = True
            elif start_parsing:
                name_string = match_file[0][:-2]
                if '\r' in name_string:
                    index = name_string.find('\r')
                    clean_name = name_string[1+index:]
                else:
                    clean_name = name_string
                if clean_name.endswith('/'):
                    folderlist.append(clean_name[:-1])
                else:
                    filelist.append(clean_name)
    
    return folderlist, filelist
