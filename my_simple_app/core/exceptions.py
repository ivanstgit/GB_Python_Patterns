class MyAppException(Exception):
    """MyAppException"""

    def __str__(self) -> str:
        if self.__doc__:
            return self.__doc__
        return "MyAppException"


class MyAppAlreadyExistsError(MyAppException):
    """object already exists"""
