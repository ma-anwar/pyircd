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
        self._dispatch = dispatch

    def _handle_message(self, message: Message):
        """Handle Message and dispatch it to EventBus"""
        self.logger.debug(message)
        parsed_message = self._parse_message(message)
        self.logger.debug(parsed_message)
        self._dispatch(parsed_message)

    def dispatch(self, message: Message):
        """Receive incoming message at parser"""
        # Currently, the delimiter check is being done inside server.py
        # If the delimiter is not found, the message never reaches the parser
        self._handle_message(message)

    def refuse():
        """Refuse to parse the message any further"""
        empty_message = None
        return empty_message

    # Work-in-progress, INCOMPLETE
    def _parse_message(self, message: Message) -> Message:
        """Parse message according to IRC spec"""

        if message.action not in [constants.ACCEPTED_ACTIONS]:
            return self.refuse()

        # Decode message
        message_str = message.message.decode("utf-8")

        # Remove EOL delimiter
        delimiter_length = len(constants.IRC_TERMINATION_DELIMITER)
        stripped_message = message_str[:-delimiter_length]

        # Accept messages that exceed MAX_LINE_LENGTH, but slice them
        if len(stripped_message) > constants.MAX_LINE_LENGTH - 2:
            stripped_message = stripped_message[: constants.MAX_LINE_LENGTH - 2]
        else:
            stripped_message = stripped_message

        # Split message by space
        split_message = stripped_message.split()

        # Inspect contents (assume no tags and source for now)
        if len(split_message) < 2:
            return self.refuse()

        command = split_message[0]
        parameters = split_message[1:]

        if (
            command not in constants.VALID_ALPHA_COMMANDS
            or command not in constants.VALID_NUMERIC_COMMANDS
        ):
            return self.refuse()

        # Add delimiter to message before returning
        return_msg = stripped_message + "\r\n"

        # Encode message before sending back
        return_msg = return_msg.encode("utf-8")

        # Return parsed message
        parsed_message = Message(
            message.client_address,
            "HANDLE",
            return_msg,
            message.key,
            command,
            parameters,
        )

        return parsed_message
