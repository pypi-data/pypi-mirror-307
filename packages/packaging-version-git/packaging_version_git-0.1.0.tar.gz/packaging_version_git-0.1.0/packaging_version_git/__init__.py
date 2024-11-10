from importlib import metadata as _metadata

from packaging_version_git.collector import GitVersionCollector  # noqa: F401
from packaging_version_git.version import GitVersion  # noqa: F401

try:
    __version__ = _metadata.version('packaging-version-git')

except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
