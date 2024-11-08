"""Pyenvs lint:
Formatter definitions.

Supported formatters:
- pylint
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

from multienv.pyenvs_lint_input_std import Configuration
from multienv.pyenvs_lint_output_pylint import Pylintrc


@dataclass(frozen=True)
class _PylintConfiguration:
    """The specific Pylint configuration model."""

    default_environment: str | None
    strict_environment: str | None
    file_pattern: str
    encoding: str

    @staticmethod
    def from_configuration(formatter: dict | str):
        """Builds a Pylint configuration object form a dict or a default one form a string"""

        if isinstance(formatter, str):
            return _DEFAULT_PYLINT_CONFIGURATION

        body = formatter[Formatters.PYLINT.value.name]

        return _PylintConfiguration(
            default_environment=body['default_environment'] if 'default_environment' in body
            else _DEFAULT_PYLINT_CONFIGURATION.default_environment,
            strict_environment=body['strict_environment'] if 'strict_environment' in body
            else _DEFAULT_PYLINT_CONFIGURATION.strict_environment,
            file_pattern=body['file_pattern'] if 'file_pattern' in body else _DEFAULT_PYLINT_CONFIGURATION.file_pattern,
            encoding=body['encoding'] if 'encoding' in body else _DEFAULT_PYLINT_CONFIGURATION.encoding
        )

_DEFAULT_PYLINT_CONFIGURATION = _PylintConfiguration(
    default_environment=None,
    strict_environment=None,
    file_pattern='pylintrc',
    encoding='utf-8'
)

def _pylint_mapper(conf: Configuration, formatter_conf: _PylintConfiguration) -> list[Pylintrc]:
    """Writes a configuration as pylintrc file."""

    environments = conf.effective_environments()

    envs: list[Pylintrc] = []

    # default environment includes all dependencies
    if formatter_conf.default_environment:
        envs.append(Pylintrc.from_configuration(name=formatter_conf.default_environment, configuration=conf))

    # strict environment excludes all dependencies specific to an environment
    if formatter_conf.strict_environment:
        envs.append(Pylintrc.from_rules(name=formatter_conf.strict_environment, sections=conf.strict_rules()))

    for e in environments:
        envs.append(Pylintrc.from_rules(name=e, sections=conf.env_rules(e)))

    return envs

def _pylint_writer(envs: list[Pylintrc], formatter_conf: _PylintConfiguration, output_dir: Path):
    """Writes a configuration as pylintrc configuration environment files."""
    for env in envs:
        env.dump(path=Path(output_dir, f'{formatter_conf.file_pattern}_{env.name}'),
                 encoding=formatter_conf.encoding)


@dataclass(frozen=True)
class _FormatterValue[C, O]:
    name: str
    to_environments: Callable[[Configuration, C], list[O]]
    serialize: Callable[[list[O], C, Path], None]
    configuration: Callable[[dict | str], C]

class Formatters(Enum):
    """The enumeration of the supported formatters."""
    PYLINT = _FormatterValue[_PylintConfiguration, Pylintrc](name='pylint',
                                                             to_environments=_pylint_mapper,
                                                             serialize=_pylint_writer,
                                                             configuration=_PylintConfiguration.from_configuration)

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
