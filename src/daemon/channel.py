import constants

class Channel:
    def __init__(self, channel_name, channel_type, channel_topic, client_limit):
        for x in constants.FORBIDDEN_CHANNELNAME_CHARS:
            assert x not in channel_name, "Please avoid using invalid \
            characters in the channel name!"
        self.channel_name = channel_name
        self.channel_prefix = constants.CHANNEL_TYPES[channel_type]
        self.channel_topic = channel_topic
        self.client_limit = client_limit
        self.banned_clients = {}    # Same key-value format as clients
        self.clients = {}           # Key=<Address>, Value=send_message_callback
                                    # <Address> = ("client_address", "client_port")

    def register(self, address: tuple, send_msg: callable):
        """Called as an instance method
        Registers a client and returns the following:
            - broadcast method
            - channel topic
            - topic reply code
            - list of clients currently in channel
        Reasoning: https://modern.ircdocs.horse/#join-message
        If client is banned, send error message and return"""
        
        if address in self.banned_clients:
            send_msg(numeric=constants.IRC_ERRORS.ERR_BANNEDFROMCHAN, 
                message=":Cannot join channel (+b)", include_nick=False)
            return None, None
        if len(self.clients) == self.client_limit:
            send_msg(numeric=constants.IRC_ERRORS.ERR_CHANNELISFULL,
                message=":Cannot join channel (+l)", include_nick=False)
        if address not in self.clients:
            self.clients[address] = send_msg
        broadcast = self.get_broadcast(address)
        return broadcast, self.channel_topic, self.clients.keys()

    def unregister(self, address: tuple):
        """Instance method for unregistering a client from the channel"""
        if address in self.clients:
            self.clients.pop(address)

    def get_broadcast(self, address: tuple):
        """Returns a callable for the client to broadcast
        a message to all clients on the channel but themselves"""
        def broadcast(*args, **kwargs):
            for client, send_msg in self.clients.items():
                if not (client[0] == address[0] and client[1] == address[1]):
                    send_msg(*args, **kwargs)
        return broadcast

    # https://modern.ircdocs.horse/#topic-message
    def change_topic(self, new_topic):
        self.channel_topic = new_topic
        if new_topic == "":
            reply_code = constants.IRC_REPLIES.RPL_NOTOPIC
        else:
            reply_code = constants.IRC_REPLIES.RPL_TOPIC

        for send_msg in self.clients.values():  # Announce topic change to all clients
            send_msg(numeric=reply_code, message=f"New topic is: {new_topic}", include_nick=False)

    def ban_user(self, address:tuple, send_msg: callable):
        if address in self.clients:
            self.clients.pop(address)
        if address not in self.banned_clients:
            self.banned_clients[address] = send_msg
