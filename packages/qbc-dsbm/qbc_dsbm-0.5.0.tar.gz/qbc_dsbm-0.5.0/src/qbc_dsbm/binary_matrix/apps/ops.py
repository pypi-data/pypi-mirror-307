"""Application module for binary matrix operations."""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path  # noqa: TCH003
from typing import Callable

import typer

from qbc_dsbm.binary_matrix import (
    BinMatrix,
    BinMatrixStats,
    DegeneratedMatrixError,
    a_inter_b_columns,
    a_inter_b_rows,
    a_minus_b_columns,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s [%(levelname)s] %(message)s",
)
console_handler.setFormatter(formatter)
_LOGGER.addHandler(console_handler)


@dataclass
class MatricesOperationArgs:
    """Matrices operation args and opts."""

    ARG_SUPER_BM_CSV_PATH = typer.Argument(
        help="Path to the super binary matrix CSV file",
    )
    ARG_SUB_BM_CSV_PATH = typer.Argument(
        help="Path to the sub binary matrix CSV file",
    )
    ARG_RESULT_BM_CSV_PATH = typer.Argument(
        help="Path to the resulting binary matrix CSV file",
    )
    OPT_MUTE_LOGGER = typer.Option(
        default=False,
        help="Mute the logger",
    )


APP = typer.Typer()


@APP.command()
def coldiff(
    super_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUPER_BM_CSV_PATH,
    sub_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUB_BM_CSV_PATH,
    result_binmatrix_csv: Path = MatricesOperationArgs.ARG_RESULT_BM_CSV_PATH,
    mute_logger: bool = MatricesOperationArgs.OPT_MUTE_LOGGER,  # noqa: FBT001
) -> None:
    """Produce the binary matrix column-intersection between two binary matrices.

    It keeps the rows but differs on the columns.

    """
    _LOGGER.info("Beginning col-diff operation")
    if mute_logger:
        _LOGGER.setLevel(logging.CRITICAL)
    super_matrix, sub_matrix = __init_super_sub_bm(
        super_binmatrix_csv,
        sub_binmatrix_csv,
    )
    result_matrix = __execute_op(super_matrix, sub_matrix, a_minus_b_columns)
    __finish_result_matrix(result_binmatrix_csv, result_matrix)


@APP.command()
def colinter(
    super_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUPER_BM_CSV_PATH,
    sub_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUB_BM_CSV_PATH,
    result_binmatrix_csv: Path = MatricesOperationArgs.ARG_RESULT_BM_CSV_PATH,
    mute_logger: bool = MatricesOperationArgs.OPT_MUTE_LOGGER,  # noqa: FBT001
) -> None:
    """Produce the binary matrix column-intersection between two binary matrices.

    It keeps the rows but differs on the columns.

    """
    _LOGGER.info("Beginning col-inter operation")
    if mute_logger:
        _LOGGER.setLevel(logging.CRITICAL)
    super_matrix, sub_matrix = __init_super_sub_bm(
        super_binmatrix_csv,
        sub_binmatrix_csv,
    )
    result_matrix = __execute_op(super_matrix, sub_matrix, a_inter_b_columns)
    __finish_result_matrix(result_binmatrix_csv, result_matrix)


@APP.command()
def rowdiff(
    super_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUPER_BM_CSV_PATH,
    sub_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUB_BM_CSV_PATH,
    result_binmatrix_csv: Path = MatricesOperationArgs.ARG_RESULT_BM_CSV_PATH,
    mute_logger: bool = MatricesOperationArgs.OPT_MUTE_LOGGER,  # noqa: FBT001
) -> None:
    """Produce the binary matrix row-difference between two binary matrices.

    It keeps the columns but differs on the rows.

    """
    _LOGGER.info("Beginning row-diff operation")
    if mute_logger:
        _LOGGER.setLevel(logging.CRITICAL)
    super_matrix, sub_matrix = __init_super_sub_bm(
        super_binmatrix_csv,
        sub_binmatrix_csv,
    )
    result_matrix = __execute_op(super_matrix, sub_matrix, a_inter_b_rows)
    __finish_result_matrix(result_binmatrix_csv, result_matrix)


@APP.command()
def rowinter(
    super_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUPER_BM_CSV_PATH,
    sub_binmatrix_csv: Path = MatricesOperationArgs.ARG_SUB_BM_CSV_PATH,
    result_binmatrix_csv: Path = MatricesOperationArgs.ARG_RESULT_BM_CSV_PATH,
    mute_logger: bool = MatricesOperationArgs.OPT_MUTE_LOGGER,  # noqa: FBT001
) -> None:
    """Produce the binary matrix row-intersection between two binary matrices.

    It keeps the columns but differs on the rows.

    """
    _LOGGER.info("Beginning row-inter operation")
    if mute_logger:
        _LOGGER.setLevel(logging.CRITICAL)
    super_matrix, sub_matrix = __init_super_sub_bm(
        super_binmatrix_csv,
        sub_binmatrix_csv,
    )
    result_matrix = __execute_op(super_matrix, sub_matrix, a_inter_b_rows)
    __finish_result_matrix(result_binmatrix_csv, result_matrix)


def __init_super_sub_bm(
    super_binmatrix_csv: Path,
    sub_binmatrix_csv: Path,
) -> tuple[BinMatrix, BinMatrix]:
    super_matrix = BinMatrix.from_csv(super_binmatrix_csv)
    sub_matrix = BinMatrix.from_csv(sub_binmatrix_csv)
    _LOGGER.info(
        "Super matrix:\n%s\n",
        BinMatrixStats.from_bin_matrix(super_matrix),
    )
    _LOGGER.info(
        "Sub matrix:\n%s\n",
        BinMatrixStats.from_bin_matrix(sub_matrix),
    )
    return super_matrix, sub_matrix


def __execute_op(
    super_matrix: BinMatrix,
    sub_matrix: BinMatrix,
    op_func: Callable[[BinMatrix, BinMatrix], BinMatrix],
) -> BinMatrix:
    try:
        return op_func(super_matrix, sub_matrix)
    except DegeneratedMatrixError as error:
        _LOGGER.critical("%s", error)
        sys.exit(1)


def __finish_result_matrix(
    result_binmatrix_csv: Path,
    result_matrix: BinMatrix,
) -> None:
    _LOGGER.info(
        "Resulting matrix:\n%s\n",
        BinMatrixStats.from_bin_matrix(result_matrix),
    )
    result_matrix.to_csv(result_binmatrix_csv)
