############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import time
import threading
import copy as cp
from datetime import datetime
from typing import Dict, Callable, Any

# import logging
from . import lib_logger as myLogger
from .lib_logger import *

logging = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)


__all__ = [ "UserManager", "get_UTC", "str_UTC" ]


def get_UTC():
    try:
        now = datetime.now()
        return now.timestamp()
    except BaseException as e:
        logging.error(e)
        raise e

def str_UTC( utc: float ):
    try:
        if utc <= 0.0:
            return None
        
        d = datetime.fromtimestamp( utc, tz=None )
        return d.strftime( "%Y-%m-%d %H:%M:%S" )
    except BaseException as e:
        logging.error(e)
        raise e


class UserManager( object ):
    '''
        > [ _mm_users_ format ]
            {
                user_id : {
                    timestamp: float,                                       # timestamp that is received last-ping
                    svc_name_01 : {state: bool, unsub_func: callable},      # true : registered subscribe
                    svc_name_02 : {state: bool, unsub_func: callable},      # false: unregistered subscribe
                    svc_name_03 : {state: bool, unsub_func: callable}
                }
            }
        
        > [ Usage-Guide ]
            - Client 등록/해제 : Server는 keep-alive 를 통해서, uid를 등록 & 해제 시킨다.
                                (해제시, unsub_func를 호출하고, stat를 False로 만든다.)
            - Service 등록/해제: Server는 subscribe를 통해서, service 등록 & unsubscribe로 해제 시킨다.
            - REQ/RESP 허용    : Server는 uid가 등록된 경우, "허용"
            - PUB/SUB 허용     : Server는 uid가 등록된 경우이면서, service가 등록되지 않았다면 Subscribe를 "허용"
            - STREAM 허용      : Server는 uid와 service가 등록된 경우, "허용"
            - Attention
                * Service당 subscribe는 오직 1개만 존재해야 한다.
                * Server에서, subscribe 함수를 허용하면, subscribe 함수를 통해서, Client로 Publish를 할수 있다.
    '''
    class CValue(object):
        state: bool = False
        unsub_func: Callable[[str],Any] = None
        
        def __init__(self, state: bool, unsub_func: Callable[[str],Any]):
            self.state = state
            self.unsub_func = unsub_func
        
        def __call__(self, state: bool, unsub_func: Callable[[str],Any]):
            self.state = state
            self.unsub_func = unsub_func
            
        def __del__(self):
            self.state = False
            self.unsub_func = None
    
    class State:
        INSERTED="inserted"
        DUPLICATED="duplicated"
        OVERFLOW="overflow-max-users"
        NOT_ALLOWED_USER="not-allowed-user"

    DEF_MAX_USERS: int = 5
    TIMESTAMP: str = "_timestamp_"

    _m_max_users_: int = 0
    _mm_users_: Dict[str, CValue] = None           # key: user_id , value: SVC-stat (dict)
    _mtx_users_: threading.Lock = threading.Lock()


    @property
    def uid_list(self):
        with self._mtx_users_:
            if self._m_max_users_ <= 0:
                return list()
            return cp.deepcopy( list(self._mm_users_.keys()) )
        
    def get_service_list(self, user_id: str):
        try:
            if user_id is None:
                raise RuntimeError("user_id is None.")
            
            svcs: dict = self._mm_users_.get(user_id, None)
            if svcs is None:
                return None
            
            return list( svcs.keys() )
        except BaseException as e:
            logging.error(e)
            raise e

    def __init__(self, max_users: int=DEF_MAX_USERS):
        try:
            if max_users < 1:
                raise RuntimeError(f"'max_users' is under the min-user cnt. ({max_users})")
            
            self._m_max_users_ = max_users
            self._mm_users_ = dict()
        except BaseException as e:
            logging.error(e)
            raise e

    def __del__(self):
        try:
            # waiting service-done
            self.join( timeout=5.0 )

            # if exist service, then force call unsubscribe-function
            for uid in self.uid_list:
                self.unreg_user( uid )
                
            # clear data-structure
            with self._mtx_users_:
                self._m_max_users_ = 0
                self._mm_users_.clear()
        except BaseException as e:
            logging.error(e)
            raise e

    def join(self, timeout: float=0.0):
        try:
            cnt = timeout
            while len(self._mm_users_) > 0 and (timeout <= 0.0 or cnt > 0.0):
                time.sleep(1.0) 
                if cnt > 0.0:
                    cnt -= 1.0
        except BaseException as e:
            logging.error(e)
            raise e

    def reg_user(self, user_id: str) -> State:
        STATE = UserManager.State
        try:
            if user_id is None:
                raise RuntimeError(f"'user_id' is None. ({user_id})")
            
            with self._mtx_users_:
                if self._mm_users_.get(user_id, None) is not None:
                    return STATE.DUPLICATED
                
                if len(self._mm_users_) >= self._m_max_users_:
                    return STATE.OVERFLOW      # Capacity of User was already overflowed.

                self._mm_users_.update({user_id: {self.TIMESTAMP: get_UTC()}})
                logging.info(f"*> User({user_id}) is registered.")
                return STATE.INSERTED
        except BaseException as e:
            logging.error(e)
            raise e

    def unreg_user(self, user_id: str):
        try:
            func_list: list = list()
            if user_id is None:
                raise RuntimeError(f"'user_id' is None. ({user_id})")
            
            with self._mtx_users_:
                user: dict = self._mm_users_.get(user_id, None)
                if user is None:
                    return 
                
                context: UserManager.CValue = None
                for svc, context in user.items():
                    if svc == self.TIMESTAMP:
                        continue

                    if context.state is True:
                        context.state = False
                        func_list.append( context.unsub_func )
                
                self._mm_users_.pop(user_id)
                logging.info(f"*> User({user_id}) is unregistered.")
        
            for func in func_list:
                if func is not None:
                    func( user_id )              # call unsubscribe-function
        except BaseException as e:
            logging.error(e)
            raise e

    def reg_service(self, user_id: str, svc_name: str, func: Callable[[str],Any]) -> State:
        STATE = UserManager.State
        try:
            if user_id is None or svc_name is None or func is None:
                raise RuntimeError(f"user_id/service_name/func is None. ({user_id}/{svc_name}/{func})")

            if svc_name in [ self.TIMESTAMP ]:
                raise RuntimeError(f"'svc_name' is not support as {self.TIMESTAMP}")

            with self._mtx_users_:
                if self.is_available_user(user_id) is False:
                    return STATE.NOT_ALLOWED_USER
                
                user: dict = self._mm_users_.get(user_id)
                if user.get(svc_name, None) is not None and user.get(svc_name).state is True:
                    return STATE.DUPLICATED    # Already, user-id was inserted to system.

                user.update({svc_name: UserManager.CValue(state=True, unsub_func=func)})
                return STATE.INSERTED
        except BaseException as e:
            logging.error(e)
            raise e

    def unreg_service(self, user_id: str, svc_name: str, force: bool=False):
        try:
            context: UserManager.CValue = None
            if user_id is None or svc_name is None:
                raise RuntimeError(f"user_id/service_name is None. ({user_id}/{svc_name})")

            if svc_name in [ self.TIMESTAMP ]:
                raise RuntimeError(f"'svc_name' is not support as {self.TIMESTAMP}")

            with self._mtx_users_:
                if self.is_available_user(user_id) is False:
                    return
                
                user: dict = self._mm_users_.get(user_id)
                if user.get(svc_name, None) is None:
                    return
                
                context = user.pop(svc_name)
            
            if context is not None and force is True:
                if context.state is True and context.unsub_func is not None:
                    context.state = False
                    context.unsub_func( user_id )              # call unsubscribe-function
        except BaseException as e:
            logging.error(e)
            raise e

    def is_available_user(self, user_id: str):
        try:
            if user_id is None:
                raise RuntimeError(f"'user_id'({user_id}) is None.")
            
            res = self._mm_users_.get(user_id, False)
            return False if res is False else True
        except BaseException as e:
            logging.error(e)
            raise e

    def is_available(self, user_id: str, svc_name: str) -> bool:
        try:
            if svc_name is None:
                raise RuntimeError(f"'svc_name'({svc_name}) is None.")
            
            if svc_name in [ self.TIMESTAMP ]:
                raise RuntimeError(f"'svc_name' is not support as {self.TIMESTAMP}")

            if self.is_available_user(user_id) is False:
                return False
            
            context: UserManager.CValue = self._mm_users_.get(user_id).get(svc_name, None)
            if context is None:
                return False
            return context.state
        except BaseException as e:
            logging.error(e)
            raise e

    def set_state(self, user_id: str, svc_name: str, stat: bool) -> bool:
        try:
            context: UserManager.CValue = None
            pre_state: bool = None
            
            if svc_name in [ self.TIMESTAMP ]:
                raise RuntimeError(f"'svc_name' is not support as {self.TIMESTAMP}")

            with self._mtx_users_:
                user: dict = self._mm_users_.get(user_id, None)
                if user is None:
                    return False
                
                context: UserManager.CValue = user.get(svc_name, None)
                if context is None:
                    return False

                pre_state = context.state
                context.state = stat
            
            if pre_state is True and stat is False and context.unsub_func is not None:
                context.unsub_func( user_id )            # call unsubscribe-function
            return True
        except BaseException as e:
            logging.error(e)
            raise e

    def get_timestamp(self, user_id: str):
        try:
            with self._mtx_users_:
                if self.is_available_user( user_id ) is False:
                    return None
                return self._mm_users_.get(user_id).get(self.TIMESTAMP)
        except BaseException as e:
            logging.error(e)
            raise e

    def update_timestamp(self, user_id: str):
        try:
            with self._mtx_users_:
                if self.is_available_user( user_id ) is False:
                    return False
                
                self._mm_users_.get(user_id).update({self.TIMESTAMP: get_UTC()})
                return True
        except BaseException as e:
            logging.error(e)
            raise e