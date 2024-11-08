
__all__ = [ "CEOutOfRange", "CEInvalidArguments", "CENotInitialized", 
            "CEOutOfLeagueException", "CECannotRecoveryException", "CEInvalidValueException", 
            "CEMissMatchedException", "CENullException", "CENotFoundException", 
            "CECommunicationError", "CEMandatoryError", "CENotSupportException",
            "CELogicErrorException" ]


# Copyright (c) 2022- excel exception

""" Definitions for Util of Gbox shared exception classes. """

class CEOutOfRange(Exception):
    """Error for Out-of-range Exception."""

class CEInvalidArguments(Exception):
    """Error for Invalid-Arguments Exception."""
    
class CENotInitialized(Exception):
    """Error for Not-Initialization Exception."""

class CEOutOfLeagueException(Exception):
    """Error for Out-of-League Exception."""
    
class CECannotRecoveryException(Exception):
    """Error for Can-not receovery Exception."""

class CEInvalidValueException(Exception):
    """Error for Invalid Value Exception."""

class CEMissMatchedException(Exception):
    """Error for Missmatched Exception."""

class CENullException(Exception):
    """Error for Null-Pointer Exception."""

class CENotFoundException(Exception):
    """Error for Can-not-find Exception."""
    
class CECommunicationError(Exception):
    """Error for Communication Error Exception."""

class CEMandatoryError(Exception):
    """Error for Mandatory Error Exception."""

class CENotSupportException(Exception):
    """Error for Not-Supported yet Exception. """

class CELogicErrorException(Exception):
    """Error for Logic-Error Exception """

