class MyFrameworkException(Exception):
    """MyFrameworkException"""

    def __str__(self) -> str:
        if self.__doc__:
            return self.__doc__
        return "MyFrameworkException"


class MFNotImplementedError(MyFrameworkException):
    """method request is not implemented"""


class MFalreadyRegisteredError(MyFrameworkException):
    """controller has already registered"""
