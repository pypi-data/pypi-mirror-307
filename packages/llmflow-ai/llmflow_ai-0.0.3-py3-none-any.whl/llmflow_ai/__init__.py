# ruff: noqa: F401 F403 F405

from importlib.metadata import version as importlib_version

from llmflow_ai._util.constants import PKG_NAME

__version__ = importlib_version(PKG_NAME)


__all__ = [
    "__version__",
]
