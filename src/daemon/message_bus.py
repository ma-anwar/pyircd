"""This module is responsible for handling parsed messages sent by the parser"""
import logging

from client import Client
from message import Message


class MessageBus:
    """Class responsible for handling parsed messages."""

    def __init__(self):
        """Initialize map of address to client objects"""
        self._logger = logging.getLogger(__name__)

    def _handle_message(self, message: Message):
        """Handle received message by forwarding it to client"""
        self._logger.debug(message)
        client = self._get_client(message)
        client.handle_message(message)

    def dispatch(self, message: Message):
        """Call handler on message, used by Parser"""
        self._handle_message(message)

    def _create_new_client(self, message: Message):
        """Create new client instance"""
        return Client(message.client_address, message.key)

    def _get_client(self, message: Message):
        """Return Client based on address
        If Client does not exist, generates a new Client instance
        """
        if message.client_address not in Client.clients:
            new_client = self._create_new_client(message)
            return new_client

        return Client.clients[message.client_address]
