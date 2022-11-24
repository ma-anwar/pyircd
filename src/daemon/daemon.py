"""This module sets up the event bus, parser and starts the server"""
import logging
import logging.config
from argparse import ArgumentParser, Namespace

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
        help="Seed to be used",
        default=constants.LOCAL_HOST,
    )
    parser.add_argument(
        "--port",
        required=False,
        type=int,
        help="Number of hosts to simulate",
        default=constants.DEFAULT_PORT,
    )
    parser.add_argument(
        "--debug",
        required=False,
        help="Print state of each host per iteration",
        action="store_true",
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
    host, port = args.host, args.port

    utils.print_logo()

    message_bus = MessageBus()
    parser = Parser(message_bus.dispatch)
    Server(host, port, parser.dispatch)


if __name__ == "__main__":
    main()
