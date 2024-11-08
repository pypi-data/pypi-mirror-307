############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import time
import threading
from abc import *
from .lib_thread import CThread
from .lib_singleton import Singleton


class IWatchDog(Singleton, metaclass=ABCMeta):
    DEF_MAX_SEC: int = 900     # default max-time : 15 minute
    
    _m_thread_: CThread = None
    _m_locker_: threading.Lock = threading.Lock()       # for _m_time_ variables
    _m_time_max_: int = 0       # unit : SEC
    _m_time_: int = 0           # unit : SEC

    
    def is_activated(self):
        return True if self._m_thread_ is not None else False
    
    def start(self):
        try:
            # create thread, if need.
            if self._m_thread_ is None:
                self._create_thread_()

            # init variables
            self.reset()

            # start thread
            self._m_thread_.start()
        except BaseException as e:
            print(f"[E][WTD] start: {e}\n")
            raise e
        
    def stop(self):
        try:
            self._destroy_thread_()
        except BaseException as e:
            print(f"[E][WTD] stop: {e}\n")
            raise e
        
    def reset(self):        # thread-safety function
        try:
            if self._m_thread_ is None:
                return
            
            with self._m_locker_:
                self._m_time_ = self._m_time_max_        # reset watch-dog timer.
                self._reset_hook_()
                # print(f"[D][WTD] reset: Called reset function. (time={self._m_time_})\n")
                
        except BaseException as e:
            print(f"[E][WTD] reset: {e}\n")
            raise e


    #############################################
    # Private Function Definition.
    ############
    def __init__(self, enable: bool=True, limited_sec: int=DEF_MAX_SEC):
        # print("[D][WTD] __init__: Entered.\n")
        try:
            self.__clean__()
            
            # set WatchDog dead-line time.
            self._m_time_max_ = limited_sec
            if self._m_time_max_ <= 0:
                raise RuntimeError(f"WATCH_DOG_MAX_SEC <= 0, It's invalid. ({limited_sec})")
            
            # trig WatchDog timer.
            if enable is True:
                self.start()
        except BaseException as e:
            print(f"[E][WTD] __init__: {e}\n")
            raise e
    
    def __del__(self):
        # print("[D][WTD] __del__: Entered.\n")
        self.stop()
        self.__clean__()
    
    def __clean__(self):
        self._m_time_max_ = 0
        self._m_time_ = 0

    
    ####################################
    # Thread related Private-Functions.
    ######
    def _create_thread_(self):
        try:
            if self._m_thread_ is not None:
                raise RuntimeError("Already, WatchDog Thread is created.")
            
            self._m_thread_ = CThread("WatchDog-thread", self._routine_thread_, daemon=True)
        except BaseException as e:
            print(f"[E][WTD] _create_thread_: {e}\n")
            raise e

    def _destroy_thread_(self):
        try:
            if self._m_thread_ is None or self._m_thread_.is_continue is not True:
                return 
            
            if self._m_thread_.is_alive() is True:
                print("[I][WTD] _destroy_thread_: Try to destory WatchDog-thread.\n")
                self._m_thread_.is_continue = False
                self._m_thread_.join(timeout=3.0)      # Blocking Function
                
            del self._m_thread_
            self._m_thread_ = None
        except BaseException as e:
            print(f"[E][WTD] _destroy_thread_: {e}\n")
            raise e

    def _routine_thread_(self, thr_inst: CThread):
        def run_algorithm():
            try:
                with self._m_locker_:
                    self._m_time_ -= 1
                    # print(f"[D][WTD] run_algorithm: time = ({self._m_time_}/{self._m_time_max_})\n")
                    
                    if self._m_time_ <= 0:
                        self._m_time_ = self._m_time_max_
                        self._work_()        # Do User-Defined function.

                time.sleep(1.0)
            except BaseException as e:
                print(f"[E][WTD] run_algorithm: {e}\n")
                raise e
        
        try:
            print( "[I][WTD] _routine_thread_: Start Thread: {}\n".format(thr_inst.getName()) )

            # Thread Main-routine.
            while( thr_inst.is_continue ):
                try:
                    # print("[D][WTD] _routine_thread_: Thread Running ...")
                    run_algorithm()
                    
                except BaseException as e:
                    print(f"[E][WTD] _routine_thread_: {e}\n")
                    # raise e
                
            # Terminate thread.
            thr_inst.is_continue = False
            
        except BaseException as e:
            print(f"[E][WTD] _routine_thread_: {e}\n")
            
        print("[I][WTD] _routine_thread_: Destroyed WatchDog-Thread.\n")
        return 0;
    
    def _work_(self):        # thread-unsafety function: need external Lock.
        '''
            User-Defined Function.
            thread-unsafety function. (need external Lock)
            
            Description: This function is triged when WatchDog-Timer is expired.
                         After This function, The WatchDog-Timer is reset.
        '''
        print("[E][WTD] _work_: Not implemented yet.\n")
        raise NotImplementedError("[WTD] Not implemented yet.")

    def _reset_hook_(self):
        '''
            Hooking-Function of 'reset' API.
            It's Optional User-Defined Function.
        '''
        pass
