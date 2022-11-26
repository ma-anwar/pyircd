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
    port = 6667
    hostname = "localhost"

    def kill_proc(self) -> None:
        """Kills the process"""
        super().kill_proc()

    def get_hostname_and_port(self) -> Tuple[str, int]:
        """Returns hostname and port"""
        return (self.hostname, int(self.port))

    def run(
        self,
        host="127.0.0.1",
        port="6667",
        password=None,
        valid_metadata_keys=None,
        invalid_metadata_keys=None,
        ssl=None,
        run_services=None,
        faketime=None,
    ) -> None:
        """Run the pyircd server"""
        pyircd_dir = os.environ.get("PYIRCD_DIR")

        if not pyircd_dir:
            raise RuntimeError("Please set PYIRCD_DIR to the root of the pyircd repo")

        daemon = pyircd_dir + "src/daemon/daemon.py"

        os.chdir(pyircd_dir)

        run_daemon_command = f"poetry run python {daemon} --host {host} --port {port}"

        self.proc = subprocess.Popen(run_daemon_command.split())


def get_irctest_controller_class() -> Type[PyIrcdController]:
    return PyIrcdController
