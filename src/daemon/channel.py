import constants


class Channel:
    def __init__(self, channel_name):
        self._channel_name = channel_name
        self._channel_topic = ""
        self._client_nicks = {}  # Key = <Address>, Value = nickname
        self._clients = {}  # Key = <Address>, Value = send_message_callback
        # <Address> = ("client_address", "client_port")

    def register(self, address: tuple, send_msg: callable, nickname: str):
        """Called as an instance method
        Registers a client and returns the following:
            - broadcast method
            - channel topic
            - topic reply code
            - list of clients currently in channel
        Reasoning: https://modern.ircdocs.horse/#join-message
        """

        broadcast = self.get_broadcast(address)

        if address not in self._clients:
            self._clients[address] = send_msg
            self._client_nicks[address] = nickname

        else:  # Client already on channel, return None
            return None

        return broadcast

    def unregister(self, address: tuple):
        """Instance method for unregistering a client from the channel"""
        if address in self._clients:
            self._clients.pop(address)
            self._client_nicks.pop(address)

    def get_broadcast(self, address: tuple):
        """Returns a callable for the client to broadcast
        a message to all clients on the channel but themselves"""

        def broadcast(*args, **kwargs):
            for client_address, send_msg in self._clients.items():
                if not (client_address == address):
                    send_msg(*args, **kwargs)

        return broadcast

    # https://modern.ircdocs.horse/#topic-message
    def change_topic(self, new_topic):
        self._channel_topic = new_topic
        if new_topic == "":
            reply_code = constants.IRC_REPLIES.NOTOPIC
        else:
            reply_code = constants.IRC_REPLIES.TOPIC

        for send_msg in self._clients.values():  # Announce topic change to all clients
            send_msg(
                numeric=reply_code,
                message=f"New topic is: {new_topic}",
                include_nick=False,
            )

    def get_members(self):
        return [x for x in self._client_nicks.values()]

    def get_topic(self):
        return self._channel_topic

    def get_client_addresses(self):
        return [x for x in self._clients.keys()]

    def get_channel_name(self):
        return self._channel_name
