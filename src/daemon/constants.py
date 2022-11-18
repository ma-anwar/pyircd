NICK_COMMAND = b"NICK"
USER_COMMAND = b"USER"
IRC_TERMINATION_DELIMITER = b"\r\n"
EMPTY_STRING = b""
# Most IRC servers limit messages to 512 bytes in length
# https://modern.ircdocs.horse/#message-format
RECEIVE_LENGTH = 1024
