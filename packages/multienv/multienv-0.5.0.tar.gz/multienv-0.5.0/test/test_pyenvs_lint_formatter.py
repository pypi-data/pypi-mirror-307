"""Test module for pyenv lint formatters."""


from multienv.pyenvs_deps_formatter import Formatters

def test_formatter_test():
    """Test formatter detection."""

    assert Formatters.CONDA.test('conda')
    assert not Formatters.CONDA.test('pip')
    assert Formatters.CONDA.test({'conda': {}})
