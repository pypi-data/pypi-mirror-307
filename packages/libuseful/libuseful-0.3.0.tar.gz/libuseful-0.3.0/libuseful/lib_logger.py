############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import os
import signal
import inspect
import platform
from . import lib_time as ltime
from .lib_watchdog import IWatchDog
from .lib_enum import ENUM_STR as myEnum

__all__ = ["CmyLogger", "get_instance", "assertMy", "WTD_logSignal"]

_PROJECT_ = None


class WTD_logSignal(IWatchDog):
    SIGNAL_ID = None
    SIGNAL_LISTEN_ID = {
        # SEND-ID : LISTEN-ID
        signal.SIGINT: signal.SIGINT,                 #  2 [Lin] execute listen-handler.     [zero-PID]    [KeyboardInterrupt] [immediatly INT-happend]
        signal.SIGTERM: signal.SIGTERM                # 15 [Lin] execute listen-handler.     [No zero-PID] [Exit Program]      [immediatly INT-happend]
                                                      # 15 [WIN] Not execute listen-handler. [No zero-PID] [Exit Program]      [immediatly INT-happend]
        # signal.SIGBREAK: signal.SIGBREAK            # 21 [WIN] Not execute listen-handler. [No zero-PID] [Exit Program]      [immediatly INT-happend]
        # signal.CTRL_C_EVENT: signal.SIGINT          #  0 [WIN] execute listen-handler.     [zero-PID]    [KeyboardInterrupt] [when waiting input/response, pending interrupt]
        # signal.CTRL_BREAK_EVENT: signal.SIGBREAK    #  1 [WIN] Not execute listen-handler. [zero-PID]    [Can not Use it]    [when waiting input/response, NOT Reacted]
    }
    _os_name_: str = None
    
    def start(self, sig_handler=None):
        def keyboardINT_handler(signum, issue_path):
            try:
                sig_handler(self._os_name_, signum, issue_path)
                
                if self._os_name_ == "Linux":
                    raise KeyboardInterrupt(signum, issue_path)
            except KeyboardInterrupt as e:
                raise e
            except BaseException as e:
                print(f"[E][WTD_logSignal] keyboardINT_handler: {e}\n")
                raise e
        
        try:
            # If need, then register sig_handler to handle processing when the signal happened.
            listen_id = self.SIGNAL_LISTEN_ID.get(self.SIGNAL_ID, None)
            if sig_handler is not None and listen_id is not None:
                print(f"[I][WTD_logSignal] start: register handler for Signal_ID. ({self.SIGNAL_ID})\n")
                signal.signal(listen_id, keyboardINT_handler)
            
            # start WatchDog-Timer's Thread.
            super().start()
        except BaseException as e:
            print(f"[E][WTD_logSignal] start: {e}\n")
            raise e
        
    def __init__(self):
        try:
            self._os_name_ = platform.system()
            
            # set variables
            if self._os_name_ == "Linux":
                self.SIGNAL_ID = signal.SIGINT      # Valid-values : SIGINT , SIGTERM
            elif self._os_name_ == "Windows":
                self.SIGNAL_LISTEN_ID.update({signal.CTRL_C_EVENT: signal.SIGINT})
                self.SIGNAL_LISTEN_ID.update({signal.SIGBREAK: None})
                self.SIGNAL_LISTEN_ID.pop(signal.SIGINT)
                self.SIGNAL_ID = signal.SIGBREAK    # Valid-values : SIGBREAK , SIGTERM
            else:
                raise RuntimeError(f"Not Supported OS-Type. ({self._os_name_})")

            # check 'SIGNAL_ID' validation.
            if self.SIGNAL_ID not in list(self.SIGNAL_LISTEN_ID.keys()):
                raise RuntimeError(f"'signal'({self.SIGNAL_ID}) is not supported yet.")
                
            # call default-constructor
            super().__init__(enable=False, limited_sec=900)     # Trig after 15 minute from last command.
        except BaseException as e:
            print(f"[E][WTD_logSignal] __init__: {e}\n")
            raise e
        
    def _work_(self):   # conditional send signal. (KeyboardInterrupt)
        '''
            User-Defined Function.
            thread-unsafety function. (need external Lock)
            
            Description: It send signal(KeyboardInterrupt) to self-process's PID.
        '''
        try:
            _m_pid_ = os.getpid()
            print(f"[I][WTD_logSignal] _send_signal_linux_: send signal({self.SIGNAL_ID}) to Self-PID.({_m_pid_})\n")
            os.kill(_m_pid_, self.SIGNAL_ID) # send SIGNAL_ID to Self-PID.
        except BaseException as e:
            print(f"[E][WTD_logSignal] _work_: {e}\n")
            raise e


