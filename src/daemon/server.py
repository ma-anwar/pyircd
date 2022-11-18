import logging
import selectors
import socket
from selectors import SelectorKey
from types import SimpleNamespace

import constants
from message import Message


class Server:
    def __init__(self, host: str, port: int, dispatch: callable) -> None:
        self.selector = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.logger = logging.getLogger("Server")
        self.dispatch = dispatch
        self.__start_server()

    def __handle_new_client_connection(self, socket: socket.socket):
        client_connection, client_address = socket.accept()

        self.logger.info(f"Accepted connection from {client_address}")
        client_connection.setblocking(False)

        key = SimpleNamespace(
            address=client_address,
            in_buffer=b"",
            out_buffer=b"",
            is_server_socket=False,
        )

        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        self.selector.register(client_connection, events, data=key)

    def __has_irc_termination_delimiter(self, in_buffer: bytes) -> bool:
        index_of_delimiter = in_buffer.find(constants.IRC_TERMINATION_DELIMITER)
        return index_of_delimiter != constants.NOT_FOUND

    def __get_delimiter_position(self, in_buffer: bytes) -> int:
        index_of_delimiter = in_buffer.find(constants.IRC_TERMINATION_DELIMITER)
        return index_of_delimiter

    def __receive_and_buffer_data(self, key: SelectorKey):
        socket, address = key.fileobj, key.data.address

        received_data = socket.recv(constants.RECEIVE_LENGTH)
        self.logger.debug(
            f"Received the following data from {address}: {received_data}"
        )

        if received_data:
            # TODO: Enforce limit on buffer length to avoid memory overflow
            key.data.in_buffer += received_data
            if self.__has_irc_termination_delimiter(key.data.in_buffer):
                self.__dispatch_message_to_parser(key)

        # Empty receipt means we terminate
        else:
            self.logger.info(f"Closing connection to {address}")
            self.selector.unregister(socket)
            # TODO: Notify downstream
            socket.close()

    def __dispatch_message_to_parser(self, key: SelectorKey):
        address = key.data.address

        delimiter_index = self.__get_delimiter_position(key.data.in_buffer)

        irc_message = key.data.in_buffer[
            : delimiter_index + constants.DELIMITER_END_INDEX
        ]

        key.data.in_buffer = key.data.in_buffer[len(irc_message) :]

        message = Message(address, "PARSE", irc_message, key)
        self.dispatch(message)

    def __service_existing_connection(self, key: SelectorKey, event_mask: int):
        if event_mask & selectors.EVENT_READ:
            self.__receive_and_buffer_data(key)

        if event_mask & selectors.EVENT_WRITE and key.data.out_buffer:
            self.__send_response(key)

    def __get_message(self, key: SelectorKey):
        while delimiter_position := key.data.out_buffer.find(
            constants.IRC_TERMINATION_DELIMITER
        ):
            if delimiter_position == constants.NOT_FOUND:
                break

            message = key.data.out_buffer[
                : delimiter_position + constants.DELIMITER_END_INDEX
            ]
            key.data.out_buffer = key.data.out_buffer[len(message) :]
            yield (message)

    def __send_response(self, key: SelectorKey):
        socket = key.fileobj

        # Could have multiple messages in output buffer
        for message in self.__get_message(key):
            self.logger.debug(f"Sending message {message}")
            while message != constants.EMPTY_STRING:
                try:
                    sent = socket.send(message)
                    message = message[sent:]
                except ConnectionError as e:
                    self.logger.debug(f"Connection error {e}, deregistering socket")
                    self.selector.unregister(socket)
                    # TODO: Notify downstream
                    return

    def __start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Avoid "Address already in use" error
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((self.host, self.port))
        server_socket.listen()

        self.logger.info(f"Listening on {(self.host, self.port)}")

        server_socket.setblocking(False)

        # key will be registered alongside socket in selector
        # so we can access it whenever we access the socket
        key = SimpleNamespace(is_server_socket=True)

        # We are only interested in reading new cxn information fron server_socket
        self.selector.register(server_socket, selectors.EVENT_READ, data=key)
        self.__run_event_loop()

    def __run_event_loop(self):
        try:
            while True:
                active_socket = self.selector.select(timeout=None)

                for socket_data, event_mask in active_socket:

                    socket = socket_data.fileobj
                    connection_receieved_on_server_socket = (
                        socket_data.data.is_server_socket
                    )

                    if connection_receieved_on_server_socket:
                        self.__handle_new_client_connection(socket)
                    else:
                        self.__service_existing_connection(socket_data, event_mask)

        except Exception as e:
            self.logger.debug(f"Exception in event loop: {e}")
        finally:
            self.selector.close()
