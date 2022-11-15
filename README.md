## Setup Instructions
First, ensure you are using Python ^3.10.

This project uses `poetry` which is a wrapper around `pip` for dependency management. We also use pre commit hooks to ensure code consistency and best practices. To set up a development environment do as follows:

1. Install [poetry](https://python-poetry.org/docs/): `curl -sSL https://install.python-poetry.org | python3 -` (you may need to add it to your Path)
2. Run `make install`; this will install dependencies (none right now) and will configure pre-commit hooks for you by installing them to your `.git` directory.

Done! Let's run a test to ensure your dev environment is properly setup.

1. Run `touch test.py` in the root directory
2. Run `git add test.py && git commit`

You should see output indicating a bunch of checks running such as "Fix End of Files" with a green status bar saying Passed.
