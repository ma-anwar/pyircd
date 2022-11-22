"""This module represents a client and defines client message handlers"""
import logging
from selectors import SelectorKey

import constants
from message import Message


class Client:
    """Class responsible for handling messages related to client connections"""

    def __init__(self, address: str, key: SelectorKey):
        self._logger = logging.getLogger("client")
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
        self._key.data.out_buffer += (
            b"001 %s: Hi, welcome to our PyIrcd\r\n" % self._nick.encode()
        )
        self._key.data.out_buffer += (
            b"002 %s: Your host is PyIrcd, running version 1\r\n" % self._nick.encode()
        )
        self._key.data.out_buffer += (
            b"003 %s: This server is being created\r\n" % self._nick.encode()
        )
        self._key.data.out_buffer += (
            b"004 %s: This server is being created\r\n" % self._nick.encode()
        )

    def handle_message(self, message: Message):
        """Handle message by invoking registration flow"""
        self._logger.debug(message)
        if not self.is_registered:
            self.handle_registration_flow(message)

    def handle_registration_flow(self, message: Message):
        """Handle registration state and ultimately send reply on success WIP"""
        # WIP registration flow
        # Need to handle error cases
        if message.command == constants.NICK_COMMAND and message.parameters[0]:
            self._nick = message.parameters[0]

        if message.command == constants.USER_COMMAND:
            if len(message.parameters) < 4:
                self._logger.info("ERROR")

            self._username = message.parameters[0]
            self._real_name = message.parameters[3]

        # user_name implies real_name is present
        if self._username and self._nick:
            self.is_registered = True
