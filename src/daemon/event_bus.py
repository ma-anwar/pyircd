import logging
from collections import defaultdict

from client import Client
from message import Message


class EventBus:
    def __init__(self):
        self.logger = logging.getLogger("Event Bus")
        self.clients = defaultdict(Client)

    def __handle_message(self, message: Message):
        self.logger.debug(message)
        client = self.__get_client(message)
        client.handle_message(message)
        # Take this out, it's just there to test we can send back to client
        message.key.data.out_buffer += b"Here is a response! \r\n"
        message.key.data.out_buffer += b" Here's another response \r\n"

    def dispatch(self, message: Message):
        self.__handle_message(message)

    def __get_client(self, message: Message):
        return self.clients[message.client_address]
