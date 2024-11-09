"""Input-output configurations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from qbc_dsbm import (
    QBCExactModels,
    QBCHeuristicModels,
    UniqueModels,
    string_to_model_enum,
)
from qbc_dsbm.models.solvers import Solver, solver_from_dict


# ============================================================================ #
#                                     CLASS                                    #
# ============================================================================ #
class IOConfig:
    """Input-output config class.

    Parameters
    ----------
    csv_path : Path
        CSV path
    model : UniqueModels
        Model
    epsilon : float
        Epsilon
    solver : Solver
        Solver

    """

    __KEY_CSV_PATH: str = "csv_path"
    __KEY_MODEL: str = "model"
    __KEY_EPSILON: str = "epsilon"
    __KEY_SOLVER: str = "solver"
    __KEY_MIN_NUMBER_OF_ROWS: str = "min_number_of_rows"
    __KEY_MIN_NUMBER_OF_COLUMNS: str = "min_number_of_columns"
    __KEY_CHECK_SATISFIABILITY: str = "check_satisfiability"

    @classmethod
    def from_dict(cls, io_config_dict: dict[str, Any]) -> IOConfig:
        """Convert dict to IOConfig.

        Parameters
        ----------
        io_config_dict : dict
            Dictionnary of IO config

        Returns
        -------
        IOConfig
            IOConfig

        """
        return cls(
            Path(io_config_dict[cls.__KEY_CSV_PATH]),
            string_to_model_enum(io_config_dict[cls.__KEY_MODEL]),
            io_config_dict[cls.__KEY_EPSILON],
            solver_from_dict(io_config_dict[cls.__KEY_SOLVER]),
            io_config_dict[cls.__KEY_MIN_NUMBER_OF_ROWS],
            io_config_dict[cls.__KEY_MIN_NUMBER_OF_COLUMNS],
            io_config_dict[cls.__KEY_CHECK_SATISFIABILITY],
        )

    def __init__(  # noqa: PLR0913
        self,
        csv_path: Path,
        model: UniqueModels,
        epsilon: float,
        solver: Solver,
        min_number_of_rows: int,
        min_number_of_columns: int,
        check_satisfiability: bool,  # noqa: FBT001
    ) -> None:
        """Initialize the configuration."""
        self.__csv_path: Path = csv_path
        self.__model: UniqueModels = model
        self.__epsilon: float = epsilon
        self.__solver: Solver = solver
        self.__min_number_of_rows: int = min_number_of_rows
        self.__min_number_of_columns: int = min_number_of_columns
        self.__check_satisfiability: bool = check_satisfiability

    def csv_path(self) -> Path:
        """CSV file path.

        Returns
        -------
        Path
            CSV file path

        """
        return self.__csv_path

    def model(self) -> UniqueModels:
        """Model string name.

        Returns
        -------
        UniqueModels
            Model string name

        """
        return self.__model

    def epsilon(self) -> float:
        """Epsilon.

        Returns
        -------
        float
            Epsilon

        """
        return self.__epsilon

    def solver(self) -> Solver:
        """Solver.

        Returns
        -------
        Solver
            Solver

        """
        return self.__solver

    def min_number_of_rows(self) -> int:
        """Minimum number of rows.

        Returns
        -------
        int
            Minimum number of rows

        """
        return self.__min_number_of_rows

    def min_number_of_columns(self) -> int:
        """Minimum number of columns.

        Returns
        -------
        int
            Minimum number of columns

        """
        return self.__min_number_of_columns

    def check_satisfiability(self) -> bool:
        """Check satisfiability.

        Returns
        -------
        bool
            Check satisfiability

        """
        return self.__check_satisfiability

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict.

        Returns
        -------
        dict[str, Any]
            Dictionary

        """
        return {
            self.__KEY_CSV_PATH: str(self.__csv_path),
            self.__KEY_MODEL: self.__model.value,
            self.__KEY_EPSILON: self.__epsilon,
            self.__KEY_SOLVER: self.__solver.to_dict(),
            self.__KEY_MIN_NUMBER_OF_ROWS: self.__min_number_of_rows,
            self.__KEY_MIN_NUMBER_OF_COLUMNS: self.__min_number_of_columns,
            self.__KEY_CHECK_SATISFIABILITY: self.__check_satisfiability,
        }

    def __str__(self) -> str:
        """Print the IOConfig parameters."""
        return "\n".join(
            [
                f"CSV path: {self.__csv_path}",
                f"Model name: {self.__model.value}",
                f"Epsilon: {self.__epsilon}",
                f"Solver: {self.__solver.name()}",
                f"Minimum number of rows: {self.__min_number_of_rows}",
                f"Minimum number of columns: {self.__min_number_of_columns}",
                f"Check satisfiability: {self.__check_satisfiability}",
            ],
        )


