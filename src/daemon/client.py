"""This module represents a client and defines client message handlers"""
import logging
from selectors import SelectorKey

import constants
from constants import IRC_COMMANDS, IRC_ERRORS, IRC_REPLIES
from message import Message


class Client:
    """Class responsible for handling messages related to client connections"""

    registered_nicks = []

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
            Client.registered_nicks.append(self._nick)

    def _send_registration_success(self):
        """Complete the registration flow as per IRC spec

        https://modern.ircdocs.horse/#connection-registration
        """
        self.send_message(IRC_REPLIES.WELCOME, ":Welcome to Pyircd")
        self.send_message(IRC_REPLIES.YOURHOST, ":This daemon is being developed.")
        self.send_message(IRC_REPLIES.CREATED, ":This server was started recently")
        self.send_message(IRC_REPLIES.MYINFO, "Pyircd More info sooon!")

    def handle_message(self, message: Message):
        """Handle message by invoking registration flow"""
        self._logger.debug(message)
        if not self.is_registered:
            self._handle_registration_flow(message)

    def _handle_registration_flow(self, message: Message):
        """Handle registration state and ultimately send reply on success WIP"""
        if message.command == IRC_COMMANDS.NICK:
            self._handle_nick(message)

        if message.command == IRC_COMMANDS.USER:
            self._handle_user(message)

        # user_name implies real_name is present
        if self._username and self._nick:
            self.is_registered = True

    def _handle_nick(self, message: Message):
        """Handle NICK command"""
        if self._is_registered:
            return

        candidate_nick = message.parameters[0] if len(message.parameters) > 0 else None

        if not candidate_nick:
            self.send_message(IRC_ERRORS.NO_NICKNAME_GIVEN, ":No nickname given")
            return

        if candidate_nick in Client.registered_nicks:
            self.send_message(
                IRC_ERRORS.NICKNAME_IN_USE,
                f"{candidate_nick}:Nickname is already in use",
            )
            return

        self._nick = candidate_nick

    def _handle_user(self, message: Message):
        """Handle USER command"""
        if self._is_registered:
            self.send_message(
                IRC_ERRORS.ALREADY_REGISTERED,
                ":Unauthorized command (already registered)",
            )
            return

        print(message)
        if len(message.parameters) < 4:
            self.send_message(IRC_ERRORS.NEED_MORE_PARAMS, "")
            return

        self._username = message.parameters[0]
        self._real_name = message.parameters[3]

    def send_message(self, numeric: str, message: str):
        """Write message to the out buffer of this client instance

        https://modern.ircdocs.horse/#numeric-replies
        numeric: 3 digit code per docs
        message: utf-8 string, optionally terminated with \r\n
        """
        constructed_messsage = (
            f"{constants.MESSAGE_PREFIX} {numeric} {self._nick} {message}"
        )
        message_as_bytes = constructed_messsage.encode()

        if not message_as_bytes.endswith(constants.IRC_TERMINATION_DELIMITER):
            message_as_bytes += constants.IRC_TERMINATION_DELIMITER

        self._key.data.out_buffer += message_as_bytes
