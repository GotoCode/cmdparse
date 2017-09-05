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

def parse(cmd_str, fmt):
    '''
    Given an input string representing a command line input,
    this function extracts information about the command name,
    required arguments, optional arguments, flags, etc.

    `fmt` represents the format object, as obtained from load_format
    '''

    cmd_name = None
    pos_args = []
    opt_args = []

    tokens = cmd_str.split()

    # extract command name from input
    if len(tokens) > 0:

        cmd_name = tokens[0]

    # if command exists, then process its argument list
    if cmd_name in fmt:

        i = 1

        while i < len(tokens):

            arg = tokens[i]

            # case: long-form option
            if arg.startswith('--'):

                # extract the long-form option name
                opt_name = arg[2:]
                i += 1

                # extract all values for this option and
                # stop once we hit the next option flag
                opt_vals = []
                
                while i < len(tokens) and not tokens[i].startswith('-'):

                    opt_vals.append(tokens[i])
                    i += 1

                opt_args.append((opt_name, opt_vals))

            # case: short-form option
            elif arg.startswith('-'):

                # extract the long-form option name
                opt_name = arg[1:]
                i += 1

                # extract all values for this option and
                # stop once we hit the next option flag
                opt_vals = []
                
                while i < len(tokens) and not tokens[i].startswith('-'):

                    opt_vals.append(tokens[i])
                    i += 1

                opt_args.append((opt_name, opt_vals))

            # case: positional argument
            else:

                pos_args.append(arg)
                i += 1

    else:

        return None

    return 'cmd: {}\npos args: {}\nopt args: {}'.format(cmd_name, pos_args, opt_args)
    

# main user interface
if __name__ == '__main__':

    fmt = load_format()

    while True:
    
        cmd_input = input('Enter shell input string: ')

        result = parse(cmd_input, fmt)
        
        if result:

            print(result, end='\n\n')

