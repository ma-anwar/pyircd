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
        # Currently, the delimiter check is being done inside server.py
        # If the delimiter is not found, the message never reaches the parser
        self.__handle_message(message)

    # Work-in-progress, INCOMPLETE
    def __parse_message(self, message: Message) -> Message:
        """Parse message according to IRC spec"""
        # Decode message
        message_str = message.message.decode("utf-8")

        # Remove EOL delimiter
        delimiter_length = len(constants.IRC_TERMINATION_DELIMITER)
        stripped_message = message_str[:-delimiter_length]

        # Check whether the message length exceeds the max length
        if len(stripped_message) > constants.MAX_LINE_LENGTH - 2:
            ret_msg = stripped_message[: constants.MAX_LINE_LENGTH - 2] + "\r\n"
        else:
            ret_msg = stripped_message + "\r\n"

        # Check for prefix?
        # A prefix could be used to invoke a command instead of sending a message

        # Check command
        split_message = stripped_message.split()

        # Check params
        command = split_message.pop(0)
        parameters = split_message

        # Encode message
        ret_msg = ret_msg.encode("utf-8")

        # Return parsed message
        parsed_message = Message(
            message.client_address,
            "HANDLE",
            ret_msg,
            message.key,
            command,
            parameters,
        )

        return parsed_message
