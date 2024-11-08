############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

from collections import OrderedDict
from .lib_thread import CThread

from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)

__all__=["CMthreads"]


class CMthreads(object):

    _handler_ = None

    def append_thread(self, name: str, run_func,
                      args: tuple=(), kwargs: dict={}, daemon: bool=False,
                      queue_names: list=None, event_names: list=None):
        try:
            assertMy(name is not None, BaseException, "name is None.")
            assertMy(run_func is not None, BaseException, "run_func is None.")
            assertMy(isinstance(name, str), BaseException, "name is not string-type.")

            handler = CThread(name=name, func=run_func, daemon=daemon, args=args, kwargs=kwargs)
            assertMy(handler is not None, BaseException, "thread handler is None.")

            if name in self._handler_.keys():
                logger.info("Already exist thread_name. We will destroy already-exist thread.")
                self.remove_thread(name)

            self._handler_.update({name: handler})

            if queue_names is not None:
                assertMy(isinstance(queue_names, list) is True, BaseException, "queue_names is not list-type.")
                for qname in queue_names:
                    handler.append_queue(qname)

            if event_names is not None:
                assertMy(isinstance(event_names, list) is True, BaseException, "event_names is not list-type.")
                for ename in event_names:
                    handler.append_event(ename)

        except BaseException as e:
            logger.error(e)

    def start_all(self):
        try:
            tnames = self.get_thread_list()
            if tnames is not None:
                for tname in tnames:
                    handler = self._handler_[tname]
                    assertMy(handler is not None, BaseException, "handler is None.")
                    if isinstance(handler, CThread) is False:
                        raise BaseException("handler is not CProcessor type.")
                    handler.start()

        except BaseException as e:
            logger.error(e)

    def stop_all(self):
        try:
            tnames = self.get_thread_list()
            if tnames is not None:
                for tname in tnames:
                    self.remove_thread(tname)
        except BaseException as e:
            logger.error(e)
            raise e

    def remove_thread(self, tname: str):
        try:
            if tname is None:
                logger.warn("name is None.")
                return

            if tname in self.get_thread_list():
                handler = self._handler_[tname]
                assertMy(handler is not None, BaseException, "handler is None.")

                del self._handler_[tname]
                assertMy(tname not in self.get_thread_list(), BaseException, "tname is there in handler_dict.")

                if isinstance(handler, CThread) is False:
                    raise BaseException("handler is not CThread-type.")
                if handler.is_alive() is True:
                    handler.is_continue = False
                    handler.join()      # Blocking Function
                del handler

        except BaseException as e:
            logger.error(e)

    def get_thread_list(self) -> list:
        return list(self._handler_.keys())

    def get_thread_handler(self, tname: str) -> CThread:
        result = None
        try:
            assertMy(tname is not None, BaseException, "name is None.")
            assertMy(isinstance(tname, str) is not None, BaseException, "name is not string-type.")
            if tname in self.get_thread_list():
                result = self._handler_[tname]

        except BaseException as e:
            logger.error(e)
        return result

    def __init__(self):
        try:
            self._handler_ = OrderedDict()
            assertMy(self._handler_ is not None, BaseException, "handler_dict is None.")

        except BaseException as e:
            logger.error(e)

    def __del__(self):
        try:
            if self._handler_ is not None:
                tnames = self.get_thread_list()
                if tnames is not None:
                    for tname in tnames:
                        self.remove_thread(tname)

                del self._handler_
                self._handler_ = None

        except BaseException as e:
            logger.error(e)
