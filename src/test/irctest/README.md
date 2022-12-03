## IRCTest

### Setup

The files here are to be used with the [irctest](https://github.com/progval/irctest) repo to run integration tests against Pyircd. The repo contains tests for many different specs of the IRC protocol. We have included a file and instructions to run tests that match our implementation below.

To get started, copy `pyircd_controller.py` to `irctest/irctest/controllers`. This will manage the setup and teardown process for the daemon between tests.

Furthermore, copy `pyproject.toml` to the `irctest`. Finally run `poetry install` in `irctest` to get the environment setup.

#### Additional Tests
Due to a lack of tests for certain core IRC functionality. We wrote some additional tests. These can be found in `additional_tests.py` and must be copied into `passing_tests.txt` after adding them into `irctest`.
Instructions for adding the tests into `irctest` can be found in `additional_tests.py`.

### Running Tests

To run the tests, first set an environment variable pointing to the root directory of `pyircd`, for example, `export PYIRCD_DIR=/home/me/pyircd/`.

Next copy over the names of the passing tests (present in this directory) into the root of the irctest directory, `cp passing_tests.txt irctest/`.

Finally run `pytest --controller irctest.controllers.pyircd_controller $(tr '\n' ' ' <passing_tests.txt) --verbose
` to run the tests.

### Debugging Tests

Sometimes during development a test may hang for various reasons. In this case, it's useful to see daemon output as the test executes. To do so, do as follows:
1. Run the server separately
2. Specify the host and port in env vars (we're going to use the external controller to run the daemon)
```
export IRCTEST_SERVER_PORT=6667
export IRCTEST_SERVER_HOSTNAME=localhost
```
3. Now run the tests like so:
`pytest --controller irctest.controllers.external_server $(tr '\n' ' ' <single.txt) --verbose` where `single.txt` contains the test(s) you want to run. It's recommended to run only a single test so that state created during one test does not affect state in the next (this is recommended only when using the external controller).
