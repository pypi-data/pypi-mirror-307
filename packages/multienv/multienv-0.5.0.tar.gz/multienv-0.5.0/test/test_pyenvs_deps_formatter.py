"""Test module for pyenv deps formatters."""


from multienv.pyenvs_lint_formatter import Formatters

def test_formatter_test():
    """Test formatter detection."""

    assert Formatters.PYLINT.test('pylint')
    assert not Formatters.PYLINT.test('pip')
    assert Formatters.PYLINT.test({'pylint': {}})
