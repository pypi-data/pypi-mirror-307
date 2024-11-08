############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import threading

__all__ = [ "Singleton" ]


class Singleton:
    __m_instance_ = None
    __m_lock_ = threading.Lock()

    @classmethod
    def get_instance(cls, *args, **kargs):
        try:
            with cls.__m_lock_:
                if cls.__m_instance_ is None:
                    cls.__m_instance_ = cls(*args, **kargs)
                    
            return cls.__m_instance_
        except BaseException as e:
            print("[Error][Singleton] Fail get_instance method.\n")
            raise e




