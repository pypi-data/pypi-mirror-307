"""
File Purpose: tools related to using a supercomputer / computer cluster.
"""
import os
import re


def find_files_re(pattern, dir=os.curdir, *, exclude=[]):
    '''find all files in this directory and all subdirectories which match the given pattern.

    pattern: str
        regular expression pattern to match filenames.
    exclude: str, or list of strs
        exclude any subdirectories whose name equals one of these strings or re.fullmatch one of these strings.
        E.g. exclude='*[.]io' will exclude all subdirectories whose name ends with '.io';
            exclude='parallel' will exclude all subdirectories whose name equals 'parallel'.
    
    returns list of abspaths to all files found.
    '''
    files = []
    pattern = re.compile(pattern)
    exclude = [exclude] if isinstance(exclude, str) else exclude
    exclude = [re.compile(str(excl)) for excl in exclude]
    for dirpath, dirnames, filenames in os.walk(dir, topdown=True):
        this_dir_name = os.path.basename(dirpath)
        if any((excl==this_dir_name or excl.fullmatch(this_dir_name)) for excl in exclude):
            dirnames[:] = []
            continue
        for filename in filenames:
            if pattern.fullmatch(filename):
                files.append(os.path.abspath(os.path.join(dirpath, filename)))
    return files

def find_jobfiles(dir=os.curdir, *, exclude=[]):
    '''find all jobfiles in this directory and all subdirectories.
    jobfiles are files which end with '.o' or '.oN' where N is an integer with any number of digits.

    exclude: str, or list of strs
        exclude any subdirectories whose name equals one of these strings or re.fullmatch one of these strings.
        E.g. exclude='*[.]io' will exclude all subdirectories whose name ends with '.io';
        exclude='parallel' will exclude all subdirectories whose name equals 'parallel'.

    returns list of abspaths to all jobfiles found.
    '''
    return find_files_re('.*[.]o[0-9]*', dir=dir, exclude=exclude)

def find_slurmfiles(dir=os.curdir, *, exclude=[]):
    '''find all slurmfiles in this directory and all subdirectories.
    slurmfiles are files which end with '.slurm'.

    exclude: str, or list of strs
        exclude any subdirectories whose name equals one of these strings or re.fullmatch one of these strings.
        E.g. exclude='*[.]io' will exclude all subdirectories whose name ends with '.io';
        exclude='parallel' will exclude all subdirectories whose name equals 'parallel'.

    returns list of abspaths to all slurmfiles found.
    '''
    return find_files_re('.*[.]slurm', dir=dir, exclude=exclude)

def slurm_nodes_from_slurmfile(f):
    '''return number of nodes used, based on this slurm file.
    f: str, path to file containing a line like: "#SBATCH -N v" with v an integer.
    (There can be any amount of whitespace, and the line can also have a comment # after.)
    '''
    with open(f, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    #pattern = re.compile(r'#SBATCH -N (\d+)')
    pattern = re.compile(r'#SBATCH\s+-N\s+(\d+)\s*(#.*)?')
    matches = [pattern.fullmatch(line) for line in lines]
    matches = [match for match in matches if match is not None]
    Ns = [int(match.group(1)) for match in matches]
    if len(Ns) == 0:
        errmsg = f'failed to find any lines like "#SBATCH -N v" in file {f!r}'
        raise FileContentsMissingError(errmsg)
    if len(set(Ns)) > 1:
        errmsg = f'found multiple lines like "#SBATCH -N v" in file {f!r}\ngiving different v={Ns}'
        raise FileContentsConflictError(errmsg)
    return Ns[0]

def n_slurm_nodes(dir=os.curdir):
    '''return number of nodes used to run the run at this directory.
    searches all slurmfiles (see find_slurmfiles) to determine number of nodes,
        from line like "#SBATCH -N v" with v an integer.
    if result is ambiguous (different v from multiple places), raise a FileContentsConflictError.
    if no slurmfiles found, raise FileNotFoundError.
    if some slurmfiles found but none tell us how many nodes were used, raise FileContentsMissingError.
    '''
    dir = os.path.abspath(dir)
    slurmfiles = find_slurmfiles(dir)
    if len(slurmfiles) == 0:
        raise FileNotFoundError(f'no slurmfiles found in directory {dir!r}')
    Ns = []
    for f in slurmfiles:
        # ALL slurmfiles should have -N info. Otherwise, this will crash (as intended).
        N = slurm_nodes_from_slurmfile(f)
        Ns.append(N)
    if len(Ns) == 0:
        raise FileContentsMissingError(f'no slurmfiles found in directory {dir!r} which contain node info.')
    if len(set(Ns)) > 1:
        errmsg = (f'found multiple lines like "#SBATCH -N n" in slurmfiles {slurmfiles!r}\n'
                    f'giving different n={Ns}')
        raise FileContentsConflictError(errmsg)
    return Ns[0]
