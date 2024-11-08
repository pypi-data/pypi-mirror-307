"""Test module for pyenv deps input."""

import pytest

from multienv.pyenvs_deps_input_std import Dependency, Configuration


def test_deps_configuration_from_dict_classic():
    """Test configuration loading from dict."""

    i = {
        'configuration': {
            'formatters': [
                {
                    'conda': {
                        'file_pattern': 'tutu',
                        'channels': ['default', 'cosmoloj']
                    }
                }
            ]
    },
        'dependencies': [{
            'id': 'multienv',
            'version': '0.0.2',
            'environments': ['multienv', 'test']
        }]
    }

    c = Configuration.from_dict(source=i)

    assert len(c.dependencies) == 1

    d = c.dependencies[0]
    assert d.id == 'multienv'
    assert d.version == '0.0.2'
    assert d.environments == ['multienv', 'test']
    assert d.sha is None
    assert d.source is None

def test_deps_configuration_strict_dependencies():
    """Test configuration supplying strict deps."""

    i = {
        'configuration': {
            'formatters': [
                {
                    'conda': {
                        'file_pattern': 'tutu',
                        'channels': ['default', 'cosmoloj']
                    }
                }
            ]
        },
        'dependencies': [{
            'id': 'multienv',
            'version': '0.0.2',
            'environments': ['multienv', 'test']
        }]
    }

    c = Configuration.from_dict(source=i)

    d = c.strict_dependencies()
    assert len(d) == 0

def test_deps_configuration_env_deps():
    """Test configuration supplying env deps."""

    i = {
        'configuration': {
            'formatters': [
                {
                    'conda': {
                        'file_pattern': 'tutu',
                        'channels': ['default', 'cosmoloj']
                    }
                }
            ]
        },
        'dependencies': [{
            'id': 'multienv',
            'version': '0.0.2',
            'environments': ['multienv', 'test']
        },
        {
            'id': 'pyyaml',
            'version': '0.0.3',
            'environments': ['test']
        }
        ]
    }

    c = Configuration.from_dict(source=i)

    d = c.env_dependencies('multienv')
    assert len(d) == 1

def test_deps_configuration_env_deps_2():
    """Test configuration supplying env deps."""

    i = {
        'configuration': {
            'formatters': [
                {
                    'conda': {
                        'file_pattern': 'tutu',
                        'channels': ['default', 'cosmoloj']
                    }
                }
            ]
        },
        'dependencies': [{
            'id': 'multienv',
            'version': '0.0.2',
            'environments': ['multienv', 'test']
        },
        {
            'id': 'pyyaml',
            'version': '0.0.3',
            'environments': ['test']
        }
        ]
    }

    c = Configuration.from_dict(source=i)

    d = c.env_dependencies('test')
    assert len(d) == 2

def test_deps_from_dict_classic():
    """Test dependency loading from dict."""

    i = {
        'id': 'multienv',
        'version': '0.0.2',
        'environments': ['multienv', 'test']
    }

    d = Dependency.from_dict(i)

    assert d.id == 'multienv'
    assert d.version == '0.0.2'
    assert d.environments == ['multienv', 'test']
    assert d.sha is None
    assert d.source is None


def test_deps_from_dict_single_id():
    """Test dependency loading from dict."""

    i = {
        'id': 'multienv'
    }

    d = Dependency.from_dict(i)

    assert d.id == 'multienv'
    assert d.version is None
    assert d.environments is None
    assert d.sha is None
    assert d.source is None


def test_deps_from_dict_without_id():
    """Test dependency loading from dict."""

    i = {
        'version': '0.0.2',
        'environments': ['multienv', 'test']
    }

    with pytest.raises(AssertionError) as e:
        Dependency.from_dict(i)

    assert e.value.args[0] == 'id is a mandatory dependency field'
