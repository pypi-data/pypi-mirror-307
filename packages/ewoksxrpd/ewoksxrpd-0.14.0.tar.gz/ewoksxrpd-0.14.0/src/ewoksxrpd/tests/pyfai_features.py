import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version
from packaging.specifiers import SpecifierSet

_PYFAI_VERSION = version("pyFAI")
PYFAI_HAS_ORIENTATION = _PYFAI_VERSION in SpecifierSet(">=2024.1.0")
