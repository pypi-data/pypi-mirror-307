"""Pyenvs depencencies:
Formatter definitions.

Supported formatters:
- conda
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

from multienv.pyenvs_deps_input_std import Configuration
from multienv.pyenvs_deps_output_conda import CondaEnvironment


@dataclass(frozen=True)
class _CondaConfiguration:
    """The specific conda configuration model."""

    default_environment: str | None
    strict_environment: str | None
    file_pattern: str
    encoding: str
    channels: list[str] | None
    pip: list[str] | None

    @staticmethod
    def from_configuration(formatter: dict | str):
        """Builds a conda configuration object form a dict or a default one form a string"""

        if isinstance(formatter, str):
            return _DEFAULT_CONDA_CONFIGURATION

        body = formatter[Formatters.CONDA.value.name]

        return _CondaConfiguration(
            default_environment=body['default_environment'] if 'default_environment' in body
            else _DEFAULT_CONDA_CONFIGURATION.default_environment,
            strict_environment=body['strict_environment'] if 'strict_environment' in body
            else _DEFAULT_CONDA_CONFIGURATION.strict_environment,
            file_pattern=body['file_pattern'] if 'file_pattern' in body else _DEFAULT_CONDA_CONFIGURATION.file_pattern,
            encoding=body['encoding'] if 'encoding' in body else _DEFAULT_CONDA_CONFIGURATION.encoding,
            channels=body['channels'] if 'channels' in body else _DEFAULT_CONDA_CONFIGURATION.channels,
            pip=body['pip'] if 'pip' in body else _DEFAULT_CONDA_CONFIGURATION.pip
        )

_DEFAULT_CONDA_CONFIGURATION = _CondaConfiguration(
    default_environment=None,
    strict_environment=None,
    file_pattern='environment',
    encoding='utf-8',
    channels=None,
    pip=None
)

def _conda_mapper(conf: Configuration, formatter_conf: _CondaConfiguration) -> list[CondaEnvironment]:
    """Writes a configuration as conda configuration environment files."""

    environments = conf.effective_environments()

    envs: list[CondaEnvironment] = []

    # default environment includes all dependencies
    if formatter_conf.default_environment:
        envs.append(CondaEnvironment.from_configuration(name=formatter_conf.default_environment,
                                                        channels=formatter_conf.channels,
                                                        pip=formatter_conf.pip,
                                                        configuration=conf))

    # strict environment excludes all dependencies specific to an environment
    if formatter_conf.strict_environment:
        envs.append(CondaEnvironment.from_dependencies(name=formatter_conf.strict_environment,
                                                       channels=formatter_conf.channels,
                                                       pip=formatter_conf.pip,
                                                       dependencies=conf.strict_dependencies()))

    for e in environments:
        envs.append(CondaEnvironment.from_dependencies(name=e,
                                                       channels=formatter_conf.channels,
                                                       pip=formatter_conf.pip,
                                                       dependencies=conf.env_dependencies(e)))

    return envs

def _conda_writer(envs: list[CondaEnvironment], formatter_conf: _CondaConfiguration, output_dir: Path):
    """Writes a configuration as conda configuration environment file."""
    for env in envs:
        env.dump(path=Path(output_dir, f'{formatter_conf.file_pattern}_{env.name}.yml'),
                 encoding=formatter_conf.encoding)


@dataclass(frozen=True)
class _FormatterValue[C, O]:
    name: str
    to_environments: Callable[[Configuration, C], list[O]]
    serialize: Callable[[list[O], C, Path], None]
    configuration: Callable[[dict | str], C]

class Formatters(Enum):
    """The enumeration of the supported formatters."""
    CONDA = _FormatterValue[_CondaConfiguration, CondaEnvironment](name='conda',
                                                                   to_environments=_conda_mapper,
                                                                   serialize=_conda_writer,
                                                                   configuration=_CondaConfiguration.from_configuration)

    def test(self, formatter: dict | str) -> bool:
        """Checks if a formatter configuration dict refers to the current Formatter value."""
        return (isinstance(formatter, str) and self.value.name == formatter
                or isinstance(formatter, dict) and self.value.name in formatter)

    def _get_formatter_configuration(self, configuration: Configuration):
        """Builds a specific formatter configuration from the main configuration related to the current Formatter value.
        """
        for formatter in configuration.formatters:
            if self.test(formatter):
                return self.value.configuration(formatter)
        raise ValueError

    def build(self, conf: Configuration):
        """Build the list of the environments using the given configuration."""
        frmtter_conf = self._get_formatter_configuration(conf)
        return self.value.to_environments(conf, frmtter_conf)

    def write(self, conf: Configuration, output_dir: Path):
        """Build the list of the environments using the given configuration and writes them to the given output folder.
        """
        frmtter_conf = self._get_formatter_configuration(conf)
        envs = self.value.to_environments(conf, frmtter_conf)
        return self.value.serialize(envs, frmtter_conf, output_dir)