class CmyLogger(object):
    # Value-List for Mode.(_mode_)
    DEBUG_MODE = myEnum("DEBUG")
    RELEASE_MODE = myEnum("RELEASE")

    # Value-List for Log-Level.
    DEBUG_LEVEL = myEnum("DEBUG")
    INFO_LEVEL = myEnum("INFO")
    WARN_LEVEL = myEnum("WARN")
    ERROR_LEVEL = myEnum("ERROR")
    NONE_LEVEL = myEnum("NONE")

    _mode_ = RELEASE_MODE
    _level_ = 1

    def set_project(prj: str):
        try:
            if _PROJECT_ is None and prj is not None:
                if isinstance(prj, str) is True and len(prj) > 0:
                    _PROJECT_ = prj
        except BaseException as e:
            print("[ERROR][{}][{}]: {}".format(_PROJECT_, ltime.TIME(), e))
    
    def stop(self):
        try:
            WTD_logSignal.get_instance().__del__()
        except BaseException as e:
            print("[ERROR][{}][{}]: {}".format(_PROJECT_, ltime.TIME(), e))

    def __init__(self, level: myEnum = INFO_LEVEL, mode: myEnum = RELEASE_MODE):
        global _logger_
        if _logger_ is None:
            _logger_ = self
            self.__set_mode__(mode)
            self.__set_level__(level)

    def __get_frameInfo__(self, func_deepth: int=0):
        classname = None
        raw_func_deepth = 2 + func_deepth
        callerframerecord = inspect.stack()[raw_func_deepth]  # 0 represents this line
                                                              # 1 represents line at caller
        frame = callerframerecord[0]
        try:
            classname = frame.f_locals["self"].__class__.__name__
        except KeyError:
            pass
        info = inspect.getframeinfo(frame)
        # print("classname: ", classname)  # Class Name.
        # print("filename: ", os.path.basename(info.filename) )  # __FILE__     -> Test.py
        # print("funcname: ", info.function )  # __FUNCTION__ -> Main
        # print("linenum : ", info.lineno )    # __LINE__     -> 13
        return os.path.basename(info.filename), classname, info.function, info.lineno

    def __level_int_to_str__(self, level: int) -> myEnum:
        str_level = self.NONE_LEVEL
        if level == 0:
            str_level = self.ERROR_LEVEL
        elif level == 1:
            str_level = self.WARN_LEVEL
        elif level == 2:
            str_level = self.INFO_LEVEL
        elif level == 3:
            str_level = self.DEBUG_LEVEL

        return str_level

    def __level_str_to_int__(self, level: myEnum) -> int:
        ret_val = 0
        if level == self.ERROR_LEVEL:
            ret_val = 0
        elif level == self.WARN_LEVEL:
            ret_val = 1
        elif level == self.INFO_LEVEL:
            ret_val = 2
        elif level == self.DEBUG_LEVEL:
            ret_val = 3

        return ret_val

    def __set_mode__(self, mode: myEnum):
        try:
            if mode is self.DEBUG_MODE or mode is self.RELEASE_MODE:
                self._mode_ = mode
            else:
                raise BaseException("Not Supported mode.(%s)" % mode.__str__())
        except BaseException as e:
            self.error(str(e))

    def __set_level__(self, level: myEnum):
        if self._mode_ is self.DEBUG_MODE:
            self._level_ = self.__level_str_to_int__(level=level)
        elif self._mode_ is self.RELEASE_MODE:
            self._level_ = self.__level_str_to_int__(level=level)

    def __get_level__(self) -> myEnum:
        if self._mode_ is self.DEBUG_MODE:
            return self.__level_int_to_str__(self._level_)
        elif self._mode_ is self.RELEASE_MODE:
            return self.__level_int_to_str__(self._level_)

    def get_level(self) -> str:
        return self.__get_level__.__str__()

    def error(self, *args, **kwargs):
        if self._mode_ is self.DEBUG_MODE:
            filename, classname, funcname, linenum = self.__get_frameInfo__()
            print("[ERROR][{}][{}] {}<{}.{}:{}>: {}:{}".format(_PROJECT_, ltime.TIME(), filename, classname, funcname, linenum, args, kwargs))
            WTD_logSignal.get_instance().reset()
        elif self._mode_ is self.RELEASE_MODE:
            print("[ERROR][{}][{}]: {}:{}".format(_PROJECT_, ltime.TIME(), args[0], kwargs))
            WTD_logSignal.get_instance().reset()

    def warn(self, *args, **kwargs):
        if self._level_ >= 1:
            if self._mode_ is self.DEBUG_MODE:
                filename, classname, funcname, linenum = self.__get_frameInfo__()
                print("[WARN][{}][{}] {}<{}.{}:{}>: {}:{}".format(_PROJECT_, ltime.TIME(), filename, classname, funcname, linenum, args, kwargs))
                WTD_logSignal.get_instance().reset()
            elif self._mode_ is self.RELEASE_MODE:
                print("[WARN][{}]: {}:{}".format(_PROJECT_, args[0], kwargs))
                WTD_logSignal.get_instance().reset()

    def info(self, *args, **kwargs):
        if self._level_ >= 2:
            if self._mode_ is self.DEBUG_MODE:
                filename, classname, funcname, linenum = self.__get_frameInfo__()
                print("[INFO][{}] {}<{}.{}:{}>: {}:{}".format(_PROJECT_, filename, classname, funcname, linenum, args, kwargs) )
                WTD_logSignal.get_instance().reset()
            elif self._mode_ is self.RELEASE_MODE:
                print("[INFO][{}]: {}:{}".format(_PROJECT_, args[0], kwargs))
                WTD_logSignal.get_instance().reset()

    def debug(self, *args, **kwargs):
        if self._level_ >= 3:
            if self._mode_ is self.DEBUG_MODE:
                filename, classname, funcname, linenum = self.__get_frameInfo__()
                print("[DEBUG][{}] {}<{}.{}:{}>: {}:{}".format(_PROJECT_, filename, classname, funcname, linenum, args, kwargs))
                WTD_logSignal.get_instance().reset()
            elif self._mode_ is self.RELEASE_MODE:
                print("[DEBUG][{}]: {}:{}".format(_PROJECT_, args[0], kwargs))
                WTD_logSignal.get_instance().reset()


def get_instance(level_of_file: myEnum=None, mode: myEnum=None) -> CmyLogger:
    global _logger_
    try:
        instance = _logger_
    except NameError:
        _logger_ = None
        instance = CmyLogger()

    if instance is not None:
        if mode is not None:
            instance.__set_mode__(mode)
        if level_of_file is not None:
            instance.__set_level__(level=level_of_file)

    return instance


def assertMy( func, except_type, msg: str="", debug_msg: str=None ):
    if (func) == False:
        if debug_msg is not None:
            logger = get_instance()
            logger.debug(debug_msg)

        raise except_type(msg)


