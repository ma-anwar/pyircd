"""This module holds constants used throughout the daemon"""

NICK_COMMAND = b"NICK"
USER_COMMAND = b"USER"
IRC_TERMINATION_DELIMITER = b"\r\n"
EMPTY_STRING = b""
# Most IRC servers limit messages to 512 bytes in length
# https://modern.ircdocs.horse/#message-format
RECEIVE_LENGTH = 1024
MAX_LINE_LENGTH = 512

# +1 for \n since find gives us index of \r
# +1 bc end index is not inclusive
DELIMITER_END_INDEX = 2

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
