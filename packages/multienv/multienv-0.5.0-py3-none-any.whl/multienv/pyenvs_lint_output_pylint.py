"""
Pyenv lint:
General Pylint formatter output definitions.
"""

from dataclasses import dataclass
from pathlib import Path

from multienv.pyenvs_lint_input_std import Section, Configuration, MapRule


@dataclass(frozen=True)
class Pylintrc:
    """Pylint configuration file definition."""
    name: str
    sections: list[Section]

    def dump(self, path: Path, encoding: str):
        """Write to yml output file."""
        with open(path, 'w', encoding=encoding) as pylintrc:
            for l in self.format():
                pylintrc.write(l)

    @staticmethod
    def from_configuration(name: str, configuration: Configuration):
        """Build an environment from a standard configuration."""
        return Pylintrc.from_rules(name=name, sections=configuration.sections)

    @staticmethod
    def from_rules(name: str, sections: list[Section]):
        """Build an environment from a dependency list."""
        return Pylintrc(name=name, sections=sections)

    def format(self) -> list[str]:
        """Formats a dependency to a pylint section rule string list."""
        result = []
        for s in self.sections:
            result.append(f"[{s.name}]\n")
            result.extend([f"{r.key}={r.environments[self.name]}\n" if isinstance(r, MapRule)
                           else f"{r.key}={r.value}\n"
                           for r in s.rules])
            result.append('\n')
        return result
