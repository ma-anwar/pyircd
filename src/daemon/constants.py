"""This module holds constants used throughout the daemon"""
from enum import Enum, unique

import config


# Use str as value in enums: https://docs.python.org/3/library/enum.html#notes
@unique
class IRC_COMMANDS(str, Enum):
    NICK = "NICK"
    USER = "USER"
    PASS = "PASS"
    PING = "PING"
    PONG = "PONG"
    QUIT = "QUIT"
    ERROR = "ERROR"
    JOIN = "JOIN"


@unique
class IRC_ERRORS(str, Enum):
    NOSUCHCHANNEL = "403"
    NO_NICKNAME_GIVEN = "431"
    NICKNAME_IN_USE = "432"
    NOTONCHANNEL = "442"
    NEED_MORE_PARAMS = "461"
    ALREADY_REGISTERED = "462"
    CHANNELISFULL = "471"
    BADCHANMASK = "476"
    USERONCHANNEL = "443"


# https://modern.ircdocs.horse/#numerics
@unique
class IRC_REPLIES(str, Enum):
    WELCOME = "001"
    YOURHOST = "002"
    CREATED = "003"
    MYINFO = "004"
    NOTOPIC = "331"
    TOPIC = "332"
    NAMREPLY = "353"
    ENDOFNAMES = "366"


# https://modern.ircdocs.horse/#message-format
IRC_TERMINATION_DELIMITER = b"\r\n"

EMPTY_STRING = b""

# Most IRC servers limit messages to 512 bytes in length
# https://modern.ircdocs.horse/#message-format
RECEIVE_LENGTH = 1024
MAX_LINE_LENGTH = 512

# +1 for \n since find gives us index of \r
# +1 bc end index is not inclusive
DELIMITER_END_OFFSET = 2

# -1 is returned by find when not found
NOT_FOUND = -1

LOCAL_HOST = "127.0.0.1"
DEFAULT_PORT = 6667

ACCEPTED_ACTIONS = ["PARSE"]

# Based on https://modern.ircdocs.horse/#client-messages
VALID_ALPHA_COMMANDS = [
    "CAP",
    "AUTHENTICATE",
    "PASS",
    "NICK",
    "USER",
    "PING",
    "PONG",
    "OPER",
    "QUIT",
    "ERROR",
    "JOIN",
    "PART",
    "TOPIC",
    "NAMES",
    "LIST",
    "INVITE",
    "KICK",
    "MOTD",
    "VERSION",
    "ADMIN",
    "CONNECT",
    "TIME",
    "STATS",
    "HELP",
    "INFO",
    "MODE",
    "PRIVMSG",
    "NOTICE",
    "WHO",
    "WHOIS",
    "WHOWAS",
    "KILL",
    "REHASH",
    "RESTART",
    "SQUIT",
    "AWAY",
    "LINKS",
    "USERHOST",
    "WALLOPS",
]

MESSAGE_PREFIX = f":{config.SERVER_NAME} "

# https://modern.ircdocs.horse/#channels
FORBIDDEN_CHANNELNAME_CHARS = [
    " ",
    ",",
    bytes.fromhex("00000007").decode("utf-8"),  # The ^G character (0x07)
]
