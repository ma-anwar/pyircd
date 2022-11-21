"""This module is responsible for handling parsed messages sent by the parser"""
import logging
from collections import defaultdict

from client import Client
from message import Message


class EventBus:
    """Class responsible for handling parsed messages."""

    def __init__(self):
        """Initialize map of address to client objects"""
        self.logger = logging.getLogger("Event Bus")
        self.clients = defaultdict(Client)

    def _handle_message(self, message: Message):
        """Handle received message by forwarding it to client, WIP"""
        self.logger.debug(message)
        client = self._get_client(message)
        client.handle_message(message)
        # Take this out, it's just there to test we can send back to client
        message.key.data.out_buffer += b"Here is a response! \r\n"
        message.key.data.out_buffer += b" Here's another response \r\n"

    def dispatch(self, message: Message):
        """Call handler on message, used by Parser"""
        self._handle_message(message)

    def _get_client(self, message: Message):
        """Return Client based on address
        If Client does not exist, generates a new Client instance
        """
        return self.clients[message.client_address]
