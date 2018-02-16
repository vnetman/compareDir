# compareDir

Given two directories ("right" and "left"), detects what files in "right" are
absent in "left", and vice versa.

Uses the file's md5 checksum as the basis for file identity, and therefore can
detect renamed files.

This tool can be used to check whether, for example, all photos on your phone
have been backed up to your backup storage device.

