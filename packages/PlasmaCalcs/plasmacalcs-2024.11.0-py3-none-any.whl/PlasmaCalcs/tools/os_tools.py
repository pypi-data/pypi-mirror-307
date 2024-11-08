"""
File Purpose: os tools
e.g. for managing files & directories.
"""
import os


''' --------------------- Changing Directories --------------------- '''

class InDir():
    '''context manager for remembering directory.
    upon enter, cd to directory (default os.curdir, i.e. no change in directory)
    upon exit, original working directory will be restored.

    For function decorator, see tools.maintain_cwd.
    '''

    def __init__(self, directory=os.curdir):
        self.cwd = os.path.abspath(os.getcwd())
        self.directory = directory

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.cwd)


def with_dir(directory):
    '''returns a function decorator which:
    - changes current directory to <directory>.
    - runs function
    - changes back to original directory.
    '''
    def decorator(f):
        @functools.wraps(f)
        def f_but_enter_dir(*args, **kwargs):
            with InDir(directory):
                return f(*args, **kwargs)
        return f_but_enter_dir
    return decorator

# define a new function decorator, maintain_cwd, which maintains current directory:
maintain_cwd = with_dir(os.curdir)

maintain_directory = maintain_cwd  # alias
maintain_dir = maintain_cwd  # alias


''' --------------------- Path names --------------------- '''

def get_paths_with_common_start(common_start, dir=os.curdir, *, exclude_if=None):
    '''return list of abspaths to paths in dir which start with common_start.
    common_start: str
        if abspath, compare to abspaths from dir, else compare to relpaths from dir.
    exclude_if: None or callable
        if provided, exclude any paths for which exclude_if(path). (using path=abspath)
    '''
    listdir = sorted(os.listdir(dir))
    if os.path.isabs(common_start):
        paths = [os.path.abspath(os.path.join(dir, path)) for path in listdir]
        paths = [path for path in paths if path.startswith(common_start)]
    else:
        paths = [os.path.abspath(path) for path in listdir if path.startswith(common_start)]
    if exclude_if is not None:
        paths = [path for path in paths if not exclude_if(path)]
    return paths

def next_unique_name(desired_name, existing_names):
    '''return a name like desired_name but which is not in existing_names.
    If desired_name is in existing_names,
        Appends '_N' where N is smallest integer>0 that produces a unique name.
    '''
    if desired_name not in existing_names:
        return desired_name
    maybe_matches = [name for name in existing_names if name.startswith(desired_name)]
    i = 1
    while desired_name + f'_{i}' in maybe_matches:
        i += 1
    return desired_name + f'_{i}'


''' --------------------- File Memory Usage --------------------- '''

def nbytes_path(path=os.curdir):
    '''returns total size (in bytes) of all files implied by path.
    path: str
        file --> size of file
        directory --> total size of all files in directory and subdirectories, recursively.
    '''
    if os.path.isfile(path):
        return os.path.getsize(path)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):  # only add if not a symbolic link
                total_size += os.path.getsize(fp)
    return total_size