class IOConfigDivCqr:
    """Input-output config class for divide and conquer method.

    Parameters
    ----------
    csv_path : Path
        The path to the csv file
    heuristic_model : QBCHeuristicModelStringName
        The model to use
    heuristic_epsilon : float
        Percentage of errors (remaining zeros) in the result submatrix
    exact_model : QBCExactModelStringName
        The model to use
    exact_epsilon : float
        Percentage of errors (remaining zeros) in the result submatrix
    solver : Solver
        The solver to use

    """

    __KEY_CSV_PATH: str = "csv_path"
    __KEY_HEURISTIC_MODEL: str = "heuristic_model"
    __KEY_HEURISTIC_EPSILON: str = "heuristic_epsilon"
    __KEY_EXACT_MODEL: str = "exact_model"
    __KEY_EXACT_EPSILON: str = "exact_epsilon"
    __KEY_SOLVER: str = "solver"

    @classmethod
    def from_dict(cls, io_config_dict: dict[str, Any]) -> IOConfigDivCqr:
        """Instantiate IOConfigDivCqr from dict.

        Parameters
        ----------
        io_config_dict : dict[str, Any]
            Dictionary containing the IOConfigDivCqr parameters

        Returns
        -------
        IOConfigDivCqr
            IOConfigDivCqr

        """
        return cls(
            Path(io_config_dict[cls.__KEY_CSV_PATH]),
            QBCHeuristicModels(io_config_dict[cls.__KEY_HEURISTIC_MODEL]),
            io_config_dict[cls.__KEY_HEURISTIC_EPSILON],
            QBCExactModels(io_config_dict[cls.__KEY_EXACT_MODEL]),
            io_config_dict[cls.__KEY_EXACT_EPSILON],
            solver_from_dict(io_config_dict[cls.__KEY_SOLVER]),
        )

    def __init__(  # noqa: PLR0913
        self,
        csv_path: Path,
        heuristic_model: QBCHeuristicModels,
        heuristic_epsilon: float,
        exact_model: QBCExactModels,
        exact_epsilon: float,
        solver: Solver,
    ) -> None:
        """Initialize the configuration."""
        self.__csv_path: Path = csv_path
        self.__heuristic_model: QBCHeuristicModels = heuristic_model
        self.__heuristic_epsilon: float = heuristic_epsilon
        self.__exact_model: QBCExactModels = exact_model
        self.__exact_epsilon: float = exact_epsilon
        self.__solver: Solver = solver

    def csv_path(self) -> Path:
        """CSV file path.

        Returns
        -------
        Path
            CSV file path

        """
        return self.__csv_path

    def heuristic_model(self) -> QBCHeuristicModels:
        """Heuristic model.

        Returns
        -------
        QBCHeuristicModels
            Heuristic model

        """
        return self.__heuristic_model

    def heuristic_epsilon(self) -> float:
        """Epsilon for the heuristic model.

        Returns
        -------
        float
            Epsilon

        """
        return self.__heuristic_epsilon

    def exact_model(self) -> QBCExactModels:
        """Exact model.

        Returns
        -------
        QBCExactModels
            Exact model

        """
        return self.__exact_model

    def exact_epsilon(self) -> float:
        """Epsilon for the exact model.

        Returns
        -------
        float
            Epsilon

        """
        return self.__exact_epsilon

    def solver(self) -> Solver:
        """Solver.

        Returns
        -------
        Solver
            Solver

        """
        return self.__solver

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict.

        Returns
        -------
        dict[str, Any]
            Dictionary

        """
        return {
            self.__KEY_CSV_PATH: str(self.__csv_path),
            self.__KEY_HEURISTIC_MODEL: self.__heuristic_model.value,
            self.__KEY_HEURISTIC_EPSILON: self.__heuristic_epsilon,
            self.__KEY_EXACT_MODEL: self.__exact_model.value,
            self.__KEY_EXACT_EPSILON: self.__exact_epsilon,
            self.__KEY_SOLVER: self.__solver.to_dict(),
        }

    def __str__(self) -> str:
        """Print the IOConfigDAC parameters."""
        return "\n".join(
            [
                "----------",
                "Parameters",
                "----------",
                "",
                f"CSV path: {self.__csv_path}",
                f"Heuristic model name: {self.__heuristic_model.value}",
                f"Heuristic epsilon: {self.__heuristic_epsilon}",
                f"Exact model name: {self.__exact_model.name}",
                f"Exact epsilon: {self.__exact_epsilon}",
                f"Solver: {self.__solver.name()}",
            ],
        )
