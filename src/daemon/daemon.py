import logging
import sys
from argparse import ArgumentParser, Namespace

import constants
import utils
from event_bus import EventBus
from parser import Parser
from server import Server


def parse_args() -> Namespace:
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


def main() -> None:
    args = parse_args()
    host, port = args.host, args.port

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    utils.print_logo()

    event_bus = EventBus()
    parser = Parser(event_bus.dispatch)
    Server(host, port, parser.dispatch)


if __name__ == "__main__":
    main()
