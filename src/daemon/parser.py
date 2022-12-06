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
        self._logger = logging.getLogger("Parser")
        self._dispatch = dispatch

    def _handle_message(self, message: Message):
        """Handle Message and dispatch it to EventBus"""
        self._logger.debug(message)

        # Forward messages that are not to be parsed
        if message.action not in constants.ACCEPTED_ACTIONS:
            self._dispatch(message)
            return

        parsed_message = self._parse_message(message)
        self._logger.debug(parsed_message)
        if parsed_message is not None:
            self._dispatch(parsed_message)

    def dispatch(self, message: Message):
        """Receive incoming message at parser"""
        # Currently, the delimiter check is being done inside server.py
        # If the delimiter is not found, the message never reaches the parser
        self._handle_message(message)

    def _parse_parameters(self, parameters: list):
        """Return a list of parsed parameters.
        If there are any bad parameters, return None"""
        for i in range(len(parameters)):
            for forbidden_sequence in ["\0", "\r", "\n", "::"]:
                if forbidden_sequence in parameters[i]:
                    return None
        return parameters

    def _parse_message(self, message: Message) -> Message | None:
        """Parse message according to IRC spec
        If parse is successful, forward message to EventBus
        Otherwise, drop message"""

        # Decode message
        try:
            message_str = message.message.decode("utf-8")
        except UnicodeDecodeError:
            self._logger.debug("Could not decode message from utf-8 encoding!")
            return

        # Remove EOL delimiter
        delimiter_length = len(constants.IRC_TERMINATION_DELIMITER)
        stripped_message = message_str[:-delimiter_length].lstrip()

        # Accept messages that exceed MAX_LINE_LENGTH, but slice them
        # https://modern.ircdocs.horse/#compatibility-with-incorrect-software
        if len(stripped_message) > constants.MAX_LINE_LENGTH - delimiter_length:
            stripped_message = stripped_message[
                : constants.MAX_LINE_LENGTH - delimiter_length
            ]

        # Find colon in message, if exists
        aggregated_param = None
        colon_index = stripped_message.find(":")
        if colon_index > -1 and colon_index < len(stripped_message):
            aggregated_param = self._parse_parameters(
                [stripped_message[colon_index + 1 :]]
            )
            if aggregated_param is None:
                return
            stripped_message = stripped_message[:colon_index].rstrip()

        # Split message by space
        split_message = stripped_message.split(" ")

        # Inspect contents (assume no tags and source for now)
        if len(split_message) < 1 and aggregated_param is None:
            return

        command = split_message[0].upper()
        parameters = self._parse_parameters(split_message[1:])
        for param in parameters:
            if param == "":
                parameters.remove(param)
        if aggregated_param is not None:
            parameters.append(aggregated_param[0])

        if (command not in constants.VALID_ALPHA_COMMANDS) or parameters is None:
            return

        # Return parsed message
        parsed_message = Message(
            message.client_address,
            "HANDLE",
            message.message,
            message.key,
            command,
            parameters,
        )

        return parsed_message
