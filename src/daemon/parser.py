"""The module is responsible for parsing IRC messages according to specification"""
import logging

import constants
from message import Message


class Parser:
    """Parser responsible for parsing received IRC messages

    It receives a Message object. It parses the message creates a new
    Message with command and parameter fields. Finally it dispatches the
    Message to the EventBus.
    """

    def __init__(self, dispatch: callable):
        """Save the dispatch function to send messages to event_bus"""
        self.logger = logging.getLogger("Parser")
        self.__dispatch = dispatch

    def __handle_message(self, message: Message):
        """Handle Message and dispatch it to EventBus"""
        self.logger.debug(message)
        parsed_message = self.__parse_message(message)
        self.logger.debug(parsed_message)
        self.__dispatch(parsed_message)

    def dispatch(self, message: Message):
        """Call handler on message, used by Server"""
        self.__handle_message(message)

    # Jank temporary parse function, not to spec, just for PoC
    def __parse_message(self, message: Message) -> Message:
        """Parse message according to IRC spec"""
        # Remove EOL delimiter
        delimiter_length = len(constants.IRC_TERMINATION_DELIMITER)
        stripped_message = message.message[:-delimiter_length]

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
