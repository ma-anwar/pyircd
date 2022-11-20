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

    def run(self, host="127.0.0.1", port="6667") -> None:
        """Run the pyircd server"""
        self.proc = subprocess.run("poetry", f"run python src/daemon/daemon.py --host {host} --port {port}")


def get_irctest_controller_class() -> Type[PyIrcdController]:
    return PyIrcdController
