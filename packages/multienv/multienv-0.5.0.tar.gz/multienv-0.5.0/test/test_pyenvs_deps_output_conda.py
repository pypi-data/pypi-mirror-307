"""Test module for pyenv conda environment output."""

from multienv.pyenvs_deps_output_conda import CondaEnvironment
from multienv.pyenvs_deps_input_std import Configuration, Dependency

def test_to_dict():
    """test dict representation of conda environment output"""

    env = CondaEnvironment(name="environment_name",
                           channels=["channel1", "channel2"],
                           pip_dependencies=["pip1", "pip2"],
                           dependencies=["pip1", "conda1", "pip2", "conda2"])

    assert env.to_dict() == {
        'name': 'environment_name',
        'channels': ['channel1', 'channel2'],
        'dependencies': ['pip1',
                         'conda1',
                         'pip2',
                         'conda2',
                         {
                             'pip': ['pip1', 'pip2']
                         }]
    }

def test_format_dependency():
    """test dependency formatting for conda"""

    d = Dependency(id="d_id", version="d_version", environments=["env_a", "env_b"], source="d_source", sha="d_sha")

    assert CondaEnvironment._format_dependency(d=d) == "d_id=d_version=d_sha"


def test_from_configuration():
    """test conda environment instantiation from configuration"""

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
    e = CondaEnvironment.from_configuration(name='default',
                                        pip=None,
                                        channels=None,
                                        configuration=c)

    assert e.name == 'default'
    assert e.dependencies == ['multienv=0.0.2']

def test_from_dependencies():
    """test conda environment instantiation from dependencies"""

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
    e = CondaEnvironment.from_dependencies(name='default',
                                           pip=None,
                                           channels=None,
                                           dependencies=c.dependencies)

    assert e.name == 'default'
    assert e.dependencies == ['multienv=0.0.2']
