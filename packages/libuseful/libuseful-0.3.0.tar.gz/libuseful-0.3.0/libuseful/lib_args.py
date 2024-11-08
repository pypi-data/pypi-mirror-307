############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import os
import sys
import argparse
from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)


class CArgParserCommon(object):
    __inst__ = None
    __arg_info__ = None

    def __init__(self, name: str, desc: str="No Description.", sign_log: str="No Sign"):
        self.__inst__ = argparse.ArgumentParser(prog=name, description=desc, epilog=sign_log)
        self.__arg_info__ = None

    def get_parser_instance(self):
        return self.__inst__

    def get_info_handler(self):
        return self.__arg_info__

    def extract_arg_info(self):
        try:
            self.__arg_info__ = self.__inst__.parse_args()
            self.post_proc_of_parse(self.__arg_info__)
        except SystemExit as e:
            raise e
        except BaseException as e:
            logger.error("extracting argument is failed. : " + str(e))
            raise e

        return self.__arg_info__

    def get_arg_info(self, item_name):
        """
            It's Virtual member function for un-definition.
        :param item_name:
        :return:
        """
        raise NotImplementedError

    def post_proc_of_parse(self, arg_info):
        """
            It's Virtual member function for un-definition.
        :param arg_info: parsed arguments info-list.
        :return: None
        """
        pass


class CHargs(object):
    __cmd__ = None
    __arg_leng__ = None
    __arg_parser__ = None

    def __init__(self, class_inst: CArgParserCommon):
        self.__cmd__ = os.path.basename(sys.argv[0])
        self.__arg_leng__ = len(sys.argv) - 1
        try:
            if class_inst is None:
                raise BaseException

            self.__arg_parser__ = class_inst
            self.__arg_parser__.extract_arg_info()
        except SystemExit as e:
            raise e
        except BaseException as e:
            logger.error("extracting argument-info is failed. : " + str(e))
            raise e

    def get_cmd(self):
        return self.__cmd__

    def get_arg_leng(self):
        return self.__arg_leng__

    def get_arg_data(self, item_name):
        return self.__arg_parser__.get_arg_info(item_name=item_name)
