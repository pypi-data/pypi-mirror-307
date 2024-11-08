"""
Pyenv dependencies:
General Pip formatter output definitions.
"""

from dataclasses import dataclass

from multienv.pyenvs_deps_input_std import Dependency

@dataclass(frozen=True)
class PipEnvironment:
    """Pip environment file definition."""

    @staticmethod
    def format_dependency(d: Dependency) -> str:
        """Formats a dependency to a conda dependency string."""
        result : str = d.id
        if d.version is not None:
            result += '==' + d.version
        return result
