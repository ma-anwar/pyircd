"""Holds the Message class that is passed around by different parts of the server"""
from dataclasses import dataclass, field
from selectors import SelectorKey
from typing import List


@dataclass
class Message:
    """This class encapsulates information about IRC messages or events.

    Messages are passed to different handlers throughout the program.
    """

    # Address sent just in case we need it in future
    client_address: tuple
    # Action because we may not want a downstream handler to handle message
    # Possible Ex: delete action to delete a client
    action: str
    # Command and parameters should be parsed from message according to docs
    message: str
    key: SelectorKey = field(repr=False)
    command: str = ""
    parameters: List[str] = field(default_factory=list)
