import logging

from message import Message


class Parser:
    def __init__(self, dispatch: callable):
        self.logger = logging.getLogger("Parser")
        self.__dispatch = dispatch

    def __handle_message(self, message: Message):
        self.logger.debug(message)
        parsed_message = self.__parse_message(message)
        self.logger.debug(parsed_message)
        self.__dispatch(parsed_message)

    def dispatch(self, message: Message):
        self.__handle_message(message)

    # Jank temporary parse function, not to spec, just for PoC
    def __parse_message(self, message: Message) -> Message:
        # Remove EOL delimiter
        stripped_message = message.message[:-2]

        split_message = stripped_message.split()

        command = split_message.pop(0)
        parameters = split_message

        parsed_message = Message(
            message.client_address,
            "HANDLE",
            message.message,
            message.key,
            command,
            parameters,
        )

        return parsed_message
