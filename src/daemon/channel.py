import constants


class Channel:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.channel_topic = ""
        self.client_nicks = {}  # Key = <Address>, Value = nickname
        self.clients = {}  # Key = <Address>, Value = send_message_callback
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
        other_members = [x for x in self.client_nicks.values()]

        if address not in self.clients:
            self.clients[address] = send_msg
            self.client_nicks[address] = nickname
        else:
            send_msg(
                numeric=constants.IRC_ERRORS.USERONCHANNEL,
                message=f"{self.channel_name} :is already on channel",
                include_nick=True,
            )
            return
        return broadcast, self.channel_topic, other_members

    def unregister(self, address: tuple):
        """Instance method for unregistering a client from the channel"""
        if address in self.clients:
            self.clients.pop(address)
            self.client_nicks.pop(address)

    def get_broadcast(self, address: tuple):
        """Returns a callable for the client to broadcast
        a message to all clients on the channel but themselves"""

        def broadcast(*args, **kwargs):
            for client_address, send_msg in self.clients.items():
                if not (client_address == address):
                    send_msg(*args, **kwargs)

        return broadcast

    # https://modern.ircdocs.horse/#topic-message
    def change_topic(self, new_topic):
        self.channel_topic = new_topic
        if new_topic == "":
            reply_code = constants.IRC_REPLIES.NOTOPIC
        else:
            reply_code = constants.IRC_REPLIES.TOPIC

        for send_msg in self.clients.values():  # Announce topic change to all clients
            send_msg(
                numeric=reply_code,
                message=f"New topic is: {new_topic}",
                include_nick=False,
            )
