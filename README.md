## pexpect_ssh_walk

os.walk() over SSH.  

Python3 utilities for iterating through files via SSH using pexpect.

#### `iterator pexpect_ssh_walk(pexpect child, string directory)`

Usage similar to os.walk().  Used to allow iterating through files in a for loop.

#### `tuple pexpect_ssh_parse_folder(pexpect child, string directory)`

Returns a single directory walk tuple for the given root directory only.
