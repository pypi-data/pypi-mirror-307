"""Test module for pyenv conda environment output."""

from multienv.pyenvs_deps_output_pip import PipEnvironment
from multienv.pyenvs_deps_input_std import Dependency

def test_format_dependency():
    """Test dependency formatting for pip."""

    d = Dependency(id="d_id", version="d_version", environments=["env_a", "env_b"], source="d_source", sha="d_sha")

    assert PipEnvironment.format_dependency(d=d) == "d_id==d_version"
