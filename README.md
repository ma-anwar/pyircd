## Setup Instructions
First, ensure you are using Python ^3.10.

This project uses `poetry` which is a wrapper around `pip` for dependency management. We also use pre commit hooks to ensure code consistency and best practices. To set up a development environment do as follows:

1. Install [poetry](https://python-poetry.org/docs/): `curl -sSL https://install.python-poetry.org | python3 -` (you may need to add it to your Path)
2. Run `poetry install` from the root directory to install all dependencies
3. Setup pre-commit checks by running: `poetry run pre-commit install`, this will take the pre-commit hooks configured in `.pre-commit-config.yaml` and install them as hooks in your `.git` directory.

Done! Let's run a test to ensure your dev environment is properly setup.

1. Run `touch test.py` in the root directory
2. Run `git add test.py && git commit`

You should see output indicating a bunch of checks running such as "Fix End of Files" with a green status bar saying Passed.

If you would like to run the formatter or linter manually, you can run them with the Makefile using `make format` or `make lint`. Additionally you can configure your editor to run these commands on save.
