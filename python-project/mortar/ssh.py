from mortar import process


class SSH:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

    def scp_to(self, local, remote):
        cmd = ['scp', '-P', self.port, local, f'{self.host}:/{remote}']

        result = process.run(cmd)

        return result

    def scp_from(self, remote, local):
        cmd = ['scp', '-P', self.port, f'{self.host}:/{remote}', local]

        result = process.run(cmd)

        return result

    def run(self, command):
        ssh_command = ['ssh', '-p', self.port, self.host] + command

        return process.run(ssh_command)
