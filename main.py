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
#                (special value of None indicates N-many values)
# num_pos_args - # of positional args
#                (None indicates N-many values)
# 

# sort example_file

# prog: sort
# pos:  [example_file]

# sort -o out_file example_file

# prog: sort
# opt:  [(o, out_file)]
# pos:  [example_file]

# sort -oout_file example_file

# prog: sort
# opt:  [(o, out_file)]
# pos:  [example_file]

# sort --output=out_file example_file

# prog: sort
# opt:  [(output, out_file)]
# pos:  [example_file]
