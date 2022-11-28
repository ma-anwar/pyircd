class Channel:
    # This class is strictly a broadcast medium :)

    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.clients = {}   # Key=<Address>, Value=send_message_callback
                            # <Address> = ("client_address", "client_port")

    def register(self, address:tuple, send_msg: callable):
        """Called as an instance method
        Registers a client and returns methods for
        broadcasting and unregistering"""
        if address not in self.clients:
            self.clients[address] = send_msg
        broadcast = self.get_broadcast(address)
        unregister = self.get_unregister(address)
        send_msg(f"You have joined the channel: {self.channel_name}")
        return broadcast, unregister

    def get_unregister(self, address:tuple):
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
    