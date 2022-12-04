"""Holds global variables to be shared across modules

https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
"""


SERVER_NAME = "pyircd"


def init(name: str):
    """This method should only be called by the daemon module"""
    global SERVER_NAME
    SERVER_NAME = name if name is not None else "pyircd"
