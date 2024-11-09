import sys

import pytest

from bumgr.executable import Executable


@pytest.fixture
def patch_executables():
    mpatch = pytest.MonkeyPatch()
    with mpatch.context() as m:
        # Use python as the execuatble
        m.setattr(Executable, "executable", sys.executable)
        yield
