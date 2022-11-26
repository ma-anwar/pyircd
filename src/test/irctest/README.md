## IRCTest

### Setup

The files here are to be used with the (irctest)[https://github.com/progval/irctest] repo to run integration tests against Pyircd.

To get started, copy `pyircd_controller.py` to `irctest/irctest/controllers`. This will manage the setup and teardown process for the daemon between tests.

Furthermore, copy `pyproject.toml` to the `irctest`. Finally run `poetry install` in `irctest` to get the environment setup.

### Running Tests

To run the tests, first set an environment variable pointing to the root directory of `pyircd`, for example, `export PYIRCD_DIR=/home/me/pyircd/`.

A selection of tests can then be run with a command such as, `pytest --controller irctest.controllers.pyircd_controller  -k 'not Ergo and not deprecated and not strict and connection_registration' --verbose`.
