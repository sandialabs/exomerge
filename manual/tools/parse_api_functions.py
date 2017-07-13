import inspect
import re

import exomerge

# get list of functions and members
# ignore uppercase values
# ignore special functions
# ignore hidden functions
functions = [x
             for x in dir(exomerge.ExodusModel)
             if x == x.lower() and x[0] != '_']

example_header = '\nExample'


# descriptions for each argument
description = dict()
description['adjust_displacement_field'] = ('If `True`, the displacement '
                                            'field will be updated if it '
                                            'exists.')
description['angle_in_degrees'] = 'An angle given in degrees.'
description['axis'] = 'A vector describing an axis.'
description['calculate_location'] = ('If `True`, the location of this value '
                                     'will be calculated and stored.')
description['calculate_block_id'] = ('If `True`, the element block containing '
                                     'this value will be calculated and '
                                     'stored.')
description['check_for_merged_nodes'] = ('If `True`, check for merged nodes '
                                         'between element blocks to avoid '
                                         'inconsistent output.')
description['colorspace'] = 'Colorspace to use.'
description['connectivity'] = ('A list of node indices defining the element '
                               'connectivity.')
description['current_element_block_id'] = 'An element block id.'
description['current_element_field_name'] = 'An element field name'
description['current_global_variable_name'] = 'A global variable name.'
description['current_node_field_name'] = 'A node field name.'
description['current_node_set_field_name'] = 'A node set field name.'
description['current_node_set_id'] = 'A node set id.'
description['current_side_set_field_name'] = 'A side set field name.'
description['current_side_set_id'] = 'A side set id.'
description['current_timestep'] = 'A timestep value.'
description['displacement_timestep'] = ('The timestep value to use for '
                                        'displacement values.')
description['duplicate_nodes'] = ('If `True`, new nodes will be created for '
                                  'the new element block.  Else, nodes will '
                                  'be reused.')
description['element_block_id'] = 'An element block id.'
description['element_block_ids'] = 'A list of element block ids.'
description['element_field_name'] = 'An element field name.'
description['element_field_name_prefix'] = 'A prefix for an element field.'
description['element_field_names'] = 'A list of element field names.'
description['export_exodus_copy'] = ('If `True`, a copy of the model will '
                                     'also be output to an Exodus file.')
description['expression'] = 'An expression to evaluate.'
description['field_range'] = 'The range of field values.'
description['filename'] = 'A filename.'
description['from_element_field_names'] = 'A list of element field names.'
description['global_variable_name'] = 'A global variable name. '
description['global_variable_names'] = 'A list of global variable names.'
description['info'] = 'See function description.'
description['interpolation'] = 'An interpolation type.'
description['intervals'] = 'The number of intervals to use.'
description['new_element_block_id'] = 'An element block id.'
description['new_element_field_name'] = 'An element field name.'
description['new_element_type'] = 'An element type.'
description['new_global_variable_name'] = 'A global variable name.'
description['new_node_field_name'] = 'A node field name.'
description['new_node_set_field_name'] = 'A node set field name.'
description['new_node_set_id'] = 'A node set id.'
description['new_node_set_members'] = 'A list of node indices.'
description['new_nodes'] = 'A list of node indices.'
description['new_side_set_field_name'] = 'A side set field name.'
description['new_side_set_id'] = 'A side set id.'
description['new_side_set_members'] = 'A list of side set members.'
description['new_timestep'] = 'A timestep value.'
description['node_field_name'] = 'A node field name.'
description['node_field_names'] = 'A list of node field names.'
description['node_set_field_name'] = 'A node set field name.'
description['node_set_field_names'] = 'A list of node set field names.'
description['node_set_id'] = 'A node set id.'
description['node_set_ids'] = 'A list of node set ids.'
description['node_set_members'] = 'A list of node indices.'
description['normal'] = 'A vector describing a normal.'
description['old_element_block_id'] = 'An element block id.'
description['point'] = 'A vector describing a point.'
description['relative_tolerance'] = 'A tolerance value.'
description['scale'] = 'The scale factor.'
description['scheme'] = 'A name of the scheme.'
description['side_set_field_name'] = 'A side set field name.'
description['side_set_field_names'] = 'A list of side set field names.'
description['side_set_id'] = 'A side set id.'
description['side_set_ids'] = 'A list of side set ids.'
description['side_set_members'] = 'A list of element faces.'
description['suppress_warnings'] = ('If `True`, warning messages will not be '
                                    'output.')
description['target_element_block_id'] = 'An element block id.'
description['timestep'] = 'A timestep value'
description['timesteps'] = 'A list of any number of timesteps.'
description['tolerance'] = 'A tolerance value.'
description['value'] = 'A value.'
description['vector'] = 'A vector.'
description['zero_member_warning'] = ('If `True` and the list evaluates to '
                                      'zero members, output a warning.')
description['delete_orphaned_nodes'] = ('If `True`, nodes which are no longer '
                                        'referenced will be deleted.')

def escaped(text):
    """Escape characters for text mode."""
    return re.sub('_', '\_', text)

def to_code(text):
    """Convert text to work inside a \code bracket."""
    return '\code{' + escaped(text) + '}'

#translate '`text`' in descriptions to '\code{text}'
for key, value in description.items():
    new_value = re.sub(r'`([^`]*)`', r'\code{\1}', value)
    new_value = escaped(new_value)
    if value != new_value:
        description[key] = new_value

