"""Pyenv config:
General standard input definition.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MapRule:
    """Representation of pyenvs lint map rule content.
    Such a rule specifies distinct values for a same rule in many environments."""
    key: str
    environments: dict[str, str]

    @staticmethod
    def from_dict(source: dict):
        """Builds a Rule from a configuration dict."""

        return MapRule(
            key=source['key'],
            environments=source['environments'],
        )

@dataclass(frozen=True)
class ValueRule:
    """Representation of pyenvs lint strict rule content.
    Such a rule is common to all environments and so, don't need to specify anyone."""
    key: str
    value: str

    @staticmethod
    def from_dict(source: dict):
        """Builds a Rule from a configuration dict."""

        return ValueRule(
            key=source['key'],
            value=source['value']
        )

@dataclass(frozen=True)
class ListRule:
    """Representation of pyenvs lint rule content.
    Such a rule specifies a single value valid for a list of specific environments."""
    key: str
    value: str
    environments: list[str]

    @staticmethod
    def from_dict(source: dict):
        """Builds a Rule from a configuration dict."""

        return ListRule(
            key=source['key'],
            value=source['value'],
            environments=source['environments'],
        )

@dataclass(frozen=True)
class Section:
    """Representation of pyenvs lint section content."""
    name: str
    rules: list[ValueRule | MapRule | ListRule]

    @staticmethod
    def from_dict(source: dict):
        """Builds a Section from a configuration dict."""

        assert 'name' in source, 'name is a mandatory section field'
        assert 'rules' in source, 'rules is a mandatory section field'

        rules = []
        for s in source['rules']:
            if 'value' in s and 'environments' in s:
                rules.append(ListRule.from_dict(s))
            elif 'value' in s:
                rules.append(ValueRule.from_dict(s))
            elif 'environments' in s:
                rules.append(MapRule.from_dict(s))
            else:
                raise ValueError
        return Section(
            name=source['name'],
            rules=rules,
        )

    def environment_rules(self, environment: str):
        """Get a new section containing only rules for the given environment."""
        return Section(name=self.name,
                       rules=[r for r in self.rules if isinstance(r, ValueRule) or environment in r.environments])

    def strict_rules(self):
        """Get a new section containing only the strict rules."""
        return Section(name=self.name,
                       rules=[r for r in self.rules if isinstance(r, ValueRule)])

    def __len__(self):
        return len(self.rules)

@dataclass(frozen=True)
class Configuration:
    """Representation of pyenvs lint configuration content."""

    formatters: list[dict | str]
    """Each formatter either can be a single character string of one of supported formatters or a key/value pair with 
    the key referencing to the formatter name and the value referencing to its specific configuration."""

    environments: list[str] | None
    """A reference list of the environments referenced by dependencies. If the list is provided, dependencies 
    referencing an unknown environment raise an error. If the list is not provided, it is inferred from the dependency
    environments. If an empty list is provided, no dependency is supposed to reference any specific environment."""

    sections: list[Section]
    """The list of the sections."""

    @staticmethod
    def from_dict(source: dict):
        """Builds a Configuration from a configuration dict."""
        return Configuration(
            formatters=source['configuration']['formatters'],
            environments=source['environments'] if 'environments' in source else None,
            sections=[Section.from_dict(s) for s in source['sections']]
        )

    def strict_rules(self) -> list[Section]:
        """Returns only the strict rules which are ones not specifying any environment."""
        return [sr for sr in [s.strict_rules() for s in self.sections] if len(sr) > 0]

    def env_rules(self, environment: str) -> list[Section]:
        """Returns all the specified environment rules which are strict ones and ones referring to the given
        environment."""
        return [er for er in [s.environment_rules(environment=environment) for s in self.sections] if len(er) > 0]

    def _implicit_environments(self) -> list[str]:
        """Computes implicit environments which are ones contained in dependency environment lists."""
        return list(dict.fromkeys([e for s in self.sections if s.rules
                                   for r in s.rules if not isinstance(r, ValueRule)
                                   for e in r.environments]))

    def effective_environments(self) -> list[str]:
        """Checks environments and computes effective ones.

        1. Computes the effective environments.
        2. If a global environment list is provided, cheks its maps the implicit environment set.
        3. Returns the environment list if supplied, or default, the implicit environment list.
        """
        implicit_envs = self._implicit_environments()

        if self.environments is not None and set(self.environments) != set(implicit_envs):
            raise ValueError(
                f'if defined, environment list {self.environments} should match '
                f'the implicit environment dependency set {implicit_envs}')

        return implicit_envs if self.environments is None else self.environments
