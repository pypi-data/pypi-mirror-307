############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
#   Created-Date: 2024.08.13
#   Updated-Date: 2024.08.17
#   Attention: Recommended Version is greater than python-3.8.
#
#   Reference:
#       - https://docs.python.org/ko/3.8/library/asyncio-task.html
#       - https://ks1171-park.tistory.com/81
#       - https://ks1171-park.tistory.com/82
#
#  Fundamental Principle:
'''
    1. Event-Loop의 instance를 얻는다. (이미 있는걸 찾고, 없다면 생성한다.)
        loop = asyncio.get_event_loop
        
    2. 실행을 원하는 coroutine(async def func() 형식)를 Task로 만들어서 Event-Loop에 등록한다. 
        task = loop.create_task( coroutine )
        
    3. 각 Task들의 종료를 기다리는 await를 호출한다.
        async def wait_return_completed():    
            result = await asyncio.gather(*[task], return_exceptions=True)
                                or
            result = await task
        
        loop.create_task(wait_return_completed(), name="wait-coroutine.")

    4. Event-Loop을 실행시킨다.
        loop.run_forever()              : loop.stop()을 할때까지 영원히 Event-Loop를 실행시킨다.
        loop.run_until_complete(task)   : task가 종료할때까지, Event-Loop를 실행시킨다.
                                          Other-task가 등록되었어도, Event-Loop를 종료하게 된다.
'''
###########################################################################

import copy
import sys
assert (sys.version_info.major * 10 + sys.version_info.minor) >= 38, "Use Python 3.8 or Upper-Version"

import time
import asyncio
import threading

import functools
import contextvars
from typing import Callable, List

# import logging
from . import lib_logger as myLogger
from .lib_logger import *

logging = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)

__all__=["CAsyncLoop"]


