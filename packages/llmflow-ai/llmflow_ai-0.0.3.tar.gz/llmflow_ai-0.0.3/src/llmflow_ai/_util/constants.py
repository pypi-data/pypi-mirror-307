from pathlib import Path

PKG_AUTHOR = "SOT"
PKG_AUTHOR_DIR = "UK-AISI"
PKG_NAME = Path(__file__).parent.parent.stem
PKG_PATH = Path(__file__).parent.parent
ALL_LOG_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]
DEFAULT_LOG_LEVEL = "warning"
DEFAULT_LOG_LEVEL_TRANSCRIPT = "info"
