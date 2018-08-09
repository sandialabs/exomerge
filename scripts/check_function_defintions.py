"""
This file checks function definitions to see if all arguments can be placed
on the same line.

Usage:
python check_function_definitions.py exomerge.py

"""

import os
import sys

filename = sys.argv[1]
with open(filename) as f:
    lines = f.readlines()
# append lines with starting line number
lines = [[i, x.replace('\n', '')]
         for i, x in enumerate(lines)]

# look for function definitions
function_lines = [i for i, x in lines if x.lstrip().startswith('def ')]

collapse_count = 0
for start_line in function_lines:
    definition = lines[start_line][1]
    # get full function definition string
    i = start_line
    while definition.rstrip()[-1] != ':':
        i += 1
        definition += lines[i][1]
    if i == start_line:
        continue
    # reformat
    while ',  ' in definition:
        definition = definition.replace(',  ', ', ')
    # get total length
    if len(definition) < 80:
        collapse_count += 1
        print('%d:%s'
              % (start_line + 1, definition.replace('(', ' ').split()[1]))
    #print definition
    #exit(1)

if not collapse_count:
    exit(0)
print('\nFound %d functions that need collapsed.')
exit(1)
