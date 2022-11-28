"""Tests the parsing module (src/daemon/parser.py)"""
import pytest
import yaml
from message import Message
from message_bus import MessageBus
from parser import Parser


def load_data():
    res = []
    data = yaml.safe_load(open("src/test/parser_tests/parser_tests.yaml").read())
    tests = data["tests"]
    for test in tests:
        atom = test["atoms"]
        raw_message = test["message"][0].encode("utf-8") + b"\r\n"
        message = Message("localhost", "PARSE", raw_message, "key")
        params = atom.get("params") if atom.get("params") else []
        command = atom.get("command") if atom.get("command") else ""
        parsed_message = Message(
            "localhost",
            "HANDLE",
            raw_message,
            "key",
            command,
            params,
        )
        res.append((message, parsed_message))
    return res


DATA = load_data()


@pytest.fixture
def parser():
    """Returns a Parser instance"""
    event_bus = MessageBus()
    return Parser(event_bus.dispatch)


@pytest.mark.parametrize("message, parsed_message", DATA)
def tests_from_yaml(parser, message, parsed_message):
    for message, parsed_message in DATA:
        assert parsed_message == parser._parse_message(message)
