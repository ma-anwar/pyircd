"""This module sets up the event bus, parser and starts the server"""
import logging
import logging.config
from argparse import ArgumentParser, Namespace

import config
import constants
import utils
import yaml
from message_bus import MessageBus
from parser import Parser
from server import Server


def parse_args() -> Namespace:
    """Parse command line arguments"""
    parser = ArgumentParser("Python IRC Daemon")

    parser.add_argument(
        "--host",
        type=str,
        required=False,
        help="Host address to run server on",
        default=constants.LOCAL_HOST,
    )
    parser.add_argument(
        "--port",
        required=False,
        type=int,
        help="Port to listen on",
        default=constants.DEFAULT_PORT,
    )
    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="Name of server",
        default="pyircd",
    )
    return parser.parse_args()


def setup_logging():
    with open("logging_config.yml", "rt") as f:
        config = yaml.safe_load(f.read())

    logging.config.dictConfig(config)


def main() -> None:
    """Get parsed commandline arguments, setup event_bus, parser and start server"""
    setup_logging()

    args = parse_args()
    host, port, name = args.host, args.port, args.name

    utils.print_logo()

    config.init(name)

    message_bus = MessageBus()
    parser = Parser(message_bus.dispatch)
    Server(host, port, parser.dispatch)


if __name__ == "__main__":
    main()
