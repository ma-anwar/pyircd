"""This module holds constants used throughout the daemon"""
from enum import Enum, unique


# Use str as value in enums: https://docs.python.org/3/library/enum.html#notes
@unique
class IRC_COMMANDS(str, Enum):
    NICK = "NICK"
    USER = "USER"
    PASS = "PASS"


# https://modern.ircdocs.horse/#numerics
@unique
class IRC_REPLIES(str, Enum):
    WELCOME = "001"
    YOURHOST = "002"
    CREATED = "003"
    MYINFO = "004"


# https://modern.ircdocs.horse/#message-format
IRC_TERMINATION_DELIMITER = b"\r\n"

EMPTY_STRING = b""

# Most IRC servers limit messages to 512 bytes in length
# https://modern.ircdocs.horse/#message-format
RECEIVE_LENGTH = 1024

# +1 for \n since find gives us index of \r
# +1 bc end index is not inclusive
DELIMITER_END_OFFSET = 2

# -1 is returned by find when not found
NOT_FOUND = -1

LOCAL_HOST = "127.0.0.1"
DEFAULT_PORT = 6667
