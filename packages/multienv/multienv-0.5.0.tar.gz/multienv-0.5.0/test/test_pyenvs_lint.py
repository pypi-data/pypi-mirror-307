"""Test module for pyenvs"""
from argparse import Namespace
from pathlib import Path


from multienv.pyenvs_lint import _lint


def _input_file(file: str) -> str:
    """Les fichiers d'entrée se trouvent à côté des scripts de test."""
    return str(Path(Path(__file__).parent, file))

def _output_file(file: str) -> str:
    """Les fichiers de sortie sont générés relativement à l'endroit où la commande est exécutée."""
    return str(Path(Path.cwd(), file))

def test_lint_without_default_env():
    """test config call without default env"""

    _lint(Namespace(CMD='lint', file=_input_file('pyenvs_lint.yml'), encoding='utf-8', output='.'))

    assert True

def test_lint_with_distinct_values_by_envs():
    """test config call without default env"""

    _lint(Namespace(CMD='lint', file=_input_file('pyenvs_distinct_lint.yml'), encoding='utf-8', output='.'))

    assert True
