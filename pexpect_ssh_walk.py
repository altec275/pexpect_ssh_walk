
import pexpect


def pexpect_ssh_walk(terminal, directory=None):
    walk_tuple = pexpect_ssh_parse_folder(terminal, directory)
    yield walk_tuple
    if walk_tuple[1] != []:
        for dir in walk_tuple[1]:
            yield from pexpect_ssh_walk(terminal, walk_tuple[0]+'/'+dir)


def pexpect_ssh_walk_list(terminal, directory):
    walk_tuple_list = []
    walk_tuple_list.append(pexpect_ssh_parse_folder(terminal, directory))
    for dir in walk_tuple_list[0][1]:
        walk_tuple_list.append(pexpect_ssh_walk_list(terminal, walk_tuple_list[0][0]+'/'+dir))
    return walk_tuple_list


def pexpect_ssh_parse_folder(terminal, directory=None):
    
    filelist = []
    folderlist = []

    # If a directory is specified, append that command
    if directory is None:
        dir_command = 'dir -N -p -1'
    else:
        dir_command = 'dir -N -p -1 "' + directory + '"'
    
    # Parse the output of the dir command
    terminal.sendline(dir_command)
    discard_buffer = True
    while True:
        index = terminal.expect([r'(.*?\n)', "No such file or directory", pexpect.EOF, pexpect.TIMEOUT, ], timeout=0.5)
        if index != 0:
            break
        match_file = terminal.match.groups()
        if discard_buffer:
            if dir_command in match_file[0]:
                discard_buffer = False
        else:
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
                
    # If no base directoy was specified, get the current directory
    if directory is None:
        directory = pexpect_ssh_current_directory(terminal)
            
    return (directory, folderlist, filelist)


def pexpect_ssh_current_directory(terminal):
    dir_command = 'echo "$PWD"'
    terminal.sendline(dir_command)
    discard_buffer = True
    while(True):
        index = terminal.expect([r'(.*?\n)', "No such file or directory", pexpect.EOF, pexpect.TIMEOUT, ], timeout=0.5)
        if index != 0:
            break
        match_root = terminal.match.groups()
        if discard_buffer:
            if dir_command in match_root[0]:
                discard_buffer = False
        else:
            name_string = match_root[0][:-2]
            index = name_string.find('\r')
            return name_string[1+index:]
