"""Pyenv config:
General standard input definition.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Dependency:
    """Representation of dependency features."""

    id: str
    version: str | None
    environments: list[str] | None
    source: str | None
    sha: str | None

    @staticmethod
    def from_dict(source: dict):
        """Builds a Dependency from a configuration dict."""

        assert 'id' in source, 'id is a mandatory dependency field'

        return Dependency(
            id=source['id'],
            version=str(source['version']) if 'version' in source else None,
            environments=source['environments'] if 'environments' in source else None,
            source=source['source'] if 'source' in source else None,
            sha=source['sha'] if 'sha' in source else None
        )

@dataclass(frozen=True)
class Configuration:
    """Representation of pyenvs configuration content."""

    formatters: list[dict | str]
    """Each formatter either can be a single character string of one of supported formatters or a key/value pair with 
    the key referencing to the formatter name and the value referencing to its specific configuration."""

    environments: list[str] | None
    """A reference list of the environments referenced by dependencies. If the list is provided, dependencies 
    referencing an unknown environment raise an error. If the list is not provided, it is inferred from the dependency
    environments. If an empty list is provided, no dependency is supposed to reference any specific environment."""

    dependencies: list[Dependency]
    """The list of the dependencies."""

    @staticmethod
    def from_dict(source: dict):
        """Builds a Configuration from a configuration dict."""
        return Configuration(
            formatters=source['configuration']['formatters'],
            environments=source['environments'] if 'environments' in source else None,
            dependencies=[Dependency.from_dict(d) for d in source['dependencies']]
        )

    def strict_dependencies(self) -> list[Dependency]:
        """Returns only the strict dependencies which are ones not specifying any environment."""
        return [d for d in self.dependencies if not d.environments]

    def env_dependencies(self, environment: str) -> list[Dependency]:
        """Returns all the specified environment dependencies which are strict ones and ones referring to the given
        environment."""
        return [d for d in self.dependencies if not d.environments or environment in d.environments]

    def _implicit_environments(self) -> list[str]:
        """Computes implicit environments which are ones contained in dependency environment lists."""
        return list(dict.fromkeys([e for dep in self.dependencies if dep.environments for e in dep.environments]))

    def effective_environments(self) -> list[str]:
        """Checks environments and computes effective ones.

        1. Computes the effective environments.
        2. If a global environment list is provided, checks its maps the implicit environment set.
        3. Returns the environment list if supplied, or default, the implicit environment list.
        """
        implicit_envs = self._implicit_environments()

        if self.environments is not None and set(self.environments) != set(implicit_envs):
            raise ValueError(
                f'if defined, environment list {self.environments} should match '
                f'the implicit environment dependency set {implicit_envs}')

        return implicit_envs if self.environments is None else self.environments
