"""Problem solvers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable, Literal

if TYPE_CHECKING:
    from pulp import LpVariable

    from qbc_dsbm.models.views import ModelLPMILPStats, ModelSolveStats

from qbc_dsbm import BCModels, QBCExactModels, QBCHeuristicModels
from qbc_dsbm.bigraph import ZerosBiGraph
from qbc_dsbm.binary_matrix import BinMatrix, DegeneratedMatrixError
from qbc_dsbm.models.exact_dsbm import (
    max_ones,
    max_ones_compact,
    max_perimeter,
    max_surface,
)
from qbc_dsbm.models.heuristic_dsbm import (
    kp_qb,
    min_del_cols,
    min_del_cols_relax,
    min_del_ones,
    min_del_rc,
    min_del_rows,
    min_del_rows_relax,
)
from qbc_dsbm.models.konig import konig_e, konig_v
from qbc_dsbm.models.solvers import NoSolutionError, Solver, SolverTimeLimitReachedError

LOGGER = logging.getLogger(__name__)


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                  Exact DSBM                                  #
# ---------------------------------------------------------------------------- #
# REFACTOR use exact config
# REFACTOR each model should have its own command / config
def solve_exact_dsbm(
    bin_matrix: BinMatrix,
    model: QBCExactModels,
    epsilon: float,
    solver: Solver,
    min_number_of_rows: int = 0,
    min_number_of_columns: int = 0,  # XXX optional constraints
    warm_solution: BinMatrix | None = None,
    check_satisfiability: bool = False,  # noqa: FBT001, FBT002
) -> tuple[BinMatrix, ModelLPMILPStats]:
    """Solve exact DSBM problem.

    Parameters
    ----------
    bin_matrix : BinMatrix
        Binary matrix
    model : QBCExactModels
        Exact model
    epsilon : float
        Error rate
    solver : Solver
        Solver to use
    min_number_of_rows : int
        Minimum number of rows
    min_number_of_columns : int
        Minimum number of columns
    warm_solution : BinMatrix
        Warm solution
    check_satisfiability : bool
        Check satisfiability, do not solve an optimization problem

    Returns
    -------
    BinMatrix
        Sub-binary matrix
    SolveStats
        Solve statistics

    Raises
    ------
    SolveError
        The problem could not be solved
    ModelFindsDegeneratedMatrixError
        The model finds degenerated matrix

    """
    match model:
        case QBCExactModels.MAX_ONES:
            prob, row_choices, col_choices, _ = max_ones(bin_matrix, epsilon)
            vars_are_integers = True
        case QBCExactModels.MAX_ONES_COMPACT:
            prob, row_choices, col_choices, _ = max_ones_compact(
                bin_matrix,
                epsilon,
                min_number_of_rows=min_number_of_rows,
                min_number_of_columns=min_number_of_columns,
                warm_solution=warm_solution,
                check_satisfiability=check_satisfiability,
            )
            vars_are_integers = True
        case QBCExactModels.MAX_PERIMETER:
            prob, row_choices, col_choices, _ = max_perimeter(bin_matrix, epsilon)
            vars_are_integers = True
        case QBCExactModels.MAX_SURFACE:
            prob, row_choices, col_choices, _ = max_surface(bin_matrix, epsilon)
            vars_are_integers = True

    try:
        solve_stats = solver.solve_milp(prob, warm_start=(warm_solution is not None))
    except NoSolutionError as no_sol_err:
        raise SolveError(no_sol_err) from no_sol_err
    except SolverTimeLimitReachedError as time_lim_err:
        raise SolveError(time_lim_err) from time_lim_err

    row_mask, col_mask = __row_col_vertex_choices_to_masks(
        bin_matrix.number_of_rows(),
        bin_matrix.number_of_columns(),
        vars_are_integers,
        row_choices,
        col_choices,
        (False, True),
    )

    try:
        return bin_matrix.to_sub_matrix(row_mask, col_mask), solve_stats
    except DegeneratedMatrixError as degen_error:
        raise ModelFindsDegeneratedMatrixError(
            solve_stats,
            degen_error,
        ) from degen_error


# ---------------------------------------------------------------------------- #
#                                     König                                    #
# ---------------------------------------------------------------------------- #
def solve_konig(
    bin_matrix: BinMatrix,
    model: BCModels,
    solver: Solver,
) -> tuple[BinMatrix, ModelLPMILPStats]:
    """Solve bi-clique König problems.

    Parameters
    ----------
    bin_matrix : BinMatrix
        Binary matrix
    model : BCModels
        Biclique model
    solver : Solver
        Solver to use

    Returns
    -------
    BinMatrix
        Sub-binary matrix
    SolveStats
        Solve statistics

    Raises
    ------
    SolveError
        The problem could not be solved
    ModelFindsDegeneratedMatrixError
        The model finds degenerated matrix

    """
    bigraph = ZerosBiGraph.from_bin_matrix(bin_matrix)

    match model:
        case BCModels.KONIG_V:
            prob, u_vertex_choices, v_vertex_choices = konig_v(bigraph)
            vars_are_integers = True
        case BCModels.KONIG_E:
            prob, u_vertex_choices, v_vertex_choices = konig_e(bigraph)
            vars_are_integers = True

    try:
        solve_stats = solver.solve_milp(prob)
    except NoSolutionError as no_sol_err:
        raise SolveError(no_sol_err) from no_sol_err
    except SolverTimeLimitReachedError as time_lim_err:
        raise SolveError(time_lim_err) from time_lim_err

    row_mask, col_mask = __row_col_vertex_choices_to_masks(
        bigraph.card_u_bipart(),
        bigraph.card_v_bipart(),
        vars_are_integers,
        u_vertex_choices,
        v_vertex_choices,
        (True, False),
    )

    try:
        return bin_matrix.to_sub_matrix(row_mask, col_mask), solve_stats
    except DegeneratedMatrixError as degen_error:
        raise ModelFindsDegeneratedMatrixError(
            solve_stats,
            degen_error,
        ) from degen_error


# ---------------------------------------------------------------------------- #
#                                   Heuristic                                  #
# ---------------------------------------------------------------------------- #
def solve_heuristic_dsbm(  # noqa: C901
    bin_matrix: BinMatrix,
    model: QBCHeuristicModels,
    epsilon: float,
    solver: Solver,
) -> tuple[BinMatrix, ModelSolveStats]:
    """Solve heuristic DSBM problem.

    Parameters
    ----------
    bin_matrix : BinMatrix
        Binary matrix
    model : QBCHeuristicModels
        Quasi bi-clique heuristic model
    epsilon : float
        Error rate
    solver : Solver
        Solver to use

    Returns
    -------
    BinMatrix
        Sub-binary matrix
    ModelSolveStats
        Solve statistics

    Raises
    ------
    SolveError
        The problem could not be solved
    ModelFindsDegeneratedMatrixError
        The model finds degenerated matrix

    """
    bigraph = ZerosBiGraph.from_bin_matrix(bin_matrix)

    is_milp = True
    u_vertex_choices: Iterable[LpVariable] | None
    v_vertex_choices: Iterable[LpVariable] | None
    match model:
        case QBCHeuristicModels.MIN_DEL_ONES:
            prob, u_vertex_choices, v_vertex_choices, _ = min_del_ones(bigraph, epsilon)
            vars_are_integers = True
        case QBCHeuristicModels.MIN_DEL_RC:
            prob, u_vertex_choices, v_vertex_choices, _ = min_del_rc(bigraph, epsilon)
            vars_are_integers = True
        case QBCHeuristicModels.MIN_DEL_ROWS:
            prob, u_vertex_choices, _ = min_del_rows(bigraph, epsilon)
            v_vertex_choices = None
            vars_are_integers = True
        case QBCHeuristicModels.MIN_DEL_COLS:
            prob, v_vertex_choices, _ = min_del_cols(bigraph, epsilon)
            u_vertex_choices = None
            vars_are_integers = True
        case QBCHeuristicModels.MIN_DEL_ROWS_RELAX:
            is_milp = False
            prob, u_vertex_choices, _ = min_del_rows_relax(bigraph, epsilon)
            v_vertex_choices = None
            vars_are_integers = False
        case QBCHeuristicModels.MIN_DEL_COLS_RELAX:
            is_milp = False
            prob, v_vertex_choices, _ = min_del_cols_relax(bigraph, epsilon)
            u_vertex_choices = None
            vars_are_integers = False
        case QBCHeuristicModels.KP_QB:
            prob, u_vertex_choices, v_vertex_choices = kp_qb(bigraph, epsilon)
            vars_are_integers = True

    try:
        solve_stats = solver.solve_milp(prob) if is_milp else solver.solve_lp(prob)
    except NoSolutionError as no_sol_err:
        raise SolveError(no_sol_err) from no_sol_err
    except SolverTimeLimitReachedError as time_lim_err:
        raise SolveError(time_lim_err) from time_lim_err

    row_mask, col_mask = __row_col_vertex_choices_to_masks(
        bigraph.card_u_bipart(),
        bigraph.card_v_bipart(),
        vars_are_integers,
        u_vertex_choices,
        v_vertex_choices,
        (True, False),
    )

    try:
        return bin_matrix.to_sub_matrix(row_mask, col_mask), solve_stats
    except DegeneratedMatrixError as degen_error:
        raise ModelFindsDegeneratedMatrixError(
            solve_stats,
            degen_error,
        ) from degen_error


# ---------------------------------------------------------------------------- #
#                             LP Variables To Masks                            #
# ---------------------------------------------------------------------------- #
def __row_col_vertex_choices_to_masks(  # noqa: PLR0913
    n_row: int,
    n_col: int,
    vars_are_integers: bool,  # noqa: FBT001
    row_choices: Iterable[LpVariable] | None,
    col_choices: Iterable[LpVariable] | None,
    keep: tuple[bool, bool],
) -> tuple[list[bool], list[bool]]:
    masks: tuple[list[bool], list[bool]] = ([], [])
    for k, (choices, dim) in enumerate(
        (
            (row_choices, n_row),
            (col_choices, n_col),
        ),
    ):
        if choices is None:
            for _ in range(dim):
                masks[k].append(keep[0])
        else:
            for var in choices:
                masks[k].append(
                    keep[
                        __lp_var_value_to_bin_value(var)
                        if vars_are_integers
                        else __continuous_var_value_to_bin_value(var)
                    ],
                )
    return masks


def __lp_var_value_to_bin_value(var: LpVariable) -> Literal[0, 1]:
    if var.value() is None:
        LOGGER.warning("None variable value replaced by 1")
        var.setInitialValue(1)
    if var.value() == 1:
        return 1
    if var.value() == 0:
        return 0
    msg = f"Invalid bool value {var.value()}"
    raise ValueError(msg)


def __continuous_var_value_to_bin_value(var: LpVariable) -> Literal[0, 1]:
    if var.value() is None:
        LOGGER.warning("None variable value replaced by 1")
        var.setInitialValue(1)
    if var.value() == 1:
        return 1
    return 0


# ============================================================================ #
#                                   EXCEPTION                                  #
# ============================================================================ #
class SolveError(Exception):
    """Solve exception."""

    def __init__(self, error: SolverTimeLimitReachedError | NoSolutionError) -> None:
        """Initialize the exception."""
        self.__error: SolverTimeLimitReachedError | NoSolutionError = error

    def error(self) -> SolverTimeLimitReachedError | NoSolutionError:
        """Error.

        Returns
        -------
        SolverTimeLimitReachedError | NoSolutionError
            Error

        """
        return self.__error

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message

        """
        return f"Problem solving failed:\n{self.__error}\n"


class ModelFindsDegeneratedMatrixError(Exception):
    """Model finds degenerated matrix exception."""

    def __init__(
        self,
        solve_stats: ModelSolveStats,
        degen_error: DegeneratedMatrixError,
    ) -> None:
        """Initialize the exception."""
        self.__solve_stats: ModelSolveStats = solve_stats
        self.__degen_error: DegeneratedMatrixError = degen_error

    def solve_stats(self) -> ModelSolveStats:
        """Solve statistics.

        Returns
        -------
        SolveStats
            Solve statistics

        """
        return self.__solve_stats

    def degen_error(self) -> DegeneratedMatrixError:
        """Degenerated matrix error.

        Returns
        -------
        DegeneratedMatrixError
            Degenerated matrix error

        """
        return self.__degen_error

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message

        """
        return (
            f"The model finds degenerated matrix:\n"
            f"{self.__degen_error}\n"
            f"See the solve statistics:\n"
            f"{self.__solve_stats}"
        )
