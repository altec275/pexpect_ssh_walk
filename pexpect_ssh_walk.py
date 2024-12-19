import pexpect


def pexpect_ssh_walk(terminal, directory):
    
    # Parse the current directory
    walk_tuple = pexpect_ssh_parse_folder(terminal, directory)
    # Yield the current directory
    yield walk_tuple
    # Recursive loop through subdirectories
    for dir in walk_tuple[1]:
        yield from pexpect_ssh_walk(terminal, walk_tuple[0]+'/'+dir)


def pexpect_ssh_parse_folder(terminal, directory):
    
    # Lists to store directory contents for return
    filelist = []
    folderlist = []

    # Parse the output of the dir command
    dir_command = 'dir -N -p -1 "' + directory + '"'
    terminal.sendline(dir_command)
    
    # Loop through the buffer
    discard_buffer = True
    while True:
        # Get the current line
        index = terminal.expect([r'(.*?\n)', "No such file or directory", pexpect.EOF, pexpect.TIMEOUT, ], timeout=0.5)
        # If no lines were found, exit the loop
        if index != 0:
            break
        # Get the contents of the current line
        match_file = terminal.match.groups()
        # If the buffer contents are prior to the dir output, discard
        if discard_buffer:
            if dir_command in match_file[0]:
                discard_buffer = False
        # If we have reached the dir echo, save the line
        else:
            # Clean extraneous characters from string
            name_string = match_file[0][:-2]
            if '\r' in name_string:
                index = name_string.find('\r')
                name_string = name_string[1+index:]
            # dir output formatted to add / at end of directories
            if name_string.endswith('/'):
                folderlist.append(name_string[:-1])
            # Otherwise, save as a file name
            else:
                filelist.append(name_string)
                
    return (directory, folderlist, filelist)