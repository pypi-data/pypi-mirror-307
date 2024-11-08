############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import numpy as np
from . import lib_shell as lshell
from .lib_singleton import *

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)

__all__ = ["CFatalErr"]


class CFatalErr(Singleton):
    class KEY:
        ID = "id"
        TYPE = "type"
        MODE = "mode"
        PC_STAMP = "timestamp-PC"
        MSG = "msg"
        
    class TYPE:
        NONE = "none"
        ADB = "adb"
        
    class MODE:
        BROKEN = "broken"
        INFINITE_WAIT = "infinite_wait"
        OFFLINE = "offline"
    
    _mm_fatal_ = {}
    _mm_ids_ = {}

    #--- Public Functions----------------------
    def get_infos(self, type: TYPE=TYPE.NONE) -> dict:
        try:
            if type != self.TYPE.NONE:
                return {type: self._mm_fatal_.get(type, [])}
            return self._mm_fatal_
        except BaseException as e:
            logger.error(e)
            raise e
        
    def get_info(self, id: str) -> dict:
        return self._mm_ids_.get(id, None)
        
    def set_info(self, type: TYPE, mode: MODE, err: str) -> str:
        Key = CFatalErr.KEY
        
        try:
            id = str(np.random.randint(low=0, high=0x7FFFFFFF))
            tstamp = lshell.local_date()
            info = {Key.PC_STAMP: tstamp, 
                    Key.ID: id, 
                    Key.TYPE: type, 
                    Key.MODE: mode,
                    Key.MSG: err}
            
            # create empty list.
            info_list: list = self._mm_fatal_.get(type, None)
            if info_list is None:
                self._mm_fatal_.update({type: []})
                info_list = self._mm_fatal_.get(type, None)
            
            # update infomation.
            info_list.append(info)
            self._mm_ids_.update({id: info})
            return id
        except BaseException as e:
            logger.error(e)
            raise e
        
    #--- Private Functions-----------------------
    def __init__(self) -> None:
        super().__init__()
    
    def __del__(self):
        self._mm_fatal_ = {}
