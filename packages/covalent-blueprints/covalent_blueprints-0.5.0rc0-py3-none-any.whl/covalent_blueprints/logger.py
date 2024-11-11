# Copyright 2024 Agnostiq Inc.
"""Logger for core blueprints functionality."""

import logging
import time
from pathlib import Path


class LocalTimeFormatter(logging.Formatter):
    """Override the converter to use local time."""

    def converter(self, timestamp):
        """Overridden converter method."""
        return time.localtime(timestamp)


# Define the log file path
BLUEPRINTS_LOGFILE = Path.home() / ".cache/covalent/blueprints/logfile.txt"

# Ensure the log file and its directory exist
if not BLUEPRINTS_LOGFILE.exists():
    BLUEPRINTS_LOGFILE.parent.mkdir(parents=True, exist_ok=True)
    BLUEPRINTS_LOGFILE.touch()

# Define the log format
LOG_FORMAT = (
    "> %(asctime)s [%(levelname)s] - %(pathname)s:%(lineno)d\n\n%(message)s\n\n"
)

# Create a logger
bp_log = logging.getLogger("covalent_blueprints")
bp_log.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler(BLUEPRINTS_LOGFILE)
file_handler.setLevel(logging.DEBUG)

# Create a formatter with local time
formatter = LocalTimeFormatter(
    fmt=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(formatter)

# Add the handler to the logger
bp_log.addHandler(file_handler)


def clear_logs() -> None:
    """Delete the blueprints log file."""
    if not BLUEPRINTS_LOGFILE.exists():
        BLUEPRINTS_LOGFILE.parent.mkdir(parents=True, exist_ok=True)
        BLUEPRINTS_LOGFILE.touch()

    with open(BLUEPRINTS_LOGFILE, "w", encoding="utf-8") as log_file:
        log_file.write("")

    print(f"Erased contents of logs file: {BLUEPRINTS_LOGFILE!s}")


def get_logs_content() -> str:
    """Return the contents of the blueprints log file."""
    with open(BLUEPRINTS_LOGFILE, "r", encoding="utf-8") as log_file:
        return "\n".join([log_file.read(), f"[FILE: {BLUEPRINTS_LOGFILE!s}]"])
