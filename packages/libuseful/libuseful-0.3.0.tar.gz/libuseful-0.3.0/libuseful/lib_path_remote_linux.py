############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)


def join_paths(path1: str, path2: str) -> str:
    if path1.endswith("/") is False:
        path1 += "/"
    if path2.startswith("/") is True:
        path2 = path2[1:]
    return path1 + path2    


def get_dirpath(filepath: str):
    """
    Returns the Directory path.
    """
    return filepath[ :filepath.rfind("/")]


def get_filename(filepath: str):
    """
    Returns the filename
    Args:      None
    Returns:   A string indicating ROOT path.
    """
    if filepath.endswith("/") is True:
        raise RuntimeError("filepath is dirpath. please check it.")
    return filepath[ filepath.rfind("/")+1:]


def split_filename_ext(filepath):
    file_name = filepath[ :filepath.rfind(".")-1]
    extension = filepath[ filepath.rfind(".")+1:]
    return file_name, extension


def get_relpath(target_abs_path: str, base_path: str) -> str:
    """
    Convert absolute-path to relative-path & Return Full-Path.
    :param target_abs_path:
    :param base_path:
    :return:
    """
    if base_path.endswith("/") is True:
        base_path = base_path[:base_path.rfind("/")-1]
        
    start_idx = target_abs_path.find(base_path) + len(base_path)
    rel_path = target_abs_path[start_idx:]
    
    if rel_path.startswith("/") is True:
        rel_path = rel_path[1:]
    return rel_path

