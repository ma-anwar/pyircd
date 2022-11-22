"""This module represents a client and defines client message handlers"""
import logging
from selectors import SelectorKey

import constants
from constants import IRC_COMMANDS, IRC_REPLIES
from message import Message


class Client:
    """Class responsible for handling messages related to client connections"""

    def __init__(self, address: str, key: SelectorKey):
        self._logger = logging.getLogger(__name__)
        self._is_registered = False
        self._nick = ""
        self._real_name = ""
        self._username = ""
        self._key = key
        self.address = address

    @property
    def is_registered(self):
        """Get value of _is_registered"""
        return self._is_registered

    @is_registered.setter
    def is_registered(self, is_registered):
        """Set value of is_registered, call success handler if is_registered"""
        self._is_registered = is_registered
        if is_registered:
            self._send_registration_success()

    def _send_registration_success(self):
        """Complete the registration flow as per IRC spec

        https://modern.ircdocs.horse/#connection-registration
        """
        self.send_message(f"{IRC_REPLIES.WELCOME} {self._nick} :Welcome to PyIrcd.")
        self.send_message(
            f"{IRC_REPLIES.YOURHOST} {self._nick} :This daemon is being developed."
        )
        self.send_message(
            f"{IRC_REPLIES.CREATED} {self._nick} : This server was started recently."
        )
        self.send_message(f"{IRC_REPLIES.MYINFO} {self._nick} PyIrcd More info sooon!")

    def handle_message(self, message: Message):
        """Handle message by invoking registration flow"""
        self._logger.debug(message)
        if not self.is_registered:
            self.handle_registration_flow(message)

    def handle_registration_flow(self, message: Message):
        """Handle registration state and ultimately send reply on success WIP"""
        # WIP Need to handle error cases
        if message.command == IRC_COMMANDS.NICK and message.parameters[0]:
            self._nick = message.parameters[0]

        if message.command == IRC_COMMANDS.USER:
            if len(message.parameters) < 4:
                self._logger.debug("ERROR: Not enough params")

            self._username = message.parameters[0]
            self._real_name = message.parameters[3]

        # user_name implies real_name is present
        if self._username and self._nick:
            self.is_registered = True

    def send_message(self, message: str):
        """Write message to the out buffer of this client instance

        message: utf-8 string, optionally terminated with \r\n
        """
        message_as_bytes = message.encode()

        if not message_as_bytes.endswith(constants.IRC_TERMINATION_DELIMITER):
            message_as_bytes += constants.IRC_TERMINATION_DELIMITER

        self._key.data.out_buffer += message_as_bytes
