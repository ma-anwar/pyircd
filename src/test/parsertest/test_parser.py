"""Tests the parsing module (src/daemon/parser.py)"""
import pytest
import yaml
from message import Message
from message_bus import MessageBus
from parser import Parser


@pytest.fixture
def parser():
    """Returns a Parser instance"""
    event_bus = MessageBus()
    return Parser(event_bus.dispatch)


def tests_from_yaml(parser):
    # Currently just for first one, will modify the yaml and
    # loop through all of the valid tests we need.
    data = yaml.safe_load(open("src/test/parsertest/parser_tests.yaml").read())

    test = data["tests"][0]
    atoms = test["atoms"]
    matches = test["matches"]
    matches[0] = matches[0] + "\r\n"

    message = Message("localhost", "PARSE", matches[0].encode("utf-8"), "key")
    parsed_message = Message(
        "localhost",
        "HANDLE",
        matches[0].encode("utf-8"),
        "key",
        atoms.get("verb"),
        atoms.get("params"),
    )
    res = parser._parse_message(message)
    assert parsed_message == res
