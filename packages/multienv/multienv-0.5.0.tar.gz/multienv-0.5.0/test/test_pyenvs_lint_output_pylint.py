"""Test module for pyenv pylint environment output."""

from multienv.pyenvs_lint_output_pylint import Pylintrc
from multienv.pyenvs_lint_input_std import Section, ListRule


def test_format_dependency():
    """Test dependency formatting for conda."""

    s = Section(
        name='FORMAT',
        rules=[
            ListRule(key='max-line-length', value='120', environments=None),
            ListRule(key='max-args', value='9', environments=['src'])
        ]
    )

    assert (Pylintrc.from_rules(name='name', sections=[s]).format()
            == ['[FORMAT]\n', 'max-line-length=120\n', 'max-args=9\n', '\n'])
