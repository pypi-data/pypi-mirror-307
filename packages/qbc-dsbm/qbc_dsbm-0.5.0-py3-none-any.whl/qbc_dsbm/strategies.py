"""Solving strategies."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from qbc_dsbm import BCModels, QBCExactModels, QBCHeuristicModels
from qbc_dsbm.binary_matrix import BinMatrix, BinMatrixStats

if TYPE_CHECKING:
    from qbc_dsbm.io_config import IOConfig, IOConfigDivCqr
    from qbc_dsbm.models.views import ModelSolveStats

import logging

from qbc_dsbm.loggers import DivCqrStrategyLogger, UniqueStrategyLogger
from qbc_dsbm.models.views import ModelLPMILPStats
from qbc_dsbm.solve_problems import (
    ModelFindsDegeneratedMatrixError,
    SolveError,
    solve_exact_dsbm,
    solve_heuristic_dsbm,
    solve_konig,
)

_LOGGER = logging.getLogger(__name__)


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
def unique_strategy(io_config: IOConfig) -> tuple[BinMatrix, UniqueStrategyLogger]:
    """Solve the unique strategy.

    Parameters
    ----------
    io_config : IOConfig
        IO config

    Returns
    -------
    BinMatrix
        Sub-binary matrix
    UniqueStrategyLogger
        Logger

    Raises
    ------
    UniqueStrategyError
        The unique strategy failed

    """
    init_bin_matrix = BinMatrix.from_csv(io_config.csv_path())
    logger = UniqueStrategyLogger(
        io_config,
        BinMatrixStats.from_bin_matrix(init_bin_matrix),
    )

    _LOGGER.info("Input / Output config:\n%s\n", io_config)
    _LOGGER.info(
        "Initial binary matrix stats:\n%s\n",
        str(logger.init_bin_matrix()),
    )

    model = io_config.model()
    solve_stats: ModelSolveStats
    try:
        if model in QBCExactModels:
            result_bin_matrix, solve_stats = solve_exact_dsbm(
                init_bin_matrix,
                cast(QBCExactModels, model),
                io_config.epsilon(),
                io_config.solver(),
                min_number_of_rows=io_config.min_number_of_rows(),
                min_number_of_columns=io_config.min_number_of_columns(),
                check_satisfiability=io_config.check_satisfiability(),
            )
        elif model in BCModels:
            result_bin_matrix, solve_stats = solve_konig(
                init_bin_matrix,
                cast(BCModels, model),
                io_config.solver(),
            )
        elif model in QBCHeuristicModels:
            result_bin_matrix, solve_stats = solve_heuristic_dsbm(
                init_bin_matrix,
                cast(QBCHeuristicModels, model),
                io_config.epsilon(),
                io_config.solver(),
            )
    except (
        ModelFindsDegeneratedMatrixError,
        SolveError,
    ) as error:
        if isinstance(error, ModelFindsDegeneratedMatrixError):
            logger.add_solve_stats(error.solve_stats())
        elif isinstance(error, SolveError):
            logger.add_solve_stats(error.error().solve_stats())
        _LOGGER.info(
            "Model solve stats:\n%s\n",
            logger.model_solve_stats(),
        )
        _LOGGER.critical(str(error))
        raise UniqueStrategyError(logger) from error
    logger.add_solve_stats(solve_stats)
    logger.add_result_bin_matrix(
        BinMatrixStats.from_bin_matrix(result_bin_matrix),
    )
    _LOGGER.info(
        "Model solve stats:\n%s\n",
        logger.model_solve_stats(),
    )
    _LOGGER.info(
        "Result binary matrix stats:\n%s\n",
        str(logger.result_bin_matrix()),
    )
    return result_bin_matrix, logger


def divide_and_conquer_strategy(
    io_config: IOConfigDivCqr,
) -> tuple[BinMatrix, DivCqrStrategyLogger]:
    """Solve the divide-and-conquer strategy.

    Parameters
    ----------
    io_config : IOConfigDivCqr
        IO configuration

    Returns
    -------
    BinMatrix
        Binary matrix
    DivCqrStrategyLogger
        Logger

    Raises
    ------
    DivideAndConquerStrategyError
        If the final matrix is degenerated
        or if the solver time limit is reached

    """
    init_bin_matrix = BinMatrix.from_csv(io_config.csv_path())
    logger = DivCqrStrategyLogger(
        io_config,
        BinMatrixStats.from_bin_matrix(init_bin_matrix),
    )

    _LOGGER.info("Input / Output config:\n%s\n", io_config)
    _LOGGER.info(
        "Initial binary matrix stats:\n%s\n",
        str(logger.init_bin_matrix()),
    )

    _LOGGER.info(
        "D&C: solving heuristic problem %s",
        io_config.heuristic_model().value,
    )
    try:
        smaller_bin_matrix, heuristic_solve_stats = solve_heuristic_dsbm(
            init_bin_matrix,
            io_config.heuristic_model(),
            io_config.heuristic_epsilon(),
            io_config.solver(),
        )
    except ModelFindsDegeneratedMatrixError as error:
        _LOGGER.info("Submatrix degenerated, keep original matrix")
        smaller_bin_matrix = init_bin_matrix
        heuristic_solve_stats = error.solve_stats()
    except SolveError as error:
        logger.add_heuristic_solve_stats(error.error().solve_stats())
        _LOGGER.info("Solve stats:\n%s\n", logger.heuristic_solve_stats())
        _LOGGER.critical(str(error))
        raise DivideAndConquerStrategyError(logger) from error

    logger.add_heuristic_solve_stats(heuristic_solve_stats)
    logger.add_heuristic_result_bin_matrix(
        BinMatrixStats.from_bin_matrix(smaller_bin_matrix),
    )
    _LOGGER.info(
        "Heuristic solve stats:\n%s\n",
        logger.heuristic_solve_stats(),
    )
    _LOGGER.info(
        "Heuristic result binary matrix stats:\n%s\n",
        str(logger.heuristic_result_bin_matrix()),
    )
    _LOGGER.info(
        "D&C: solving exact problem %s",
        io_config.exact_model().value,
    )
    try:
        exact_result_bin_matrix, exact_solve_stats = solve_exact_dsbm(
            smaller_bin_matrix,
            io_config.exact_model(),
            io_config.exact_epsilon(),
            io_config.solver(),
        )
    except (ModelFindsDegeneratedMatrixError, SolveError) as error:
        if isinstance(error, ModelFindsDegeneratedMatrixError):
            logger.add_exact_solve_stats(cast(ModelLPMILPStats, error.solve_stats()))
        elif isinstance(error, SolveError):
            logger.add_exact_solve_stats(
                cast(ModelLPMILPStats, error.error().solve_stats()),
            )
        _LOGGER.info("Solve stats:\n%s\n", logger.exact_solve_stats())
        _LOGGER.critical(str(error))
        raise DivideAndConquerStrategyError(logger) from error

    logger.add_exact_solve_stats(exact_solve_stats)
    logger.add_exact_result_bin_matrix(
        BinMatrixStats.from_bin_matrix(exact_result_bin_matrix),
    )
    _LOGGER.info(
        "Exact solve stats:\n%s\n",
        logger.exact_solve_stats(),
    )
    _LOGGER.info(
        "Exact result binary matrix stats:\n%s\n",
        str(logger.exact_result_bin_matrix()),
    )
    return exact_result_bin_matrix, logger


# ============================================================================ #
#                                  EXCEPTIONS                                  #
# ============================================================================ #
class UniqueStrategyError(Exception):
    """Unique strategy exception."""

    def __init__(self, logger: UniqueStrategyLogger) -> None:
        """Initialize the exception."""
        self._LOGGER: UniqueStrategyLogger = logger

    def logger(self) -> UniqueStrategyLogger:
        """Logger.

        Returns
        -------
        UniqueStrategyLogger
            Logger

        """
        return self._LOGGER

    def __str__(self) -> str:
        """Print the exception message."""
        return "Unique strategy error"


class DivideAndConquerStrategyError(Exception):
    """Divide and conquer strategy exception."""

    def __init__(self, logger: DivCqrStrategyLogger) -> None:
        """Initialize the exception."""
        self._LOGGER: DivCqrStrategyLogger = logger

    def logger(self) -> DivCqrStrategyLogger:
        """Logger.

        Returns
        -------
        DivCqrStrategyLogger
            Logger

        """
        return self._LOGGER

    def __str__(self) -> str:
        """Print the exception message."""
        return "Divide and conquer strategy error"
