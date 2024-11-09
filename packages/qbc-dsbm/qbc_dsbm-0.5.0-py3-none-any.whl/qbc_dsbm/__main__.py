"""Quasi-bi-clique and the densest sub-binary matrix problem main module."""

# Due to typer usage:
# ruff: noqa: TCH001, TCH003, UP007, FBT001, PLR0913

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

import typer

import qbc_dsbm.binary_matrix.apps.create as bm_apps_create
import qbc_dsbm.binary_matrix.apps.ops as bm_apps_ops
import qbc_dsbm.binary_matrix.apps.views as bm_apps_views
from qbc_dsbm import QBCExactModels, QBCHeuristicModels
from qbc_dsbm.binary_matrix.items import BinMatrix
from qbc_dsbm.cli import (
    CommonArgs,
    DivCqrArgs,
    SolverChoice,
    UniqueArgs,
    UniqueModelChoices,
)
from qbc_dsbm.io_config import IOConfig, IOConfigDivCqr
from qbc_dsbm.loggers import DivCqrStrategyLogger, UniqueStrategyLogger
from qbc_dsbm.models.solvers import CBCSolver, GurobiSolver, Solver
from qbc_dsbm.strategies import (
    DivideAndConquerStrategyError,
    UniqueStrategyError,
    divide_and_conquer_strategy,
    unique_strategy,
)

__APP = typer.Typer()


_LOGGER = logging.getLogger("qbc_dsbm")
_LOGGER.setLevel(logging.DEBUG)


__APP.add_typer(bm_apps_create.APP, name="bm_create", help="Binary matrix creation")
__APP.add_typer(bm_apps_ops.APP, name="bm_ops", help="Binary matrix operations")
__APP.add_typer(bm_apps_views.APP, name="bm_views", help="Binary matrix views")


@__APP.command()
def unique(
    csv_path: Path = CommonArgs.ARG_CSV_PATH,
    solver: SolverChoice = CommonArgs.OPT_SOLVER,
    solve_time_lim: Optional[int] = CommonArgs.OPT_SOLVE_TIME_LIM,
    solver_log: bool = CommonArgs.OPT_SOLVER_PRINT_LOG,
    minimum_number_of_rows: int = UniqueArgs.OPT_MIN_NUMBER_OF_ROWS,
    minimum_number_of_columns: int = UniqueArgs.OPT_MIN_NUMBER_OF_COLUMNS,
    check_satisfiability: bool = UniqueArgs.OPT_CHECK_SATISFIABILITY,
    output_directory: Path = CommonArgs.OPT_OUTDIR,
    model: UniqueModelChoices = UniqueArgs.ARG_MODEL,
    epsilon: float = UniqueArgs.OPT_EPSILON,
    debug: bool = CommonArgs.OPT_DEBUG,
) -> None:
    """Solve with one model."""
    __format_logger(debug)
    __init_output_directory(output_directory)
    solver_obj = __create_solver_obj(solver, solve_time_lim, solver_log)
    io_config = IOConfig(
        csv_path,
        model.to_unique_model(),
        epsilon,
        solver_obj,
        minimum_number_of_rows,
        minimum_number_of_columns,
        check_satisfiability,
    )
    try:
        result_bin_matrix, logger = unique_strategy(io_config)
    except UniqueStrategyError as error:
        error.logger().write_yaml(output_directory)
        _LOGGER.critical(str(error))
        sys.exit(1)
    else:
        __finalize(result_bin_matrix, logger, output_directory)


@__APP.command()
def divcqr(
    csv_path: Path = CommonArgs.ARG_CSV_PATH,
    solver: SolverChoice = CommonArgs.OPT_SOLVER,
    solve_time_lim: Optional[int] = CommonArgs.OPT_SOLVE_TIME_LIM,
    solver_log: bool = CommonArgs.OPT_SOLVER_PRINT_LOG,
    output_directory: Path = CommonArgs.OPT_OUTDIR,
    heuristic_model: QBCHeuristicModels = DivCqrArgs.ARG_HEURISTIC_MODEL,
    heuristic_epsilon: float = DivCqrArgs.ARG_HEURISTIC_EPSILON,
    exact_model: QBCExactModels = DivCqrArgs.ARG_EXACT_MODEL,
    exact_epsilon: float = DivCqrArgs.ARG_EXACT_EPSILON,
    debug: bool = CommonArgs.OPT_DEBUG,
) -> None:
    """Solve with the divide and conquer strategy."""
    __format_logger(debug)
    __init_output_directory(output_directory)
    solver_obj = __create_solver_obj(solver, solve_time_lim, solver_log)
    io_config = IOConfigDivCqr(
        csv_path,
        heuristic_model,
        heuristic_epsilon,
        exact_model,
        exact_epsilon,
        solver_obj,
    )
    try:
        result_bin_matrix, logger = divide_and_conquer_strategy(io_config)
    except DivideAndConquerStrategyError as error:
        error.logger().write_yaml(output_directory)
        _LOGGER.critical(str(error))
    else:
        __finalize(result_bin_matrix, logger, output_directory)


def __format_logger(debug: bool) -> None:
    """Format logger."""
    handler = logging.StreamHandler(sys.stdout)
    if debug:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s %(name)s [%(levelname)s] %(message)s",
    )
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    log_filter = logging.Filter("qbc_dsbm")
    _LOGGER.addFilter(log_filter)


def __init_output_directory(output_directory: Path) -> None:
    try:
        output_directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        _LOGGER.critical("Output directory already exists: %s", output_directory)
        sys.exit(1)


def __create_solver_obj(
    solver: SolverChoice,
    solve_time_lim: int | None,
    solver_log: bool,
) -> Solver:
    match solver:
        case SolverChoice.CBC:
            return CBCSolver(
                time_limit=solve_time_lim,
                print_log=solver_log,
            )
        case SolverChoice.GUROBI:
            return GurobiSolver(
                time_limit=solve_time_lim,
                print_log=solver_log,
            )
        case _:
            _LOGGER.critical("Unknown solver: %s", solver)
            sys.exit(1)


def __finalize(
    result_bin_matrix: BinMatrix,
    logger: DivCqrStrategyLogger | UniqueStrategyLogger,
    output_directory: Path,
) -> None:
    logger.write_yaml(output_directory)
    result_bin_matrix.to_csv(output_directory / "result_bin_matrix.csv")


def main() -> None:
    """Execute the typer app."""
    __APP()


if __name__ == "__main__":
    main()
