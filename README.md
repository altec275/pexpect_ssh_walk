## pexpect_ssh_walk

Python3 utilities for iterating through files via SSH using pexpect.

#### `iterator pexpect_ssh_walk(pexpect child, string directory)`

Usage similar to os.walk().  Used to allow iterating through files in a for loop.

#### `tuple list pexpect_ssh_walk_list(pexpect child, string directory)`

Returns the full list of tuples generated in the directory walk operation.

#### `tuple pexpect_ssh_parse_folder(pexpect child, string directory)`

Returns a single directory walk tuple for the given root directory only.

#### `string pexpect_ssh_current_directory(pexpect child)`

Returns the string name of the current directory.
