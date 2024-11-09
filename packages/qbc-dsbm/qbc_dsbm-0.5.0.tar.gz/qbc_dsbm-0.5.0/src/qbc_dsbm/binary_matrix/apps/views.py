"""Application module for binary matrix views."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml  # type: ignore[import-untyped]

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

import typer

from qbc_dsbm.binary_matrix import BinMatrix, BinMatrixStats

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s [%(levelname)s] %(message)s",
)
console_handler.setFormatter(formatter)
_LOGGER.addHandler(console_handler)


@dataclass
class BMStatsArgs:
    """Binary matrix stats args and opts."""

    ARG_INPUT_BM_CSV_PATH = typer.Argument(
        help="Path to the binary matrix CSV file",
    )
    ARG_OUTPUT_DIRECTORY = typer.Option(
        default=None,
        help="Path to the output directory",
    )


APP = typer.Typer()


@APP.command()
def stats(
    binary_matrix_csv: Path = BMStatsArgs.ARG_INPUT_BM_CSV_PATH,
    output_directory: Optional[Path] = BMStatsArgs.ARG_OUTPUT_DIRECTORY,  # noqa: UP007
) -> None:
    """Get stats of a binary matrix."""
    binary_matrix = BinMatrix.from_csv(binary_matrix_csv)
    bin_matrix_stats = BinMatrixStats.from_bin_matrix(binary_matrix)
    _LOGGER.info("Binary matrix:\n%s\n", bin_matrix_stats)

    if output_directory is not None:
        output_directory = Path(output_directory)
        _LOGGER.info("Output directory: %s", output_directory)
        with (output_directory / "bin_matrix_stats.yaml").open("w") as yaml_out:
            yaml_out.write(
                yaml.dump(
                    bin_matrix_stats.to_dict(),
                    Dumper=Dumper,
                    sort_keys=False,
                ),
            )