# make sure we have a description for each argument
all_descriptions = True
for name in sorted(functions):
    function = getattr(exomerge.ExodusModel, name)
    # get the interface as a single line
    interface = inspect.getsource(function)
    interface = interface[:interface.find(':') + 1].strip()
    interface = re.sub(r'[ \n]+', ' ', interface)
    # get the non-self arguments
    arguments = [x.strip()
                 for x in interface[interface.find('(') + 1:].split(',')]
    arguments = [re.sub(r'[^a-z_].*', '', x) for x in arguments]
    # ignore empty arguments (such as *args and **kwargs)
    arguments = [x for x in arguments if x]
    if arguments[0] == 'self':
        del arguments[0]
    for x in arguments:
        if not x in description:
            print 'Add description for "%s" argument in "%s"' % (x, name)
            all_description = False

if not all_descriptions:
    exit(1)
    
# process each function
print '%% Note: This file was generated by the parse_api_functions.py script.'
for name in sorted(functions):
    function = getattr(exomerge.ExodusModel, name)
    # get the interface as a single line
    interface = inspect.getsource(function)
    interface = interface[:interface.find(':') + 1].strip()
    interface = re.sub(r'[ \n]+', ' ', interface)
    # get the non-self arguments
    arguments = [x.strip()
                 for x in interface[interface.find('(') + 1:].split(',')]
    arguments = [re.sub(r'[^a-z_].*', '', x) for x in arguments]
    # ignore empty arguments (such as *args and **kwargs)
    arguments = [x for x in arguments if x]
    if arguments[0] == 'self':
        del arguments[0]
    # format the interface to fit in a console width
    if len(interface) > 79:
        header_length = interface.find('(') + 1
        interface = re.sub(r', ', ',\n' + ' ' * header_length, interface)
    # ensure it fits
    if max(len(x) for x in interface.split('\n')) > 79:
        print 'ERROR'
        exit(1)
    # get the info string
    notes = function.__doc__
    # parse into lines
    notes = [x.strip() for x in notes.split('\n')]
    # extract examples
    notes = '\n'.join(notes)
    if example_header in notes:
        example = notes[notes.find(example_header):]
        example = example[example.find('\n') + 1:]
        example = example[example.find('\n') + 1:].strip()
        notes = notes[:notes.find(example_header)].strip()
    else:
        example = ''
    notes = notes.split('\n')
    # remove leading/trailing newlines
    while notes[0] == '':
        notes = notes[1:]
    while notes[-1] == '':
        notes = notes[:-1]
    syntax=None
    # escape things appropriately
    syntax = 'regular'
    i = 0
    notes.append('')
    while i < len(notes):
        # look for the end of the example
        if syntax == 'example' and not notes[i]:
            notes[i:i] = ['\end{pythoncode}']
            i += 1
            syntax = 'regular'
            continue
        # look for the end of the list
        if syntax == 'list' and (not notes[i] or notes[i][0] != '*'):
            notes[i:i] = [r'\end{itemize}']
            i += 1
            syntax = 'regular'
            continue
        # regular statement
        if syntax == 'regular':
            # look for beginning of a list
            if notes[i] and notes[i][0] == '*':
                syntax = 'list'
                notes[i:i] = [r'\begin{itemize}\setlength{\itemsep}{-0.6em}']
                notes[i:i] = [r'\vspace{-2em}']
                notes[i:i] = ['']
                i += 3
                continue
            # look for beginning of an example
            if notes[i] and notes[i][:3] == '>>>':
                syntax = 'example'
                notes[i:i] = [r'\begin{pythoncode}']
                i += 1
                continue
            # convert "'text'" into "\code{text}"
            notes[i] = re.sub(r"'([^']*)'", r"\code{\1}", notes[i])
            # add underscores
            notes[i] = escaped(notes[i])
        # list
        elif syntax == 'list':
            notes[i] = r'\item' + escaped(re.sub(r"'([^']*)'", r"\code{\1}", notes[i][1:]))
        # python code
        elif syntax == 'example':
            pass
        i += 1
    # reform as a single string
    notes = '\n'.join(notes)
    print r''
    print r''
    #print r'\clearpage'
    #print r'\vspace{1.5cm}'
    print r'\vfill'
    print r'\section*{%s}' % escaped(name)
    print r'\index{\code{%s}}' % escaped(name)
    print r''
    print r'%s' % notes
    print r''
    print r'\textit{\small Interface}'
    print r''
    print r'\begin{pythoncode}'
    print r'%s' % interface
    print r'\end{pythoncode}'
    print r''
    if arguments:
        print r'\textit{\small Parameters}'
        print r''
        print r'\hspace*{0.43in}'
        print r'\begin{tabularx}{5.4in}{lX}'
        table_rows = ['\code{' + escaped(name) + '} & ' + description[name]
                      for name in arguments]
        print '%s' % ' \\\\[5pt]\n'.join(table_rows)
        print r'\end{tabularx}'
    else:
        print r'\textit{\small No parameters}'
    print r''
    if example:
        print r'\textit{\small Example}'
        print r''
        print r'\begin{pythoncode}'
        print r'%s' % example
        print r'\end{pythoncode}'
    else:
        print r'\textit{\small No example code}'
# print out the information

#for name in sorted(needed_arguments):
#    print 'description[\'%s\'] = \'\'' % name
