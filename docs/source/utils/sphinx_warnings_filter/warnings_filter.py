"""Sphinx plugin to filter out warnings that are known to be false positives.

Warnings filter extension
#########################

Copyright (c) 2021 Nordic Semiconductor ASA
SPDX-License-Identifier: Apache-2.0

Introduction
============

This Sphinx plugin can be used to filter out warnings that are known to be false
positives. The warnings are filtered out based on a set of regular expressions
given via an configuration file. The format of the configuration file is a
yaml file where each entry consists of :

regex: A regex for matching the desired warnings text (e.g. ".*document isn't included in any toctree.*")
silent: true: the message will be removed from the log, false: the warning is still shown
message_level: Loglevel of logging. Decides only the color of the log message
               Allowed values are WARNING or INFO. Default: INFO.
extra_message: An additional message to add to the warning message

Any lines starting with ``#`` will be ignored.

Configuration options
=====================

- ``warnings_filter_config``: Configuration file.

==============================================================================
 C O P Y R I G H T
------------------------------------------------------------------------------
Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

Modifications:

- Fixed bug where warnings text was not interpreted as string
- Changed config file to use YAML. Added customization features in YAML

Authors:

- Nirmal Sasidharan (Robert Bosch GmbH)
- Joscha Liedtke (Robert Bosch GmbH)
- Stephan Kuempel (em:AG contracted by Robert Bosch GmbH)
==============================================================================
"""

import logging
import re
from pathlib import Path
from typing import List

import yaml
from sphinx.application import Sphinx
from sphinx.util.logging import NAMESPACE, WarningStreamHandler


class WarningsFilter(logging.Filter):  # pylint: disable=R0903
    """Warnings filter.

    Args:
        expressions: List of regular expressions.
        silent: If true, warning is hidden, otherwise it is shown as INFO.
        name: Filter name.
    """

    def __init__(self, expressions: List[dict], app: Sphinx) -> None:
        super().__init__("")

        self._expressions = expressions
        self._app: Sphinx = app

    def filter(self, record: logging.LogRecord) -> bool:
        # return True to not filter from stream
        # return False, it will not display and not counted as WARNING

        # All messages passed to WarningStreamHandler are of type WARNING
        for expression in self._expressions:
            if re.match(expression["regex"], str(record.msg)):
                if expression.get("silent", True):
                    return False

                extra_message = expression.get("extra_message", "")
                message_level = expression.get("message_level", "info")

                if message_level.lower() == "warning":
                    fg_color = "\x1b[0;31;20m"
                    color_reset = "\x1b[0m"
                else:
                    fg_color = ""
                    color_reset = ""

                logger = logging.getLogger(NAMESPACE)

                path = self._app.builder.env.doc2path(record.location)
                logger.info(
                    "%s\nFiltered warning:\n%s:%s\n%s%s", fg_color, path, record.msg, extra_message, color_reset
                )
                return False
        return True


def configure(app: Sphinx) -> None:
    """Entry point.

    Args:
        app: Sphinx application instance.
    """

    # load expressions from configuration file
    configfile = Path(app.config.warnings_filter_config)
    if not configfile.is_absolute():
        configfile = Path(app.srcdir) / configfile
    with configfile.open() as warn_file:
        expressions = yaml.safe_load(warn_file)
    if expressions is None:
        expressions = list()
    # install warnings filter to all the Sphinx logger handlers
    warnings_filter = WarningsFilter(expressions, app)
    logger = logging.getLogger(NAMESPACE)
    for handler in logger.handlers:
        if isinstance(handler, WarningStreamHandler):
            handler.filters.insert(0, warnings_filter)
