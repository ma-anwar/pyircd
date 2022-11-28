"""This module is responsible for handling parsed messages sent by the parser"""
import logging
from typing import Callable

from client import Client
from message import Message


class MessageBus:
    """Class responsible for handling parsed messages."""

    def __init__(self):
        """Initialize map of address to client objects"""
        self._logger = logging.getLogger(__name__)
        self._clients = {}

    def _handle_message(self, message: Message):
        """Handle received message by forwarding it to client, WIP"""
        self._logger.debug(message)
        client = self._get_client(message)
        client.handle_message(message)

    def dispatch(self, message: Message):
        """Call handler on message, used by Parser"""
        self._handle_message(message)

    def _create_new_client(self, message: Message, unregister_callback: Callable):
        """Create new client instance"""
        return Client(message.client_address, message.key, unregister_callback)

    def _get_client(self, message: Message):
        """Return Client based on address
        If Client does not exist, generates a new Client instance
        """
        if message.client_address not in self._clients:
            unregister_callback = self._get_unregister_client_callback(
                message.client_address
            )
            new_client = self._create_new_client(message, unregister_callback)
            self._clients[new_client.address] = new_client
            return new_client

        return self._clients[message.client_address]

    def _get_unregister_client_callback(self, client_address: tuple):
        """Callback passed to client to unregister from message_bus on disconnect"""

        def unregister_self():
            self._clients.pop(client_address)

        return unregister_self
