from __future__ import annotations

import logging
from typing import Any

from ruamel import yaml

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        self.settings: dict[str, Any] | None = None

    def read_from_file(self, filename: str):
        try:
            with open(filename, encoding="utf-8") as fp:
                settings: Any = yaml.safe_load(fp.read())
        except (TypeError, FileNotFoundError):
            logger.error("Could not open configuration file %s.", filename)
            settings = None

        if settings is not None and not isinstance(settings, dict):
            raise ValueError("Malformed configuration file.")

        self.settings = settings

    def __str__(self) -> str:
        return self.settings.__str__()


config = Config()
