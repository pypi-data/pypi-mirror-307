############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

from queue import Queue
import threading
from collections import OrderedDict

__all__=["CThread"]


def assertMy( func, except_type, msg: str="", debug_msg: str=None ):
    if (func) == False:
        if debug_msg is not None:
            print(f"[D][CThread] {debug_msg}\n")

        raise except_type(msg)
    
    
class CThread(threading.Thread):
    _is_continue_ = False
    _queues_ = None
    _events_ = None

    @property
    def is_continue(self):
        return self._is_continue_

    @is_continue.setter
    def is_continue(self, value: bool):
        assertMy(isinstance(value, bool) is True, BaseException, "value is not Boolean-type.")
        self._is_continue_ = value

    def append_queue(self, qname: str):
        try:
            assertMy(qname is not None, BaseException, "qname is None.")
            assertMy(self.is_alive() is False, BaseException, "Already Thread started. We can append New-queue.")
            if qname in self.get_queue_list():
                print("[W][CThread] append_queue: Already exist queue-name(%s)\n" % qname)
                return

            qhandler = Queue()
            assertMy(qhandler is not None, BaseException, "qhandler is None.")
            self._queues_.update({qname: qhandler})

        except BaseException as e:
            print(f"[E][CThread] append_queue: {e}\n")

    def get_queue_list(self) -> list:
        return list(self._queues_.keys())

    def get_queue(self, qname: str) -> Queue:
        result = None
        try:
            assertMy(qname is not None, BaseException, "qname is None")
            if qname in self.get_queue_list():
                result = self._queues_[qname]

        except BaseException as e:
            print(f"[E][CThread] get_queue: {e}\n")
        return result

    def append_event(self, ename: str):
        try:
            assertMy(ename is not None, BaseException, "ename is None.")
            assertMy(self.is_alive() is False, BaseException, "Already Thread started. We can append New-event.")
            if ename in self.get_event_list():
                print("[W][CThread] append_event: Already exist event-name(%s)\n" % ename)
                return

            ehandler = threading.Event()
            assertMy(ehandler is not None, BaseException, "ehandler is None.")
            self._events_.update({ename: ehandler})

        except BaseException as e:
            print(f"[E][CThread] append_event: {e}\n")

    def get_event_list(self) -> list:
        return list(self._events_.keys())

    def get_event(self, ename: str) -> threading.Event:
        result = None
        try:
            assertMy(ename is not None, BaseException, "ename is None")
            if ename in self.get_event_list():
                result = self._events_[ename]

        except BaseException as e:
            print(f"[E][CThread] get_event: {e}\n")
        return result

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

    def __init__(self, name: str, func, daemon: bool=False, args: tuple=(), kwargs: dict={}):
        try:
            super().__init__(name=name, target=func, args=args, kwargs=kwargs, daemon=daemon)
            self._queues_ = OrderedDict()
            self._events_ = OrderedDict()

        except BaseException as e:
            print(f"[E][CThread] __init__: {e}\n")

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
            print(f"[E][CThread] __del__: {e}\n")

