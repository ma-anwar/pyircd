"""Tiny client implementation for quick testing using Python IRC Library"""
import irc.client

SERVER = "127.0.0.1"
PORT = 6667
NICKNAME = "test_nickname"
CHANNEL = "#random"


def main():
    reactor = irc.client.Reactor()
    reactor.server().connect(SERVER, PORT, NICKNAME)


if __name__ == "__main__":
    main()
