# Copyright (C) 2023,2024 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# pylint: disable=W0622

"""A console program that generates yearly calendar heatmap."""

import argparse
import logging
import multiprocessing
import platform
import random
import sys
from pathlib import Path

import pandas as pd

__version__ = "0.13.4"

# Suppress logging from matplotlib in debug mode
logging.getLogger("matplotlib").propagate = False
logger = multiprocessing.get_logger()


class DemoAction(argparse.Action):
    """Generate a list of demo heatmaps action."""

    def __init__(self, *nargs, **kwargs):
        """Overwrite class method."""
        kwargs.update({"nargs": "?"})
        super().__init__(*nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Overwrite class method."""
        setattr(
            namespace, "input_filename", f"{namespace.output_dir}/sample.csv"
        )
        setattr(namespace, "year", 2024)
        setattr(namespace, "week", 52)
        setattr(namespace, "demo", values)

        self._generate_sample_csv(namespace)

    def _generate_sample_csv(self, config: argparse.Namespace) -> None:
        """Generate a sample CSV data file.

        Args:
            config (argparse.Namespace): Config from command line arguments

        Returns:
            None
        """
        df_dates = pd.DataFrame(
            {
                "date": pd.date_range(
                    start=f"{config.year}-01-01",
                    end=f"{config.year}-12-31",
                ),
            }
        )
        df_dates["count"] = random.sample(range(12000), len(df_dates))

        csv_filename = Path(config.output_dir, "sample.csv")
        csv_filename.parent.mkdir(parents=True, exist_ok=True)
        df_dates.to_csv(csv_filename, sep=",", index=False, header=False)
        logger.debug("generate sample csv file: %s", csv_filename)


class EnvironmentAction(argparse.Action):
    """Show environment details action."""

    def __init__(self, *nargs, **kwargs):
        """Overwrite class method."""
        kwargs.update({"nargs": 0})
        super().__init__(*nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Overwrite class method."""
        sys_version = sys.version.replace("\n", "")
        env = (
            f"heatmap: {__version__}\n"
            f"python: {sys_version}\n"
            f"platform: {platform.platform()}\n"
        )
        parser._print_message(env, sys.stdout)
        parser.exit()
