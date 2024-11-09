from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("rsize")
except PackageNotFoundError:
    __version__ = "unknown"
