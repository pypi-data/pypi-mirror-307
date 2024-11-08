"""
File Purpose: misc tools for input/output to files.

For checking file existence or creating new files, see os_tools instead.
"""

import ast
import os


''' --------------------- attempt to eval string --------------------- '''

def attempt_literal_eval(s):
    '''returns ast.literal_eval(s), or s if the literal_eval fails.'''
    try:
        return ast.literal_eval(s)
    except Exception as err:
        # failed to evaluate. Might be string, or might be int with leading 0s.
        if isinstance(err, SyntaxError):  # <-- occurs if s is an int with leading 0s.
            try:
                return int(s)
            except ValueError:
                # failed to convert to int; return original string.
                pass
        return s


''' --------------------- parse params from idl-like file --------------------- '''

def read_idl_params_file(filename, *, eval=True, as_tuples=False):
    '''parse idl file of params into a python dictionary of params.

    filename: string
        file to read from.
    eval: bool, default True
        whether to attempt to evaluate the values,
        using ast.literal_eval (safer but less flexible than eval).
        if True, try to evaluate values but use strings if evaluation fails.
        if False, values will remain as strings.
    as_tuples: bool, default False
        if True, return list of tuples instead of dictionary.
        list of tuples guaranteed to appear in the same order as in the idl file.

    File formatting notes:
        - semicolons (;) are used for comments. (idl format)
        - ignore blank lines & lines that don't assign a variable (missing '=')
        - ignores all leading & trailing whitespace in vars & values.
    '''
    filename = os.path.abspath(filename)  # <-- makes error messages more verbose, if crash later.
    # read the file lines.
    with open(filename, 'r') as file:
        lines = file.readlines()
    # remove comments
    lines = [line.split(";",1)[0] for line in lines]
    # trim whitespace
    lines = [line.strip() for line in lines]
    # remove empty lines, and remove lines without an equal sign.
    lines = [line for line in lines if line!='' and ('=' in line)]
    # split lines into vars & values
    var_value_pairs = [line.split("=",1) for line in lines]
    # cleanup whitespace in vars & values
    var_value_pairs = [(var.strip(), value.strip()) for (var, value) in var_value_pairs]

    if eval:
        var_value_pairs = [(var, attempt_literal_eval(value)) for (var, value) in var_value_pairs]

    return var_value_pairs if as_tuples else dict(var_value_pairs)
