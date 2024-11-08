############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import sys
import types
from . import lib_path as lpath

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(mode=CmyLogger.DEBUG_MODE)



def import_module(absolute_path: str):
    try:
        if absolute_path is None:
            raise RuntimeError("absolute_path is NULL.")
        
        # check validation.
        dir = lpath.get_dirpath( absolute_path )
        file = lpath.get_filename( absolute_path )
        file, ext = lpath.split_filename_ext( file )
        if ext != ".py":
            raise RuntimeError("import_module function is only support '*.py' source file case.")
        
        # append new PYTHONPATH to system.
        if dir not in sys.path:
            sys.path.append(dir)
            
        # import file as a module, dynamically.
        return __import__(file, fromlist=[file])
    except BaseException as e:
        logger.error(e)
        raise e

def import_class( module: types.ModuleType, class_name: str ):
    try:
        if module is None or class_name is None:
            raise RuntimeError(f"module({module}) or class_name({class_name}) is NULL.")
        
        _class_ = getattr( module, class_name )
        if _class_ is None:
            raise RuntimeError(f"Can not find class({class_name}) in module.({module})")
        return _class_
    except BaseException as e:
        logger.error(e)
        raise e

def get_path_class( data: dict ):
    try:
        if data is None:
            raise RuntimeError("'data' is NULL.")
        
        _path_ = data.get("path", None)
        _class_ = data.get("class", None)
        
        if _path_ is None or _class_ is None:
            raise RuntimeError("Can not find mandatory key('path', 'class').")
        
        return _path_, _class_
    except BaseException as e:
        logger.error(e)
        raise e

def get_class_reference(data: dict, local_root: str):
    try:
        # get values of 'path' & 'class'
        _path_, _class_name_ = get_path_class( data )
        
        # make absolute path.
        if lpath.is_abspath( _path_ ) is False:
            _path_ = lpath.join_paths( local_root, _path_ )
        
        print()
        logger.info("------- Import Class -------")
        logger.info(f"- path : {_path_}")
        logger.info(f"- class: {_class_name_}")
        logger.info("----------------------------")
        print()        

        # get class object from python source-file.
        module = import_module( lpath.get_abspath(_path_) )
        return import_class( module, _class_name_ )
    
    except BaseException as e:
        logger.error(e)
        raise e
