# This will look through exomerge.py and attempt to find instances where
# a node_set function is used instead of a side_set function, and vice versa.
#
# Because the use of each of these is so similar, I continually run into bugs
# where I've copy-pasted a node_set function and failed to replace all
# instances to side_set.
#
# python check_node_side_discrepancies.py exomerge.py

import sys
import re

def running_sum(x):
  tot = 0
  for item in x:
    tot += item
    yield tot

def remove_single_quotes(line):
    in_single_quote = False
    in_double_quote = False
    last_was_backslash = False
    last_was_r = False
    in_raw_quote = False
    new_line = ''
    for x in line:
        # check for quote opening
        if not in_single_quote and not in_double_quote:
            if x == '\'':
                in_single_quote = True
                in_raw_quote = last_was_r
                last_was_r = False
                last_was_backslash = False
                continue
            if x == '\"':
                in_double_quote = True
                in_raw_quote = last_was_r
                last_was_r = False
                last_was_backslash = False
                continue
        # check for quote closing
        if in_single_quote and not last_was_backslash and x == '\'':
            in_single_quote = False
            last_was_r = False
            last_was_backslash = False
            continue
        if in_double_quote and not last_was_backslash and x == '\"':
            in_double_quote = False
            last_was_r = False
            last_was_backslash = False
            continue
        # if we're not in a quote, add it to the string
        if not in_single_quote and not in_double_quote:
            new_line += x
        if in_single_quote or in_double_quote:
            last_was_r = x == False
            if not last_was_backslash:
                last_was_backslash = x == '\\'
            else:
                last_was_backslash = False
        else:
            last_was_r = x == 'r'
            last_was_backslash = False
    return new_line

filename = sys.argv[1]
with open(filename) as f:
    lines = f.readlines()
# append lines with starting line number
lines = [[i, x.replace('\n', '')]
         for i, x in enumerate(lines)]
# TODO: strip out triple quotes

# strip out single
lines = [[x[0], remove_single_quotes(x[1])]
         for x in lines]
# strip out comment lines
lines = [x if '#' not in x[1] else [x[0], x[1][:x[1].index('#')]]
         for x in lines]
# now we need to combine statements which span multiple lines
parenthesis_level = [x[1].count('(') - x[1].count(')') +
                     x[1].count('[') - x[1].count(']') +
                     x[1].count('{') - x[1].count('}')
                     for x in lines]
net_parenthesis_level = [0]
for x in parenthesis_level:
    net_parenthesis_level.append(net_parenthesis_level[-1] + x)
assert net_parenthesis_level[-1] == 0
net_parenthesis_level = net_parenthesis_level[1:]

# combine lines which span multiple lines
new_lines = []
this_line = ''
for x, level in zip(lines, net_parenthesis_level):
    if this_line:
        this_line = this_line.rstrip() + ' ' + x[1].lstrip()
    else:
        this_line = x[1]
    if level == 0:
        new_lines.append([x[0], this_line])
        this_line = ''
lines = new_lines

# find indents
indents = [len(x[1]) - len(x[1].lstrip(' '))
          for x in lines]

# minimum indent to start checking

opening_parenthesis = '([{'
closing_parenthesis = ')]}'

# indent of node set opener
node_set_function_indent = 9999
# indent of side set opener
side_set_function_indent = 9999
for indent, (line_number, line) in zip(indents, lines):
    if indent <= node_set_function_indent:
        node_set_function_indent = 9999
    if indent <= side_set_function_indent:
        side_set_function_indent = 9999
    # check for node_set opener
    if node_set_function_indent > indent:
        if 'node_set' in line and not 'side_set' in line:
            node_set_function_indent = indent
    # check for side_set opener
    if side_set_function_indent > indent:
        if 'side_set' in line and not 'node_set' in line:
            side_set_function_indent = indent
    # if in a node set opener, check for side_set call
    if node_set_function_indent <= indent:
        if 'side_set' in line:
            print '%s:%d: %s' % (filename, line_number + 1, line)
            continue
    # if in a side set opener, check for node_set call
    if side_set_function_indent <= indent:
        if 'node_set' in line:
            print '%s:%d: %s' % (filename, line_number + 1, line)
            continue
    # check for node_set within side_set arguments, and vice versa
    # for example, this will catch self.node_sets[side_set_id]
    node_set_instances = [m.start() for m in re.finditer('node_set', line)]
    side_set_instances = [m.start() for m in re.finditer('side_set', line)]
    if not node_set_instances and not side_set_instances:
        continue
    parenthesis_level = [1 if x in opening_parenthesis else -1 if x in closing_parenthesis else 0
                         for x in line]
    parenthesis_level = list(running_sum(parenthesis_level))
    node_set_opener = [False]
    side_set_opener = [False]
    for i, x in enumerate(line):
        in_node_set_opener = any(node_set_opener[z]
                                 for z in xrange(parenthesis_level[i])) 
        in_side_set_opener = any(side_set_opener[z]
                                 for z in xrange(parenthesis_level[i])) 
        if parenthesis_level[i] >= len(node_set_opener):
            node_set_opener.append(False)
            side_set_opener.append(False)
        if i in node_set_instances:
            node_set_opener[parenthesis_level[i]] = True
            if in_side_set_opener and not in_node_set_opener:
                print '%s:%d: %s' % (filename, line_number + 1, line)
        if i in side_set_instances:
            side_set_opener[parenthesis_level[i]] = True
            if in_node_set_opener and not in_side_set_opener:
                print '%s:%d: %s' % (filename, line_number + 1, line)
        if x == ' ':
            node_set_opener[parenthesis_level[i]] = False
            side_set_opener[parenthesis_level[i]] = False
