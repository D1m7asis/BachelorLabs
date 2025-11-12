from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def set_verbosity(verbose: int) -> None:
    if verbose <= 0:
        configure_logging(logging.INFO)
    elif verbose == 1:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.NOTSET)
