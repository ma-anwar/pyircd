import constants

class Channel:
    def __init__(self, channel_name, channel_type, channel_topic):
        for x in constants.FORBIDDEN_CHANNELNAME_CHARS:
            assert x not in channel_name, "Please avoid using invalid characters in the channel name!"
        self.channel_name = channel_name
        self.channel_prefix = constants.CHANNEL_TYPES[channel_type]
        self.channel_topic = channel_topic
        self.clients = {}   # Key=<Address>, Value=send_message_callback
                            # <Address> = ("client_address", "client_port")

    def register(self, address: tuple, send_msg: callable):
        """Called as an instance method
        Registers a client and returns methods for
        broadcasting and unregistering"""
        if address not in self.clients:
            self.clients[address] = send_msg
        broadcast = self.get_broadcast(address)
        unregister = self.get_unregister(address)
        send_msg(f"You have joined the channel: {self.channel_name}")
        return broadcast, unregister

    def get_unregister(self, address: tuple):
        """Returns a callable to unregister a client form the channel"""

        def unregister():
            if address in self.clients:
                self.clients.pop(address)

        return unregister

    def get_broadcast(self, address: tuple):
        """Returns a callable for the client to broadcast
        a message to all clients on the channel but themselves"""

        def broadcast(message: str):
            for client, send_msg in self.clients.items():
                if not (client[0] == address[0] and client[1] == address[1]):
                    send_msg(message)

        return broadcast

    # https://modern.ircdocs.horse/#topic-message
    def change_topic(self, new_topic):
        self.channel_topic = new_topic
        for send_msg in self.clients.values():  # Announce topic change to all clients
            send_msg(constants.IRC_REPLIES.RPL_TOPIC, f":{new_topic}", include_nick=False)