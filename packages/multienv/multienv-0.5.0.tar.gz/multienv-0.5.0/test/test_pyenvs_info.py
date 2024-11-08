"""Test module for pyenvs info"""
from argparse import Namespace


from multienv.pyenvs import _create_parser



def test_info_args():
    """test info command"""

    parser = _create_parser()
    assert parser.parse_args(['info']) == Namespace(CMD='info')
