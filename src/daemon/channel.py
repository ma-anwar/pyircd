class Channel:
    # This class is strictly a broadcast medium :)

    clients = {}    # Key=<Address>, Value=send_message_callback
                    # <Address> = ("client_address", "client_port")

    def announce_user_join_or_leave(self, address: tuple, join: int):
        if join:
            joined_or_left = "joined"
        else:
            self.clients.pop(address)
            joined_or_left = "left"
        message = f"{address[0]}:{address[1]} has {joined_or_left} the channel!"
        
        broadcast = self.get_broadcast_method(address)
        broadcast(message)

    def get_broadcast_method(self, address: tuple):
        # Get method to broadcast to all clients except for address
        def broadcast(message: str):
            for client, send_msg in self.clients.items():
                if client[0] != address[0] and client[1] != address[1]:
                    send_msg(message)
        return broadcast
    
    