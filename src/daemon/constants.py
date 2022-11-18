NICK_COMMAND = b"NICK"
USER_COMMAND = b"USER"
IRC_TERMINATION_DELIMITER = b"\r\n"
EMPTY_STRING = b""
# Most IRC servers limit messages to 512 bytes in length
# https://modern.ircdocs.horse/#message-format
RECEIVE_LENGTH = 1024

# +1 for \n since find gives us index of \r
# +1 bc end index is not inclusive
DELIMITER_END_INDEX = 2

NOT_FOUND = -1
LOCAL_HOST = "127.0.0.1"
DEFAULT_PORT = 6667
