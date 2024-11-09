"""CLI module."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import typer

from qbc_dsbm import BCModels, QBCExactModels, QBCHeuristicModels, UniqueModels


class SolverChoice(Enum):
    """Solver choice."""

    GUROBI = "Gurobi"
    CBC = "CBC"


class UniqueModelChoices(Enum):
    """Unique model choices."""

    MAX_ONES = QBCExactModels.MAX_ONES.value
    MAX_SURFACE = QBCExactModels.MAX_SURFACE.value
    MAX_PERIMETER = QBCExactModels.MAX_PERIMETER.value
    MAX_ONES_COMPACT = QBCExactModels.MAX_ONES_COMPACT.value

    KONIG_V = BCModels.KONIG_V.value
    KONIG_E = BCModels.KONIG_E.value

    MIN_DEL_RC = QBCHeuristicModels.MIN_DEL_RC.value
    MIN_DEL_ROWS = QBCHeuristicModels.MIN_DEL_ROWS.value
    MIN_DEL_COLS = QBCHeuristicModels.MIN_DEL_COLS.value
    MIN_DEL_ROWS_RELAX = QBCHeuristicModels.MIN_DEL_ROWS_RELAX.value
    MIN_DEL_COLS_RELAX = QBCHeuristicModels.MIN_DEL_COLS_RELAX.value
    MIN_DEL_ONES = QBCHeuristicModels.MIN_DEL_ONES.value
    KP_QB = QBCHeuristicModels.KP_QB.value

    def to_unique_model(self) -> UniqueModels:
        """Convert to unique model.

        Returns
        -------
        UniqueModels
            Unique model

        """
        with suppress(ValueError):
            return QBCExactModels(self.value)
        with suppress(ValueError):
            return BCModels(self.value)
        return QBCHeuristicModels(self.value)


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
#
# Common args/opts
#
@dataclass
class CommonArgs:
    """Common args and opts."""

    ARG_CSV_PATH = typer.Argument(parser=Path, help="Binary matrix CSV file path")

    OPT_SOLVER_DEF = SolverChoice.CBC
    OPT_SOLVER = typer.Option(
        default=OPT_SOLVER_DEF.value,
        help="The solver to use",
    )

    OPT_SOLVE_TIME_LIM_DEF: int | None = None
    OPT_SOLVE_TIME_LIM = typer.Option(
        default=OPT_SOLVE_TIME_LIM_DEF,
        help="Solve time limit in seconds",
    )

    OPT_SOLVER_PRINT_LOG_DEF = False
    OPT_SOLVER_PRINT_LOG = typer.Option(
        default=OPT_SOLVER_PRINT_LOG_DEF,
        help="Print solver log",
    )

    OPT_OUTDIR_DEF = Path("./qbc_dsbm_results")
    OPT_OUTDIR = typer.Option(
        default=OPT_OUTDIR_DEF,
        help="The output directory path",
    )

    OPT_DEBUG_DEF = False
    OPT_DEBUG = typer.Option(
        default=OPT_DEBUG_DEF,
        help="Debug mode",
    )


#
# Command unique
#
@dataclass
class UniqueArgs:
    """Unique args and opts."""

    ARG_MODEL = typer.Argument(
        help="The model to use",
    )

    OPT_EPSILON_DEF = 0.0
    OPT_EPSILON = typer.Option(
        default=OPT_EPSILON_DEF,
        help="Remaining zeros percentage",
    )

    OPT_MIN_NUMBER_OF_ROWS = typer.Option(
        default=0,
        help="Minimum number of rows",
    )

    OPT_MIN_NUMBER_OF_COLUMNS = typer.Option(
        default=0,
        help="Minimum number of columns",
    )

    OPT_CHECK_SATISFIABILITY = typer.Option(
        default=False,
        help="Just check the satisfiability, do not solve an optimization problem",
    )


#
# Command divcqr
#
@dataclass
class DivCqrArgs:
    """DivCqr args and opts."""

    ARG_HEURISTIC_MODEL = typer.Argument(
        help="The heuristic model to use",
    )

    ARG_HEURISTIC_EPSILON = typer.Argument(
        help="The heuristic epsilon to use",
    )

    ARG_EXACT_MODEL = typer.Argument(
        help="The exact model to use",
    )

    ARG_EXACT_EPSILON = typer.Argument(
        help="The exact epsilon to use",
    )
