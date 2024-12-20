import pexpect

def pexpect_ssh_walk(terminal, root):

    # Lists to store directory contents
    files = []
    subdirs = []

    # Parse the output of the dir command
    dir_command = 'dir -N -p -1 "' + root + '"'
    terminal.sendline(dir_command)
    
    # Loop through the buffer
    discard_buffer = True
    while True:
        # Get the current line
        index = terminal.expect([r'(.*?\n)', "No such file or directory", pexpect.EOF, pexpect.TIMEOUT, ], timeout=0.1)
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
                subdirs.append(name_string[:-1])
            # Otherwise, save as a file name
            else:
                files.append(name_string)
                
    # Yield the current root directory contents
    yield (root, subdirs, files)
    
    # Recursive loop through subdirectories
    for dir in subdirs:
        yield from pexpect_ssh_walk(terminal, root+'/'+dir)
