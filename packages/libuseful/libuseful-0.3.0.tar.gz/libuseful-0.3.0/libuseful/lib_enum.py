############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

__all__ = ["ENUM_STR", "enum" ]

class ENUM_STR(object):

    _value_ = None

    def __init__(self, val: str):
        self._value_ = val

    def __str__(self):
        return self._value_


def enum(**enums):
    return type('Enum', (), enums)




