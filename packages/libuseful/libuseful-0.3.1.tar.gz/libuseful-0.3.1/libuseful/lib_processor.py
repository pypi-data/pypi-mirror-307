############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

from typing import Dict
import multiprocessing
import multiprocessing.synchronize
from collections import OrderedDict
from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)

__all__=["CMprocessors", "CProcessor"]


class CProcessor(multiprocessing.Process):

    _is_continue_ = False
    _queues_: Dict[multiprocessing.Queue] = None
    _events_: Dict[multiprocessing.synchronize.Event] = None

    @property
    def is_continue(self) -> bool:
        return self._is_continue_

    @is_continue.setter
    def is_continue(self, value: bool):
        try:
            assertMy(isinstance(value, bool) is True, BaseException, "value is not Boolean-type.")
            self._is_continue_ = value

        except BaseException as e:
            logger.error(e)

    def append_queue(self, qname: str):
        try:
            assertMy(qname is not None, BaseException, "qname is None.")
            assertMy(self.is_alive() is False, BaseException, "Already Thread started. We can append New-queue.")
            if qname in self.get_queue_list():
                logger.warn("Already exist queue-name(%s)" % qname)
                return

            qhandler = multiprocessing.Queue()
            assertMy(qhandler is not None, BaseException, "qhandler is None.")
            self._queues_.update({qname: qhandler})

        except BaseException as e:
            logger.error(e)

    def get_queue_list(self) -> list:
        return list(self._queues_.keys())

    def get_queue(self, qname: str) -> multiprocessing.Queue:
        result = None
        try:
            assertMy(qname is not None, BaseException, "qname is None")
            if qname in self.get_queue_list():
                result = self._queues_[qname]

        except BaseException as e:
            logger.error(e)
        return result

    def append_event(self, ename: str):
        try:
            assertMy(ename is not None, BaseException, "ename is None.")
            assertMy(self.is_alive() is False, BaseException, "Already Thread started. We can append New-event.")
            if ename in self.get_event_list():
                logger.warn("Already exist event-name(%s)" % ename)
                return

            ehandler = multiprocessing.Event()
            assertMy(ehandler is not None, BaseException, "ehandler is None.")
            self._events_.update({ename: ehandler})

        except BaseException as e:
            logger.error(e)

    def get_event_list(self) -> list:
        return list(self._events_.keys())

    def get_event(self, ename: str) -> multiprocessing.synchronize.Event:
        result = None
        try:
            assertMy(ename is not None, BaseException, "ename is None")
            if ename in self.get_event_list():
                result = self._events_[ename]

        except BaseException as e:
            logger.error(e)
        return result

    def thread_join(self):
        try:
            for (qname, queue) in self._queues_.items():
                if isinstance(queue, multiprocessing.queues.Queue) is False:
                    raise BaseException("queue is not multiprocessing.Queue-type.")
                queue.close()
                queue.join_thread()
                del queue

            del self._queues_
            self._queues_ = None

        except BaseException as e:
            logger.error(e)

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target:
                self.is_continue = True
                self._target(self, *self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def __init__(self, name: str, func, args: tuple=(), kwargs: dict={}):
        try:
            super().__init__(name=name, target=func, args=args, kwargs=kwargs)
            self._queues_ = OrderedDict()
            self._events_ = OrderedDict()

        except BaseException as e:
            logger.error(e)

    def __del__(self):
        try:
            self.is_continue = False

            # Clear Queues
            if self._queues_ != None:
                for (qname, queue) in self._queues_.items():
                    if queue is not None:
                        del queue
                del self._queues_
                self._queues_ = None

            # Clear Events
            if self._events_ != None:
                for (ename, event) in self._events_.items():
                    if event is not None:
                        del event
                del self._events_
                self._events_ = None

        except BaseException as e:
            logger.error(e)


class CMprocessors(object):

    _handler_ = None

    def append_processor(self, name: str, run_func,
                      args: tuple=(), kwargs: dict={},
                      queue_names: list=None, event_names: list=None):
        try:
            assertMy(name is not None, BaseException, "name is None.")
            assertMy(run_func is not None, BaseException, "run_func is None.")
            assertMy(isinstance(name, str), BaseException, "name is not string-type.")

            handler = CProcessor(name=name, func=run_func, args=args, kwargs=kwargs)
            assertMy(handler is not None, BaseException, "thread handler is None.")

            if name in self._handler_.keys():
                logger.info("Already exist thread_name. We will destroy already-exist thread.")
                self.remove_processor(name)

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
            tnames = self.get_processor_list()
            if tnames is not None:
                for tname in tnames:
                    handler = self._handler_[tname]
                    assertMy(handler is not None, BaseException, "handler is None.")
                    if isinstance(handler, CProcessor) is False:
                        raise BaseException("handler is not CProcessor type.")
                    handler.start()

        except BaseException as e:
            logger.error(e)

    def remove_processor(self, tname: str):
        try:
            if tname is None:
                logger.warn("name is None.")
                return

            if tname in self.get_processor_list():
                handler = self._handler_[tname]
                assertMy(handler is not None, BaseException, "handler is None.")

                del self._handler_[tname]
                assertMy(tname not in self.get_processor_list(), BaseException, "tname is there in handler_dict.")

                if isinstance(handler, CProcessor) is False:
                    raise BaseException("handler is not CThread-type.")
                if handler.is_alive() is True:
                    handler.is_continue = False
                    handler.thread_join()
                    handler.join(timeout=1)      # Blocking Function (timeout : 1 seconds)
                    if handler.is_alive() is True:
                        handler.terminate()

                del handler

        except BaseException as e:
            logger.error(e)

    def get_processor_list(self) -> list:
        return list(self._handler_.keys())

    def get_processor_handler(self, tname: str) -> CProcessor:
        result = None
        try:
            assertMy(tname is not None, BaseException, "name is None.")
            assertMy(isinstance(tname, str) is not None, BaseException, "name is not string-type.")
            if tname in self.get_processor_list():
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
                tnames = self.get_processor_list()
                if tnames is not None:
                    for tname in tnames:
                        self.remove_processor(tname)

                del self._handler_
                self._handler_ = None

        except BaseException as e:
            logger.error(e)
