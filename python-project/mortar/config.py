from dataclasses import dataclass, field
import os
from os.path import exists
from typing import Optional

import tomlkit as toml
from tomlkit.items import Table

import mortar.log as log


class BaseConfig:
    """ Build configuration file. """

    def init_from_file(self, path: str) -> None:
        with open(path, 'r') as fi:
            self.config = toml.parse(fi.read())

    @classmethod
    def from_file(cls, path: str) -> 'BaseConfig':
        """ Parse the configuration from an existing file. """

        ctx = cls()
        ctx.init_from_file(path)

        return ctx

    def write(self, path: str) -> None:
        """ Write the configuration to a file. """

        with open(path, 'w') as fi:
            fi.write(toml.dumps(self.config))

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value


@dataclass
class SSH:
    use_ssh: bool = False
    host: Optional[str] = None
    port: Optional[int] = 22


@dataclass
class Config(BaseConfig):
    data: Optional[str] = None

    log_level: str = 'WARNING'
    verbose: int = 0
    dry_run: Optional[bool] = None

    ssh: SSH = field(default_factory=SSH)

    def __post_init__(self) -> None:
        """ Initialize the configuration file with arguments. """

        super().__init__()

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """ Parse the configuration from an existing file. """

        with open(path, 'r') as fi:
            config = toml.parse(fi.read())

        if not isinstance(config['data'], str):
            raise Exception('str is expected.')

        if 'log_level' not in config:
            log_level = 'WARNING'
        elif not isinstance(config['log_level'], str):
            raise Exception('str is expected.')
        else:
            log_level = config['log_level']

        if not isinstance(config['ssh'], Table):
            raise Exception('Table is expected.')
        else:
            ssh = config['ssh']

            ctx = cls(
                data=config['data'],
                log_level=log_level,
                ssh=SSH(
                    host=ssh.get('host'),
                    port=ssh.get('port')
                )
            )

            if isinstance(ssh['use_ssh'], bool):
                ctx.ssh.use_ssh = ssh['use_ssh']

        return ctx

    def write(self, path: str) -> None:
        """ Write the configuration to a file. """

        self.config = toml.document()

        '''
        build = toml.table()

        if self.source_dir is not None:
            build.add('source_dir', self.source_dir)
        if self.build_dir is not None:
            build.add('build_dir', self.build_dir)
        if self.dry_run is not None:
            build.add('dry_run', self.dry_run)

        build.add('log_level', self.log_level)
        build.add('verbose', self.verbose)

        self.config.add('build', build)
        '''

        super().write(path)


_xdg_config_home = f"{os.environ['HOME']}/.config"
_config_dir = f'{_xdg_config_home}/mortar'

_config_path = f'{_config_dir}/config.toml'

if exists(_config_path):
    config = Config.from_file(_config_path)

    log.set_level(config.log_level)
else:
    config = Config()
