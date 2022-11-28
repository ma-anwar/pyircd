class Channel:
    # This class is strictly a broadcast medium :)

    clients = {}    # Key=Address, Value=send_message

    