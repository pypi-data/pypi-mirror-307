############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import os
import json
import locale
from .exception import CENullException
from . import lib_path as lpath
from collections import OrderedDict
from typing import List
import chardet

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)

# binary type CR, LF description
LINE_ENDING_WINDOW = b'\r\n'
LINE_ENDING_LINUX  = b'\n'

CODEC: str = locale.getpreferredencoding(True)

def append_text( text: str, contents: str ) -> str:
    try:
        if( contents is None ):
            contents = ""
            
        if( text.find(LINE_ENDING_WINDOW) != -1 ):
            text.replace(LINE_ENDING_WINDOW, LINE_ENDING_LINUX)
        elif( text.find(LINE_ENDING_LINUX) == -1 ):
            text = text + LINE_ENDING_LINUX
        return contents + text
    except BaseException as e:
        logger.error(e)
        raise e


def create_text_file( file_path: str, contents: str ):
    try:
        file_path = lpath.get_abspath(file_path)
        dir_path = lpath.get_dirpath(file_path)

        lpath.make_dirs( dir_path )
        
        # make 'UTF-8' type binary byte-data.
        contents = bytes( contents, 'utf-8' )
        contents = contents.replace(LINE_ENDING_WINDOW, LINE_ENDING_LINUX)

        # make 'UTF-8' type text file.
        with open(file_path, "wb") as fp:
            fp.write( contents )
    except BaseException as e:
        logger.error(e)
        raise e


def create_json_file( file_path: str, data: dict ):
    try:
        if file_path is None or data is None:
            raise BaseException(f"file_path({file_path}) or data{data} is None.\nInsert value.")
        
        file_path = lpath.get_abspath(file_path)
        dir_path = lpath.get_dirpath(file_path)

        lpath.make_dirs( dir_path )
        
        with open(file_path, "w") as fp:
            json.dump(data, fp, sort_keys=True, indent=4)
    except BaseException as e:
        logger.error(e)
        raise e

def delete_file( file_path: str ):
    try:
        if file_path is None:
            raise BaseException(f"file_path({file_path}) is None.")
        
        file_path = lpath.get_abspath(file_path)
        if lpath.check_exist(file_path, 'file') is False:
            logger.warn(f"file_path({file_path}) is not exist.")
            return
        
        os.remove(file_path)
    except BaseException as e:
        logger.error(e)
        raise e

def read_text_file( file_path: str, encoder: str = CODEC ) -> List[str]:
    
    def read_file( full_path: str, encoding: str, ignore:bool = False):
        with open( full_path, mode="r", encoding=encoding, errors='ignore' if ignore is True else None ) as fd:
            return fd.readlines()
    try:
        if file_path is None:
            raise BaseException("file_path is None. Insert file_path.")

        return read_file(file_path, encoding=encoder)
        
    except UnicodeDecodeError as e:
        with open( file_path, mode='rb') as raw:
            property = chardet.detect(raw.read(10000)).get("encoding", None)
            encoder = property if property is not None and property != encoder else encoder

        return read_file(file_path, encoding=encoder, ignore=True)
    except FileNotFoundError as e:
        logger.warn(f"Return None. Because, {e}")
        return None
    except BaseException as e:
        logger.error(f"{e}: ({file_path})")
        raise e

def read_json_file( file_path: str, with_annotation: bool=False ) -> dict:
    try:
        if file_path is None:
            raise BaseException("file_path is None. Insert file_path.")
        
        if with_annotation is False:
            with open(file_path, mode="r") as fd:
                return json.load(fd, object_pairs_hook=OrderedDict)
        else:
            with open(file_path, mode="r", encoding='utf-8-sig') as fd:
                contents = fd.read()
                return read_json( contents=contents, with_annotation=True)
    
    except FileNotFoundError as e:
        logger.error(e)
        return None
    except BaseException as e:
        logger.error(e)
    
    return None


def read_json( contents: str, with_annotation: bool=False, replace_str_indicator=False ) -> dict:
    try:
        if contents is None:
            return None
        
        contents = contents.strip()
        if len(contents) == 0:
            return None
        
        if with_annotation is True:
            while "/*" in contents:
                preComment, postComment = contents.split('/*', 1)
                contents = preComment + postComment.split('*/', 1)[1]

        if replace_str_indicator is True:
            contents = contents.replace("'", '"')
            
        return json.loads(contents)
    except json.JSONDecodeError as e:
        logger.error(e)
        raise e
    except BaseException as e:
        logger.error(e)
        raise e

def write_string( contents: dict ):
    try:
        if contents is None:
            raise CENullException("contents is NULL.")
        
        return json.dumps( contents, sort_keys=True, indent=4 )
    except BaseException as e:
        logger.error(e)
        raise e

def copy_json_file( src_path: str, dest_path: str, with_annotation: bool=False ):
    try:
        if src_path is None or dest_path is None:
            raise BaseException(f"src_path({src_path}) or dest_path({dest_path}) is None.")
        
        logger.info(f"src={src_path}, dest={dest_path}")
        contents = read_json_file(src_path, with_annotation=with_annotation)
        if contents is None:
            raise BaseException("contents is NULL.")
        
        create_json_file( dest_path, contents )
    except BaseException as e:
        logger.error(e)
        raise e
