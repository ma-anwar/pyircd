import os
import subprocess
from typing import Tuple, Type

from irctest.basecontrollers import BaseServerController


class PyIrcdController(BaseServerController):
    """Controller for running our pyircd server"""

    software_name = "pyircd-controller"
    supported_sasl_mechanisms = set(
        os.environ.get("IRCTEST_SERVER_SASL_MECHS", "").split()
    )

    def kill_proc(self) -> None:
        """Kills the process"""
        super().kill_proc()

    def get_hostname_and_port(self) -> Tuple[str, int]:
        """Returns hostname and port"""
        hostname = os.environ.get("IRCTEST_SERVER_HOSTNAME")
        port = os.environ.get("IRCTEST_SERVER_PORT")
        if not hostname or not port:
            raise RuntimeError(
                "Please set IRCTEST_SERVER_HOSTNAME and IRCTEST_SERVER_PORT."
            )
        return (hostname, int(port))

    def run(self, host: str, port: str) -> None:
        """Run the pyircd server"""
        assert type(host) in [str, int], "hostname must be either str or int"
        assert type(port) in [str, int], "port must be either str or int"
        host, port = int(host), int(port)

        subprocess.run("poetry", "run python ~/pyircd/src/daemon/daemon.py")


def get_irctest_controller_class() -> Type[PyIrcdController]:
    return PyIrcdController
