############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import logging
import random
import time
import copy as cp

from retry.compat import decorator

__all__= [ "retry" ]

logging_logger = logging.getLogger(__name__)

_DEF_TRY_IDX_="try_idx"


def __retry_internal(f, exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0,
                     logger=logging_logger):
    """
    Executes a function and retries it if it failed.

    :param f: the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """
    _tries, _delay = tries, delay
    while _tries:
        try:
            return f( _try_idx=(tries-_tries+1) )
        except exceptions as e:
            _tries -= 1
            if not _tries:
                raise e

            if logger is not None:
                logger.warn('%s, retrying in %s seconds...', e, _delay)

            time.sleep(_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)
                
        except BaseException as e:
            if logger is not None:
                logger.error(e)
            raise e


def retry(exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0, logger=logging_logger):
    """Returns a retry decorator.

    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: a retry decorator.
    """
    @decorator
    def retry_decorator(f, *fargs, **fkwargs):
        return retry_call(f, fargs, fkwargs, exceptions, tries, delay, max_delay, backoff, jitter, logger)

    return retry_decorator


def retry_call(f, fargs=None, fkwargs=None, exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1,
               jitter=0, logger=logging_logger):
    """
    Calls a function and re-executes it if it failed.
    
    Attention:
        1. Not Supported Case
            arguments중 마지막 혹은 중간의 arg의 type이 명세되지 않은 경우.
            Ex) def func_name(self, arg1: type1, arg2:type2=None, arg3=None)
                def func_name(self, arg1: type1, arg2=None,       arg3:type3=None)
            

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """
    try:
        arg_start_idx = 0
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        arg_keys = cp.deepcopy( list(f.__annotations__.keys()) )   # get key-names as arguments
        
        # if need, then remove 'return' arguments.
        if len(arg_keys) > 0 and arg_keys[-1] == "return":
            arg_keys.pop()
        
        # search 'start-point' in args to find values of arg_keys.
        arg_start_idx = (len(args)+len(kwargs)) - len(arg_keys)
        
        if len(arg_keys) > 0:
            # validation check about 'args' length.
            if len(arg_keys) < len(args[arg_start_idx:]):
                raise RuntimeError("'arg_keys' annotation is not satisfied. (length is missmatching)")
            
            # copy elements from 'args' to 'kwargs'
            for idx, arg in enumerate(args[arg_start_idx:]):
                kwargs.update({arg_keys[idx]: arg})
        
        # define caller-function
        def __caller(_try_idx: int):
            if _DEF_TRY_IDX_ in arg_keys:
                kwargs.update({_DEF_TRY_IDX_: _try_idx})
            if len(arg_keys) <= 0 and len(kwargs) <= 0:
                return f(*args)
            
            return f(*args[:arg_start_idx], **kwargs)
        
        # run custom-function.
        return __retry_internal(__caller, exceptions, tries, delay, max_delay, backoff, jitter, logger)
    
    except BaseException as e:
        if logger is not None:
            logger.error(e)
        raise e
