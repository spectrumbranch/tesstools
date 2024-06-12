from enum import Enum, auto

from mortar import process


class Command(Enum):
    SSH = auto()
    SCP = auto()


class SSH:
    def __init__(self, host=None, port=None) -> None:
        self.host = host
        self.port = port

    def scp_to(self, local, remote):
        args = self._build_args(Command.SCP, self.port)

        cmd = ['scp'] + args + [local, f'{self.host}:/{remote}']

        result = process.run(cmd)

        return result

    def scp_from(self, remote, local):
        args = self._build_args(Command.SCP, self.port)

        cmd = ['scp'] + args + [f'{self.host}:/{remote}', local]

        result = process.run(cmd)

        return result

    def run(self, command):
        args = self._build_args(Command.SSH, self.port)

        ssh_command = ['ssh'] + args + [self.host] + command

        return process.run(ssh_command)

    @staticmethod
    def _build_args(command, port):
        args = []

        if port is not None:
            if command == Command.SSH:
                args.append('-p')
            elif command == Command.SCP:
                args.append('-P')
            else:
                raise Exception()

            args.append(str(port))

        return args
