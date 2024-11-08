############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import os
import copy
from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)


class CPath:

    @staticmethod
    def join_paths(path1: str, path2: str) -> str:
        if path2.startswith('/') is True or path2.startswith('\\') is True:
            path2 = path2[1:]
        return os.path.normpath(os.path.join(path1, path2)).strip()

    @staticmethod
    def get_rootpath():
        """
        Returns the Full-Path of this package's ROOT.
        Args:      None
        Returns:   A string indicating ROOT path.
        """
        root_dir = os.getcwd()
        # root_dir = os.path.dirname(sys.modules['__main__'].__file__)
        return os.path.normpath(root_dir)

    @staticmethod
    def get_module_root(module, internal_path=None):
        try:
            if module is None:
                raise RuntimeError("'module' is None.")
                
            module_path = os.path.dirname(module.__file__)
            if internal_path is not None:
                module_path = os.path.abspath( CPath.join_paths(module_path, internal_path) )
            return module_path
        except BaseException as e:
            logger.error(e)
            raise e

    @staticmethod
    def get_dirpath(filepath: str):
        """
        Returns the Directory path.
        """
        return os.path.dirname(filepath)

    @staticmethod
    def get_filename(filepath):
        """
        Returns the filename
        Args:      None
        Returns:   A string indicating ROOT path.
        """
        file_name = os.path.basename(filepath)
        return file_name

    @staticmethod
    def split_filename_ext(filepath):
        file_name, extension = os.path.splitext(filepath)
        return file_name, extension

    @staticmethod
    def is_abspath( path: str ):
        return os.path.isabs(path)

    @staticmethod
    def get_relpath(target_abs_path: str, base_path: str) -> str:
        """
        Convert absolute-path to relative-path & Return Full-Path.
        :param target_abs_path:
        :param base_path:
        :return:
        """
        return os.path.relpath(target_abs_path, base_path)

    @staticmethod
    def get_abspath(rel_path: str=None) -> str:
        """
        Convert relative-path to absolute-path & Return Full-Path.
        :param rel_path:
        :return:
        """
        return os.path.abspath(rel_path)

    @staticmethod
    def get_rear_path(full_path: str, rear_cnt: int):
        rear_path = ""
        try:
            path = copy.deepcopy(full_path)

            for _ in range(rear_cnt):
                path, tmp = os.path.split(path)
                rear_path = os.path.join(tmp, rear_path)
        except OSError as e:
            logger.error(e)

        return rear_path

    @staticmethod
    def check_exist(path: str, attribute: str):
        result = False
        try:
            if attribute == "file":
                result = os.path.isfile(path)
            elif attribute == "dir":
                result = os.path.isdir(path)
            elif attribute == "link":
                result = os.path.islink(path)
            else:
                logger.warn("Not support attribute.(%s)" % attribute)
        except BaseException as e:
            logger.error(e)

        return result

    @staticmethod
    def classfy_files_dirs(dirpath: str):
        """
        Args:    Directory path.
        Returns: List of all-of-file-path with absolute-path.
        """
        file_list = []
        dir_list = []
        try:
            if CPath.check_exist(dirpath, "dir") is False:
                raise FileNotFoundError(f"Can not find Directory. ({dirpath})")
            
            abs_dirpath = CPath.get_abspath(dirpath)
            
            for name in os.listdir(abs_dirpath):
                full_path = CPath.join_paths(abs_dirpath, name)

                if( CPath.check_exist(full_path, "file") == True ):
                    file_list.append(full_path)
                elif( CPath.check_exist(full_path, "dir") == True ):
                    dir_list.append(name)
                elif( CPath.check_exist(full_path, "link") == True ):
                    file_list.append(full_path)
                else:
                    raise BaseException( "Not supported type.(name={})".format(full_path) )
        except BaseException as e:
            logger.error(e)
            raise e
        
        return file_list, dir_list

    @staticmethod
    def make_dirs( dirpath: str ):
        """
        Create directory & Check it.
        """
        dirpath = CPath.get_abspath(dirpath)
        os.makedirs( dirpath, exist_ok=True )
        if( CPath.check_exist(dirpath, "dir") == False ):
            raise RuntimeError(f"Directory({dirpath}) is not created.")

    @staticmethod
    def send_local_to_linux(src: str, dest_dir: str, send_func):
        '''
        src      : file or dir path in Windows and Linux machine. (Assumption: src path is exist in local-Machine.)
        dest_dir : dir path in Linux only machine. (Assumption: dest path is exist in remote-Machine.)
        send_func: it's called for sending files of src-machine to dest-machine.
        '''
        try:
            if dest_dir is None or src is None or send_func is None:
                raise RuntimeError("Invalid Arguments: dest_dir or src or send_func is None.")
            
            if dest_dir.endswith("/") is False:
                dest_dir += "/"
                
            if not os.path.exists(src):
                raise FileNotFoundError("Cannot find {}".format(src))
            elif os.path.isfile(src):
                src_root = os.path.dirname(src)
                filename = os.path.basename(src)
                
                send_func(src_root, dest_dir, [ filename ])
            elif os.path.isdir(src):
                dirname = os.path.basename(src)

                for src_root, dirs, files in os.walk(src):
                    sub_path = os.path.relpath(src_root, src)
                    dest_root = dest_dir + dirname +"/"
                    if sub_path != '.' and len(sub_path) > 0:
                        dest_root = dest_root + sub_path + "/"

                    send_func(src_root, dest_root, files)
        except BaseException as e:
            logger.error(e)
            raise e
