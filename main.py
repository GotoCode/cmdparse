#
# cmdparse
#
# this utlity extracts the command name, positional
# arguments, and optional arguments (short & long form)
# from a given string representing a command-line input
# 
# the format of the command line interface (command name,
# required arguments, options, short/long aliases, etc.)
# must be specified in a JSON file called "fmt.json"
#
# An single entry in fmt.json is below:
#
# {
#   "cmd" : "sort",
#   "opt_short" : ["o", "r"],
#   "opt_long" : ["output", "reverse"],
#   "num_opt_vals" : [1, 0],
#   "num_pos_args" : None
# }
#
# fmt.json consists of a list of such
# entries, one per command line program
#
# Description of JSON attributes:
# 
# cmd - name of command line program (sort, cat, etc.)
# opt_short - short-form options (flags) for the program
# opt_long - long-form options (flags) for the program
#            (order *must* match that of flags in opt_short)
# num_opt_vals - number of values for each option
#                (order *must* match that of flags in opt_short)
#                (special value of -1 indicates N-many values)
# num_pos_args - # of positional args
#                (special value of -1 indicates N-many values)
#

import json

def load_format():
    '''
    This function loads in the data from fmt.json to determine
    the appropriate format for various commands (cat, sort, etc.)
    and returns this loaded data as a dictionary object
    '''

    cmd_fmt = {}

    with open('fmt.json') as f:

        raw_json = json.load(f)

    for o in raw_json:

        cmd_fmt[o['cmd']] = o

    return cmd_fmt

def parse(cmd_str):
    '''
    Given an input string representing a command line input,
    this function extracts information about the command name,
    required arguments, optional arguments, flags, etc.
    '''

    pass

# main user interface
if __name__ == '__main__':

    print(load_format())

    #while True:
    
    #    cmd_input = input('Enter shell input string: ')
    #    print(parse(cmd_input), end='\n\n')
    
