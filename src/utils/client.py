
"""Tiny client implementation for quick testing; can be more robust"""
import socket

SERVER = '127.0.0.1'
PORT = 6667
NICKNAME = 'test_nickname'
CHANNEL = '#random'


class IRCConnection:
    """Class responsible for IRC server connection."""

    def __init__(self, username=NICKNAME, channel=CHANNEL, server=SERVER, port=PORT):
        """Initialize the configuration of our IRC connect"""
        self.username = username
        self.server = server
        self.port = port
        self.channel = channel
        self.connection = None

    def connect(self):
        """Connects to the server"""
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.server, self.port))

    def get_response(self):
        """Gets response from IRC server"""
        pass

    def send_cmd(self, cmd, message):
        """Sends IRC command to server"""
        pass

    def send_message(self, message):
        """Sends message to the channel"""
        pass

    def join_channel(self):
        """Joins channel"""
        pass


def main():
    """Temporary client flow for testing"""
    joined = False
    connection = IRCConnection(NICKNAME, CHANNEL)
    connection.connect()
    while not joined:
        # Based off of response (connection.get_reponse), act accordingly
        break

    # After joined == True, have a new while loop until we quit


if __name__ == "__main__":
    main()
