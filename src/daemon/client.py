import logging

import constants
from message import Message


class Client:
    def __init__(self):
        # Add address in logger output?
        self.logger = logging.getLogger("client")
        self.is_registered = False
        self.nick = b""
        self.real_name = b""
        self.user_name = b""

    def handle_message(self, message: Message):
        self.logger.debug(message)
        if not self.is_registered:
            self.handle_registration_flow(message)

    def handle_registration_flow(self, message: Message):
        # Need to handle error cases
        if message.command == constants.NICK_COMMAND and message.parameters[0]:
            self.nick = message.parameters[0]

        if message.command == constants.USER_COMMAND:
            if len(message.parameters) < 4:
                self.logger.info("ERROR")

            self.user_name = message.parameters[0]
            self.real_name = message.parameters[3]

        # user_name implies real_name is present
        if self.user_name and self.nick:
            self.is_registered = True
