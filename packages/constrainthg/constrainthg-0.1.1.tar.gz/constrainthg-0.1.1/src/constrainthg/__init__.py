"""Initialization file for ConstraintHg."""

import logging

from constrainthg.hypergraph import *
import constrainthg.relations as R

LOG_LEVEL = logging.INFO

logger = logging.getLogger(__name__)

fh = logging.FileHandler("constrainthg.log")
fh.setLevel(LOG_LEVEL)
logger.info('Package begin execution')

log_formatter = logging.Formatter(
    fmt="[{asctime} | {levelname}]: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    )
fh.setFormatter(log_formatter)
logger.addHandler(fh)

logger.setLevel(LOG_LEVEL)
