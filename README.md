    _______________.___.______________________ ________
    \______   \__  |   |   \______   \_   ___ \\______ \
     |     ___//   |   |   ||       _/    \  \/ |    |  \
     |    |    \____   |   ||    |   \     \____|    `   \
     |____|    / ______|___||____|_  /\______  /_______  /
               \/                  \/        \/        \/

## Video Demo And Design
Check out a demo of our daemon [here](https://www.youtube.com/watch?v=x1UCsyApBdU).

For details about the design of our project, see `Design_and_Implementation.pdf` in the root of our repo.

## Setup Instructions
First, ensure you are using Python ^3.10.

This project uses `poetry` which is a wrapper around `pip` for dependency management. We also use pre commit hooks to ensure code consistency and best practices. To set up a development environment do as follows:

1. Install [poetry](https://python-poetry.org/docs/): `curl -sSL https://install.python-poetry.org | python3 -` (you may need to add it to your Path)
2. Run `make install`; this will install dependencies and will configure pre-commit hooks for you by installing them to your `.git` directory.

Done! Let's run a test to ensure your dev environment is properly setup.

1. Run `touch test.py` in the root directory
2. Run `git add test.py && git commit`

You should see output indicating a bunch of checks running such as "Fix End of Files" with a green status bar saying Passed.

## Running the Daemon

To run the daemon, `poetry run python src/daemon/daemon.py`. The daemon expects to be run from the root directory in order to find the logging config.

## Testing

The daemon can be tested using the integration tests in `src/test/integration_tests/`.
The parser can be tested by running the tests in `src/test/parser_tests/`.
Each test directory contains further documentation on the nature of the tests and how to run them.

Furthermore, any off the shelf IRC client should be able to connect and interact with the daemon. We specifically tested with [Weechat](https://weechat.org/) and [pidgin](https://pidgin.im/).
Detailed instructions on how to test with an IRC client are present in our `Design_and_Implementation.pdf` under the heading "Testing with a Client".

## Configuring Logs
Logging can be configured to offer different levels of verbosity or different formats. This can be done by modifying `logging_config.yml`.
