"""These tests are to be used as part of the irctest repo to test functionality in our server

They were written because irctest lacked tests for certain functionality that we implemented.
Instructions on adding the tests to irctest are in each relevant docstring.
These are not included in passing_tests by default.
"""

# flake8: noqa


@cases.mark_specifications("RFC1459", "RFC2812")
def testPrivmsgToUser(self):
    """Add to messages.py

    Reference by:
    irctest/server_tests/messages.py::PrivmsgTestCase::testPrivmsgToUser
    """
    self.connectClient("foo")
    self.connectClient("bar")
    self.sendLine(1, "PRIVMSG bar :hey there!")
    pms = [msg for msg in self.getMessages(2) if msg.command == "PRIVMSG"]
    self.assertEqual(len(pms), 1)
    self.assertMessageMatch(pms[0], command="PRIVMSG", params=["bar", "hey there!"])


@cases.mark_specifications("RFC1459", "RFC2812")
def testPrivmsgNonexistentUser(self):
    """Add to messages.py

    Reference by:
    irctest/server_tests/messages.py::PrivmsgTestCase::testPrivmsgNonexistentUser
    """
    self.connectClient("foo")
    self.sendLine(1, "PRIVMSG bar :hey there!")
    msg = self.getMessage(1)
    self.assertIn(msg.command, ("401"))