class CAsyncLoop(object):
    THR_JOIN_TIMEOUT: float = 5.0
    GATHER_TASK_NAME: str = "_wait-coroutine__"
    MAJOR_TASK_NAME: str = "_major-coroutine__"

    class KEY:
        NAME = "name"
        FUNC = "func"
        ARGS = "args"
        KWARGS = "kwargs"
        CALLBACK = "callback"
    
    _m_loop_ = None
    _ml_tasks_: list = None
    _ml_result_: list = None
    _m_thr_loop_: threading.Thread = None
    

    def register_task(self, name: str, func, callback: Callable[[asyncio.Task], None]=None, *args, **kwargs):
        Key = CAsyncLoop.KEY
        try:
            if name is None or func is None:
                raise RuntimeError(f"'name:{name}' or 'func:{func}' is None. It's not allow.")
            
            task_names = [ item.get(Key.NAME) for item in self._ml_tasks_ ] + [self.GATHER_TASK_NAME, self.MAJOR_TASK_NAME]
            if name in set(task_names):
                raise NameError(f"name({name}) is duplicated with legacy Task-name.")

            self._ml_tasks_.append({Key.NAME: name, Key.FUNC: func, Key.ARGS: args, Key.KWARGS: kwargs, Key.CALLBACK: callback})
        except BaseException as e:
            logging.error(e)
            raise e
    
    def unregister_task(self, name: str=None):
        Key = CAsyncLoop.KEY
        try:
            if name is None:
                self._ml_tasks_.clear()
                return
            
            for item in self._ml_tasks_:
                if name == item.get(Key.NAME, None):
                    self._ml_tasks_.remove(item)
                    break
        except BaseException as e:
            logging.error(e)
            raise e

    def start(self):           # Non-Blocking API
        Key = CAsyncLoop.KEY
        tasks: List[asyncio.Task] = list()
        
        def register_tasks():
            nonlocal tasks
            try:
                for item in self._ml_tasks_:
                    name = item.get(Key.NAME, None)
                    func = item.get(Key.FUNC)
                    args = item.get(Key.ARGS)
                    kwargs = item.get(Key.KWARGS)
                    cb = item.get(Key.CALLBACK)

                    task = self._m_loop_.create_task(func(*args, **kwargs), name=name)
                    if cb is not None:
                        task.add_done_callback( functools.partial(cb) )
                    tasks.append( task )
                
            except BaseException as e:
                logging.error(e)
                raise e
        try:
            register_tasks()
            self._start_(tasks_=tasks)
        except BaseException as e:
            logging.error(e)
            raise e

    def start_onece(self, name: str, func, callback: Callable[[asyncio.Task], None]=None, *args, **kwargs):
        try:
            if name is None or func is None:
                raise RuntimeError("'name' or 'func' is None.")
            
            if self._m_loop_.is_running() is True:
                task_names = [ t.get_name() for t in asyncio.all_tasks(self._m_loop_) ]
                if name in task_names:
                    raise NameError(f"'name'({name}) is already running in event-loop.")

            task = self._m_loop_.create_task(func(*args, **kwargs), name=name)
            if callback is not None:
                task.add_done_callback( functools.partial(callback) )
            
            self._start_(tasks_=[task], onece=True)
        except BaseException as e:
            logging.error(e)
            raise e

    def start_n_wait_done(self):              # Blocking API
        try:
            self.start()
            return self.wait_done()
        except BaseException as e:
                logging.error(e)
                raise e
    
    def wait_done(self, hook: Callable[[],None]=None):           # Blocking API
        try:
            if self._ml_result_ is None:
                raise RuntimeError("TASKs are not started, yet.")
            
            while self._m_loop_.is_running() is True and len(self._ml_result_) < len(self._ml_tasks_):
                if hook is not None:
                    hook()
                time.sleep(1.0)
            
            self._destroy_thread_()
            
            temp = copy.deepcopy(self._ml_result_)
            self._ml_result_ = None
            return temp
        except BaseException as e:
            logging.error(e)
            raise e

    async def run_inline_thread(self, func, *args, **kwargs):
        try:
            if func is None:
                raise RuntimeError("'func' is None.")
            
            ctx = contextvars.copy_context()
            func_call = functools.partial(ctx.run, func, *args, **kwargs)
            return await self._m_loop_.run_in_executor(None, func_call)

        except BaseException as e:
            logging.error(e)
            raise e
        
    ##########################
    # Private Definition
    
    def __init__(self):
        try:
            self._clear_()
            self._ml_tasks_ = list()
            
            self._m_loop_ = asyncio.get_event_loop()
        except BaseException as e:
            logging.error(e)
            raise e

    def __del__(self):
        try:
            self._destroy_thread_(force=True)
            self.unregister_task()
            self._close_()

            # clear varibles
            self._clear_()
        except BaseException as e:
            logging.error(e)
            raise e
    
    def _clear_(self):
        self._m_loop_ = None
        self._ml_tasks_ = None
        self._ml_result_ = None
        self._m_thr_loop_ = None

    def _close_(self):
        try:
            # close async-loop thread if no more task-running.
            if self._m_loop_.is_running() is False:
                if self._m_loop_.is_closed() is True:
                    return
                logging.info("Close Event-Loop.")
                self._m_loop_.close()
                
        except BaseException as e:
            logging.error(e)
            raise e
    
    def _destroy_thread_(self, force: bool=False):
        try:
            if self._m_loop_.is_running() is False or force is True:
                if self._m_thr_loop_ is not None and self._m_thr_loop_.is_alive() is True:
                    self._m_thr_loop_.join(timeout=self.THR_JOIN_TIMEOUT)
                self._m_thr_loop_ = None
        
        except RuntimeError as e:
            logging.warn("{} ({})".format(str(e), self._m_thr_loop_.name))
            if "cannot join current thread" in e.args[0]:
                self._m_thr_loop_ = None
        except BaseException as e:
            logging.error(e)
            raise e

    async def _wait_coroutine_(self, tasks_: List[asyncio.Task], onece: bool=False):
        try:
            is_continue = True
            cur_task = asyncio.current_task(self._m_loop_)
            if cur_task is None:
                raise RuntimeError("[CAsyncLoop:_wait_coroutine_] 'cur_task' is None.")
            cur_name = cur_task.get_name()
            logging.info(f"Running task: {cur_name}")

            result = await asyncio.gather(*tasks_, return_exceptions=True)   # Blocking API
            if onece is False:
                self._ml_result_ += list( zip([ item.get_name() for item in tasks_ ], result) )

            if cur_name == self.GATHER_TASK_NAME:
                return  True

            while is_continue is True:
                remained_tasks = list()
                tasks_ = asyncio.all_tasks(self._m_loop_)
                for task in tasks_:
                    if task.get_name() == cur_name:
                        continue
                    remained_tasks.append(task)

                if len(remained_tasks) <= 0:
                    is_continue = False
                    continue

                await asyncio.sleep(1.0)
            
            logging.info("Done wait_coroutine: {}".format(cur_name))
            return True
        except (GeneratorExit, asyncio.CancelledError) as e:
            logging.warn(e)
        except BaseException as e:
            logging.error(e)
            raise e

    def _start_(self, tasks_: List[asyncio.Task], onece: bool=False):
        def run_event_loop():
            if self._m_loop_.is_running() is False:
                task = self._m_loop_.create_task(self._wait_coroutine_(tasks_, onece), name=self.MAJOR_TASK_NAME)
                self._m_loop_.run_until_complete( task )    # Blocking API

        try:
            if self._ml_result_ is None and onece is False:
                self._ml_result_ = list()

            if self._m_loop_.is_running() is True:
                self._m_loop_.create_task(self._wait_coroutine_(tasks_, onece), name=self.GATHER_TASK_NAME)
                return

            # if not exist, then run 'event-looop' in thread.
            if self._m_thr_loop_ is not None:
                self._destroy_thread_()
            self._m_thr_loop_ = threading.Thread(target=run_event_loop, name=self.MAJOR_TASK_NAME)
            self._m_thr_loop_.start()
        except BaseException as e:
            logging.error(e)
            raise e