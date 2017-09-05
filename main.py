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
#   "num_pos_args" : -1
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

        cmd_info = fmt[cmd_name]

        i = 1

        while i < len(tokens):

            arg = tokens[i]

            # case: long-form option
            if arg.startswith('--'):

                valid_flag = False
                selected_opt = None
                
                # check if the specified flag (arg) is a valid option (opt)
                for opt in fmt[cmd_name]['opt_long']:

                    if arg == '--' + opt or arg.startswith('--' + opt + '='):

                        valid_flag   = True
                        selected_opt = opt
                        break

                if not valid_flag:

                    return "Error: Invalid long-form option '{}'".format(arg)

                # extract the long-form option name
                opt_name = arg[2:arg.index('=')] if '=' in arg else arg[2:]

                # list of values for the specified option
                opt_vals = []

                # extract the first option value, if possible
                if arg.startswith('--' + opt_name + '=') and len(arg) > len('--' + opt_name + '='):

                    opt_vals.append(arg[len('--' + selected_opt + '='):])

                i += 1

                if '=' in arg and len(opt_vals) == 0:

                    return 'Error: No arguments provided to "{}"'.format(opt_name)

                # determine number of values for this option
                num_vals = cmd_info['num_opt_vals'][cmd_info['opt_long'].index(opt_name)]

                # extract all values for this option and
                # stop once we hit the next option flag
                while i < len(tokens) and not tokens[i].startswith('-'):

                    # extract exactly num_vals-many argument values (or N-many if num_vals == -1)
                    if num_vals == -1 or len(opt_vals) < num_vals:

                        opt_vals.append(tokens[i])
                        i += 1

                    else:

                        break

                if len(opt_vals) < num_vals:

                    return 'Error: Insufficient input values for "{}"'.format(opt_name)

                opt_args.append((opt_name, opt_vals))

            # case: short-form option
            elif arg.startswith('-'):

                valid_flag = False

                # check if the specified flag (arg) is valid option (opt)
                # Note: this code can interpret '-ooutputfile' as '-o outputfile'
                for opt in fmt[cmd_name]['opt_short']:

                    valid_flag = valid_flag or arg.startswith('-' + opt)

                if not valid_flag:

                    return "Error: Invalid short-form option '{}'".format(arg)

                # extract the short-form option name
                opt_name = arg[1:2]

                # list of values for given short-form option
                opt_vals = []

                # extract the first option value, if it exists (i.e. -oout.txt == -o out.txt)
                if len(arg) > 2:
                
                    opt_vals.append(arg[2:])
                
                i += 1

                # determine the number of values for this option
                num_vals = cmd_info['num_opt_vals'][cmd_info['opt_short'].index(opt_name)]

                # extract all values for this option and
                # stop once we hit the next option flag
                while i < len(tokens) and not tokens[i].startswith('-'):

                    # extract exactly num_vals-many argument values (or N-many if num_vals == -1)
                    if num_vals == -1 or len(opt_vals) < num_vals:

                        opt_vals.append(tokens[i])
                        i += 1

                    else:

                        break

                if len(opt_vals) < num_vals:

                    return 'Error: Insufficient input values for "{}"'.format(opt_name)

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

