"""Server module is responsible for managing client connections"""
import logging
import selectors
import socket
import traceback
from selectors import SelectorKey
from types import SimpleNamespace

import constants
from message import Message


class Server:
    """Server class responsible for handling socket connections with client

    Server will buffer receievd data until a full IRC delimited message is received.
    It will then dispatch the message as a Message to the parser.

    Server also continously checks if in_buffer for any socket has data.
    If so it will write such data to client.
    """

    def __init__(self, host: str, port: int, dispatch: callable) -> None:
        """Start the server"""
        self._selector = selectors.DefaultSelector()
        self._host = host
        self._port = port
        self._logger = logging.getLogger(__name__)
        self._dispatch = dispatch
        self._start_server()

    def _handle_new_client_connection(self, socket: socket.socket):
        """On client connection, create state and register it with the selector"""
        client_connection, client_address = socket.accept()

        self._logger.info(f"Accepted connection from {client_address}")
        client_connection.setblocking(False)

        key = SimpleNamespace(
            address=client_address,
            in_buffer=b"",
            out_buffer=b"",
            is_server_socket=False,
        )

        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        self._selector.register(client_connection, events, data=key)

    def _has_irc_termination_delimiter(self, in_buffer: bytes) -> bool:
        """Return true if buffer is delimited by \r\n"""
        index_of_delimiter = in_buffer.find(constants.IRC_TERMINATION_DELIMITER)
        return index_of_delimiter != constants.NOT_FOUND

    def _get_delimiter_position(self, in_buffer: bytes) -> int:
        """Return index of \r\n delimiter"""
        index_of_delimiter = in_buffer.find(constants.IRC_TERMINATION_DELIMITER)
        return index_of_delimiter

    def _receive_and_buffer_data(self, key: SelectorKey):
        """Receive data and call dispatcher if it has IRC delimiter.

        If no data received, close socket
        """
        socket, address = key.fileobj, key.data.address

        try:
            received_data = socket.recv(constants.RECEIVE_LENGTH)
        except ConnectionResetError:
            return

        self._logger.debug(
            f"Received the following data from {address}: {received_data}"
        )

        if received_data:
            # TODO: Enforce limit on buffer length to avoid memory overflow
            key.data.in_buffer += received_data
            if self._has_irc_termination_delimiter(key.data.in_buffer):
                self._dispatch_message_to_parser(key)

        # Empty receipt means we terminate
        else:
            self._logger.info(f"Closing connection to {address}")
            self._selector.unregister(socket)
            # TODO: Notify downstream
            socket.close()

    def _dispatch_message_to_parser(self, key: SelectorKey):
        """Retrieve data from buffer, build Message and dispatch to parser"""
        address = key.data.address

        for message in self._get_message_from_in_buffer(key):
            delimiter_index = self._get_delimiter_position(key.data.in_buffer)

            irc_message = key.data.in_buffer[
                : delimiter_index + constants.DELIMITER_END_OFFSET
            ]

            key.data.in_buffer = key.data.in_buffer[len(irc_message) :]

            message = Message(address, "PARSE", irc_message, key)
            self._dispatch(message)

    def _service_existing_connection(self, key: SelectorKey, event_mask: int):
        """Handle read or write event on existing connection"""
        if event_mask & selectors.EVENT_READ:
            self._receive_and_buffer_data(key)

        if event_mask & selectors.EVENT_WRITE and key.data.out_buffer:
            self._send_response(key)

    def _get_message_from_in_buffer(self, key: SelectorKey):
        """Generator to retrieve all IRC delimited strings from in_buffer"""
        while delimiter_position := key.data.in_buffer.find(
            constants.IRC_TERMINATION_DELIMITER
        ):
            if delimiter_position == constants.NOT_FOUND:
                break

            message = key.data.in_buffer[
                : delimiter_position + constants.DELIMITER_END_OFFSET
            ]
            key.data.out_buffer = key.data.in_buffer[len(message) :]
            yield (message)

    def _get_message(self, key: SelectorKey):
        """Generator to retrieve all IRC delimited strings from out_buffer"""
        while delimiter_position := key.data.out_buffer.find(
            constants.IRC_TERMINATION_DELIMITER
        ):
            if delimiter_position == constants.NOT_FOUND:
                break

            message = key.data.out_buffer[
                : delimiter_position + constants.DELIMITER_END_OFFSET
            ]
            key.data.out_buffer = key.data.out_buffer[len(message) :]
            yield (message)

    def _send_response(self, key: SelectorKey):
        """Send contents of out_buffer to client"""
        socket = key.fileobj

        # Could have multiple messages in output buffer
        for message in self._get_message(key):
            self._logger.debug(f"Sending message {message}")
            while message != constants.EMPTY_STRING:
                try:
                    num_bytes_sent = socket.send(message)
                    message = message[num_bytes_sent:]
                except ConnectionError as e:
                    self._logger.debug(f"Connection error {e}, deregistering socket")
                    self._selector.unregister(socket)
                    # TODO: Notify downstream
                    return

    def _start_server(self):
        """Initialize server socket and call event_loop initialization"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Avoid "Address already in use" error
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((self._host, self._port))
        server_socket.listen()

        self._logger.info(f"Listening on {(self._host, self._port)}")

        server_socket.setblocking(False)

        # key will be registered alongside socket in selector
        # so we can access it whenever we access the socket
        key = SimpleNamespace(is_server_socket=True)

        # We are only interested in reading new cxn information fron server_socket
        self._selector.register(server_socket, selectors.EVENT_READ, data=key)
        self._run_event_loop()

    def _run_event_loop(self):
        """Wait for sockets to register events and handle appropriately"""
        try:
            while True:
                active_socket = self._selector.select(timeout=None)

                for socket_data, event_mask in active_socket:

                    socket = socket_data.fileobj
                    connection_receieved_on_server_socket = (
                        socket_data.data.is_server_socket
                    )

                    if connection_receieved_on_server_socket:
                        self._handle_new_client_connection(socket)
                    else:
                        self._service_existing_connection(socket_data, event_mask)

        except Exception as e:
            self._logger.debug(f"Exception in event loop: {e}")
            traceback.print_exc()
        finally:
            self._selector.close()
