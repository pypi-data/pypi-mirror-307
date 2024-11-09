"""Application module for binary matrix creation."""

# Due to typer usage:
# ruff: noqa: TCH001, TCH003, UP007, FBT001, FBT002, PLR0913

from __future__ import annotations

import ast
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Optional, cast

import numpy as np
import pandas as pd
import typer

import qbc_dsbm.args as common_args
import qbc_dsbm.binary_matrix.configs as bm_cfg
import qbc_dsbm.binary_matrix.create as bm_create
import qbc_dsbm.logging as common_log
from qbc_dsbm.binary_matrix.items import BinMatrix, NotABinaryMatrixError

_LOGGER = logging.getLogger(__name__)

APP = typer.Typer(rich_markup_mode="rich")


@dataclass
class CommonArgs:
    """Common args and opts."""

    ARG_INPUT_MATRIX = typer.Argument(
        help="Path to the non-binary matrix",
    )

    ARG_OUTPUT_MATRIX = typer.Argument(
        help="Path to the output binary matrix",
    )


@dataclass
class NewArgs:
    """New args and opts."""

    ARG_NUMBER_OF_ROWS = typer.Argument(
        help="Number of rows",
    )

    ARG_NUMBER_OF_COLUMNS = typer.Argument(
        help="Number of columns",
    )

    ARG_DENSITY = typer.Argument(
        help="Density of the binary matrix",
    )


@dataclass
class CustomArgs:
    """Custom args and opts."""

    ARG_VALUE_REPLACED = typer.Argument(
        help=('Value to replace as a python dict in a string, e.g. "{-1: 1, -2: 0}"'),
    )


@APP.command()
def new(
    number_of_rows: Annotated[int, NewArgs.ARG_NUMBER_OF_ROWS],
    number_of_columns: Annotated[int, NewArgs.ARG_NUMBER_OF_COLUMNS],
    density: Annotated[float, NewArgs.ARG_DENSITY],
    output_matrix: Path = CommonArgs.ARG_OUTPUT_MATRIX,
) -> None:
    """Create a binary matrix."""
    bin_matrix = bm_create.generate_bin_matrix(
        number_of_rows,
        number_of_columns,
        1 - density,
    )
    bin_matrix.to_csv(output_matrix)


@APP.command()
def custom(
    input_matrix: Path = CommonArgs.ARG_INPUT_MATRIX,
    output_matrix: Path = CommonArgs.ARG_OUTPUT_MATRIX,
    value_replaced: str = CustomArgs.ARG_VALUE_REPLACED,
) -> None:
    """Transform non-binary matrix to binary matrix with custom replacement."""
    try:
        value_replaced_dict = ast.literal_eval(value_replaced)
    except SyntaxError:
        _LOGGER.critical("Invalid value_replaced: %s", value_replaced_dict)
        sys.exit(1)
    if not isinstance(value_replaced_dict, dict):
        _LOGGER.critical("Invalid value_replaced: %s", value_replaced_dict)
        sys.exit(1)

    try:
        bin_matrix = BinMatrix.from_csv(
            input_matrix,
            replace_value_map=cast(dict, value_replaced),
        )
    except NotABinaryMatrixError as err:
        _LOGGER.critical("Output matrix is not a binary matrix:")
        _LOGGER.critical(err)
        sys.exit(1)

    bin_matrix.to_csv(output_matrix)


@APP.command()
def random(
    input_matrix: Path = CommonArgs.ARG_INPUT_MATRIX,
    output_matrix: Path = CommonArgs.ARG_OUTPUT_MATRIX,
) -> None:
    """Transform non-binary matrix to binary matrix with random replacement."""
    df: pd.DataFrame = pd.read_csv(input_matrix, header=0, index_col=0)

    rng = np.random.default_rng()
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i, j] not in (0, 1):
                df.iloc[i, j] = rng.choice([0, 1], 1)

    BinMatrix.new_unsafe(df).to_csv(output_matrix)


@dataclass
class KNNArgs:
    """KNN args and opts."""

    __CFG_CAT = "KNN configuration"

    OPT_NUMBER_OF_NEIGHBOURS = typer.Option(
        "--number-of-neighbours",
        "-n",
        help="Number of nearest neighbours",
        rich_help_panel=__CFG_CAT,
    )

    OPT_THRESHOLD = typer.Option(
        "--threshold",
        "-t",
        help=(
            "Threshold confident interval:"
            " if 0 <= values < threshold, then value -> 0,"
            " else if threshold <= values <= 1, then value -> 1,"
            " else value -> undefined"
        ),
        rich_help_panel=__CFG_CAT,
    )

    OPT_CONFIG_FILE = typer.Option(
        "--config",
        help="Path to the config file",
        rich_help_panel=__CFG_CAT,
    )


@APP.command()
def knn(
    input_matrix: Annotated[Path, CommonArgs.ARG_INPUT_MATRIX],
    output_matrix: Annotated[Path, CommonArgs.ARG_OUTPUT_MATRIX],
    number_of_neighbours: Annotated[
        int,
        KNNArgs.OPT_NUMBER_OF_NEIGHBOURS,
    ] = bm_cfg.KNNFillingConfig.DEFAULT_NUMBER_OF_NEIGHBOURS,
    threshold: Annotated[
        float,
        KNNArgs.OPT_THRESHOLD,
    ] = bm_cfg.KNNFillingConfig.DEFAULT_THRESHOLD,
    config_file: Annotated[
        Optional[Path],
        KNNArgs.OPT_CONFIG_FILE,
    ] = None,
    debug: Annotated[
        bool,
        common_args.CommonArgs.OPT_DEBUG,
    ] = False,
) -> None:
    """Transform non-binary matrix to binary matrix with KNN replacement."""
    common_log.init_logger("KNN replacement command", debug)
    _LOGGER.info("Input matrix: %s", input_matrix)
    _LOGGER.info("Output matrix: %s", output_matrix)

    df: pd.DataFrame = pd.read_csv(input_matrix, header=0, index_col=0)

    knn_config = (
        bm_cfg.KNNFillingConfig.from_yaml(config_file)
        if config_file is not None
        else bm_cfg.KNNFillingConfig(
            number_of_neighbours=number_of_neighbours,
            threshold=threshold,
        )
    )

    try:
        bin_matrix = bm_create.complete_dataframe_with_knn(df, knn_config)
    except NotABinaryMatrixError as err:
        _LOGGER.critical("Output matrix is not a binary matrix:")
        _LOGGER.critical(err)
        sys.exit(1)

    if bin_matrix is None:
        _LOGGER.warning("KNN matrix cannot be completed, no output matrix")
    else:
        bin_matrix.to_csv(output_matrix)


if __name__ == "__main__":
    APP()
