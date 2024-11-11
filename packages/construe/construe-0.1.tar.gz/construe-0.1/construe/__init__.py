"""
An LLM benchmarking utility that includes a command line interface for executing
and reviewing benchmarks on specific devices (usually embedded devices).
"""

##########################################################################
## Module Info
##########################################################################

# Import the version number at the top level
from .version import get_version, __version_info__


##########################################################################
## Package Version
##########################################################################

__version__ = get_version(short=True)
