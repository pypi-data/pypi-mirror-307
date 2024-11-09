"""
Because we're printing out a lot of strings, I'm going to use individual tests
rather than pytest.parametrize.

"""

from pathlib import Path

_TEST_ROOT = Path(__file__).parent
_TEST_DATA_DIR = _TEST_ROOT / "data"
