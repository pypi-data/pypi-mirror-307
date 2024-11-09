"""Loggers module."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import yaml  # type: ignore[import-untyped]

from qbc_dsbm.binary_matrix import BinMatrixStats
from qbc_dsbm.io_config import IOConfig, IOConfigDivCqr
from qbc_dsbm.models.views import (
    ModelLPMILPStats,
    ModelLPStats,
    ModelSolveStats,
    ModelType,
)

_LOGGER = logging.getLogger(__name__)


# ============================================================================ #
#                                    CLASSES                                   #
# ============================================================================ #
class UniqueStrategyLogger:
    """Logger for the unique strategy."""

    __IO_CONFIG_KEY = "io_config"
    """IO config key."""

    __INIT_BIN_MATRIX_KEY = "init_bin_matrix"
    """Initial binary matrix key."""

    __MODEL_STATS_KEY = "model_solve_stats"
    """Model solve statistics key."""

    __RESULT_BIN_MATRIX_KEY = "result_bin_matrix"
    """Result binary matrix key."""

    __YAML_FILE: Path = Path("unique_strategy.yaml")
    """Unique strategy YAML file."""

    @classmethod
    def yaml_file(cls) -> Path:
        """Return the YAML file.

        Returns
        -------
        Path
            YAML file

        """
        return cls.__YAML_FILE

    @classmethod
    def from_yaml(cls, directory: Path) -> UniqueStrategyLogger:
        """Load the logger from the YAML file.

        Parameters
        ----------
        directory : Path
            Directory

        Returns
        -------
        UniqueStrategyLogger
            Unique strategy logger

        """
        with (directory / cls.yaml_file()).open(encoding="utf-8") as stream:
            yaml_dict = yaml.safe_load(stream)
        model_solve_stats: ModelSolveStats
        match ModelSolveStats.model_type_from_dict(yaml_dict[cls.__MODEL_STATS_KEY]):
            case ModelType.MILP:
                model_solve_stats = ModelLPMILPStats.from_dict(
                    yaml_dict[cls.__MODEL_STATS_KEY],
                )
            case ModelType.LP:
                model_solve_stats = ModelLPStats.from_dict(
                    yaml_dict[cls.__MODEL_STATS_KEY],
                )
            case _:
                _LOGGER.critical("Cannot recognize model type")
                sys.exit(1)
        return cls(
            io_config=IOConfig.from_dict(yaml_dict[cls.__IO_CONFIG_KEY]),
            init_bin_matrix=BinMatrixStats.from_dict(
                yaml_dict[cls.__INIT_BIN_MATRIX_KEY],
            ),
            model_solve_stats=model_solve_stats,
            result_bin_matrix=BinMatrixStats.from_dict(
                yaml_dict[cls.__RESULT_BIN_MATRIX_KEY],
            ),
        )

    def __init__(
        self,
        io_config: IOConfig,
        init_bin_matrix: BinMatrixStats,
        model_solve_stats: ModelSolveStats | None = None,
        result_bin_matrix: BinMatrixStats | None = None,
    ) -> None:
        """Initialize the logger."""
        self.__io_config: IOConfig = io_config
        self.__init_bin_matrix: BinMatrixStats = init_bin_matrix
        self.__model_solve_stats: ModelSolveStats | None = model_solve_stats
        self.__result_bin_matrix: BinMatrixStats | None = result_bin_matrix

    def io_config(self) -> IOConfig:
        """IO config.

        Returns
        -------
        IOConfig
            IO config

        """
        return self.__io_config

    def init_bin_matrix(self) -> BinMatrixStats:
        """Give the initial binary matrix.

        Returns
        -------
        BinMatrixStats
            Initial binary matrix

        """
        return self.__init_bin_matrix

    def model_solve_stats(self) -> ModelSolveStats | None:
        """Give the solve statistics.

        Returns
        -------
        ModelSolveStats | None
            Solve statistics

        """
        return self.__model_solve_stats

    def result_bin_matrix(self) -> BinMatrixStats | None:
        """Give the resulting binary matrix.

        Returns
        -------
        BinMatrixStats | None
            Result binary matrix

        """
        return self.__result_bin_matrix

    def add_solve_stats(self, model_solve_stats: ModelSolveStats) -> None:
        """Add Solve statistics.

        Parameters
        ----------
        model_solve_stats : ModelSolveStats
            Solve statistics

        """
        self.__model_solve_stats = model_solve_stats

    def add_result_bin_matrix(self, result_bin_matrix: BinMatrixStats) -> None:
        """Add result binary matrix.

        Parameters
        ----------
        result_bin_matrix : BinMatrixStats
            Result binary matrix

        """
        self.__result_bin_matrix = result_bin_matrix

    def write_yaml(self, directory: Path) -> None:
        """Write YAML.

        Parameters
        ----------
        directory : Path
            Output directory

        """
        with (directory / self.yaml_file()).open("w", encoding="utf-8") as yaml_out:
            yaml_out.write(
                yaml.dump(
                    {
                        self.__IO_CONFIG_KEY: (self.__io_config.to_dict()),
                        self.__INIT_BIN_MATRIX_KEY: (self.__init_bin_matrix.to_dict()),
                        self.__MODEL_STATS_KEY: (
                            self.__model_solve_stats.to_dict()
                            if self.__model_solve_stats is not None
                            else None
                        ),
                        self.__RESULT_BIN_MATRIX_KEY: (
                            self.__result_bin_matrix.to_dict()
                            if self.__result_bin_matrix is not None
                            else None
                        ),
                    },
                    sort_keys=False,
                ),
            )


class DivCqrStrategyLogger:
    """Logger for the divide-and-conquer strategy."""

    __IO_CONFIG_KEY = "io_config"
    """IO config key."""

    __INIT_BIN_MATRIX_KEY = "init_bin_matrix"
    """Initial binary matrix key."""

    __HEURISTIC_SOLVE_STATS_KEY = "heuristic_solve_stats"
    """Heuristic Solve statistics key."""

    __HEURISTIC_RESULT_BIN_MATRIX_KEY = "heuristic_result_bin_matrix"
    """Heuristic result binary matrix key."""

    __EXACT_SOLVE_STATS_KEY = "exact_solve_stats"
    """Exact Solve statistics key."""

    __EXACT_RESULT_BIN_MATRIX_KEY = "exact_result_bin_matrix"
    """Exact result binary matrix key."""

    __YAML_FILE: Path = Path("divcqr_strategy.yaml")
    """DivCqr strategy YAML file."""

    @classmethod
    def yaml_file(cls) -> Path:
        """Return the YAML file.

        Returns
        -------
        Path
            YAML file

        """
        return cls.__YAML_FILE

    @classmethod
    def from_yaml(cls, directory: Path) -> DivCqrStrategyLogger:
        """Instantiate from YAML.

        Parameters
        ----------
        directory : Path
            Directory

        Returns
        -------
        DivCqrStrategyLogger
            DivCqr strategy logger

        """
        with (directory / cls.yaml_file()).open(encoding="utf-8") as stream:
            yaml_dict = yaml.safe_load(stream)
        heuristic_solve_stats: ModelSolveStats
        match ModelSolveStats.model_type_from_dict(
            yaml_dict[cls.__HEURISTIC_SOLVE_STATS_KEY],
        ):
            case ModelType.MILP:
                heuristic_solve_stats = ModelLPMILPStats.from_dict(
                    yaml_dict[cls.__HEURISTIC_SOLVE_STATS_KEY],
                )
            case ModelType.LP:
                heuristic_solve_stats = ModelLPStats.from_dict(
                    yaml_dict[cls.__HEURISTIC_SOLVE_STATS_KEY],
                )
            case _:
                _LOGGER.critical("Cannot recognize exact model type")
                sys.exit(1)
        return cls(
            io_config=IOConfigDivCqr.from_dict(yaml_dict[cls.__IO_CONFIG_KEY]),
            init_bin_matrix=BinMatrixStats.from_dict(
                yaml_dict[cls.__INIT_BIN_MATRIX_KEY],
            ),
            heuristic_solve_stats=heuristic_solve_stats,
            heuristic_result_bin_matrix=BinMatrixStats.from_dict(
                yaml_dict[cls.__HEURISTIC_RESULT_BIN_MATRIX_KEY],
            ),
            exact_solve_stats=ModelLPMILPStats.from_dict(
                yaml_dict[cls.__EXACT_SOLVE_STATS_KEY],
            ),
            exact_result_bin_matrix=BinMatrixStats.from_dict(
                yaml_dict[cls.__EXACT_RESULT_BIN_MATRIX_KEY],
            ),
        )

    def __init__(  # noqa: PLR0913
        self,
        io_config: IOConfigDivCqr,
        init_bin_matrix: BinMatrixStats,
        heuristic_solve_stats: ModelSolveStats | None = None,
        heuristic_result_bin_matrix: BinMatrixStats | None = None,
        exact_solve_stats: ModelLPMILPStats | None = None,
        exact_result_bin_matrix: BinMatrixStats | None = None,
    ) -> None:
        """Initialize the logger."""
        self.__io_config: IOConfigDivCqr = io_config
        self.__init_bin_matrix: BinMatrixStats = init_bin_matrix
        self.__heuristic_solve_stats: ModelSolveStats | None = heuristic_solve_stats
        self.__heuristic_result_bin_matrix: BinMatrixStats | None = (
            heuristic_result_bin_matrix
        )
        self.__exact_solve_stats: ModelLPMILPStats | None = exact_solve_stats
        self.__exact_result_bin_matrix: BinMatrixStats | None = exact_result_bin_matrix

    def io_config(self) -> IOConfigDivCqr:
        """IO config.

        Returns
        -------
        IOConfigDivCqr
            IO config

        """
        return self.__io_config

    def init_bin_matrix(self) -> BinMatrixStats:
        """Give the initial binary matrix.

        Returns
        -------
        BinMatrixStats
            Initial binary matrix

        """
        return self.__init_bin_matrix

    def heuristic_solve_stats(self) -> ModelSolveStats | None:
        """Give the heuristic Solve statistics.

        Returns
        -------
        ModelSolveStats | None
            Heuristic Solve statistics

        """
        return self.__heuristic_solve_stats

    def heuristic_result_bin_matrix(self) -> BinMatrixStats | None:
        """Give the heuristic resulting binary matrix.

        Returns
        -------
        BinMatrixStats | None
            Heuristic result binary matrix

        """
        return self.__heuristic_result_bin_matrix

    def exact_solve_stats(self) -> ModelLPMILPStats | None:
        """Give the exact solve statistics.

        Returns
        -------
        ModelLPMILPStats | None
            Exact solve statistics

        """
        return self.__exact_solve_stats

    def exact_result_bin_matrix(self) -> BinMatrixStats | None:
        """Give the exact resulting binary matrix.

        Returns
        -------
        BinMatrixStats | None
            Exact result binary matrix

        """
        return self.__exact_result_bin_matrix

    def add_heuristic_solve_stats(
        self,
        heuristic_solve_stats: ModelSolveStats,
    ) -> None:
        """Add heuristic solve statistics.

        Parameters
        ----------
        heuristic_solve_stats : ModelSolveStats
            Heuristic solve statistics

        """
        self.__heuristic_solve_stats = heuristic_solve_stats

    def add_heuristic_result_bin_matrix(
        self,
        heuristic_result_bin_matrix: BinMatrixStats,
    ) -> None:
        """Add heuristic result binary matrix.

        Parameters
        ----------
        heuristic_result_bin_matrix : BinMatrixStats
            Heuristic result binary matrix

        """
        self.__heuristic_result_bin_matrix = heuristic_result_bin_matrix

    def add_exact_solve_stats(self, exact_solve_stats: ModelLPMILPStats) -> None:
        """Add exact solve statistics.

        Parameters
        ----------
        exact_solve_stats : ModelLPMILPStats
            Exact solve statistics

        """
        self.__exact_solve_stats = exact_solve_stats

    def add_exact_result_bin_matrix(
        self,
        exact_result_bin_matrix: BinMatrixStats,
    ) -> None:
        """Add exact result binary matrix.

        Parameters
        ----------
        exact_result_bin_matrix : BinMatrixStats
            Exact result binary matrix

        """
        self.__exact_result_bin_matrix = exact_result_bin_matrix

    def write_yaml(self, directory: Path) -> None:
        """Write YAML.

        Parameters
        ----------
        directory : Path
            Output directory

        """
        with (directory / self.yaml_file()).open("w", encoding="utf-8") as yaml_out:
            yaml_out.write(
                yaml.dump(
                    {
                        self.__IO_CONFIG_KEY: (self.__io_config.to_dict()),
                        self.__INIT_BIN_MATRIX_KEY: (self.__init_bin_matrix.to_dict()),
                        self.__HEURISTIC_SOLVE_STATS_KEY: (
                            self.__heuristic_solve_stats.to_dict()
                            if self.__heuristic_solve_stats is not None
                            else None
                        ),
                        self.__HEURISTIC_RESULT_BIN_MATRIX_KEY: (
                            self.__heuristic_result_bin_matrix.to_dict()
                            if self.__heuristic_result_bin_matrix is not None
                            else None
                        ),
                        self.__EXACT_SOLVE_STATS_KEY: (
                            self.__exact_solve_stats.to_dict()
                            if self.__exact_solve_stats is not None
                            else None
                        ),
                        self.__EXACT_RESULT_BIN_MATRIX_KEY: (
                            self.__exact_result_bin_matrix.to_dict()
                            if self.__exact_result_bin_matrix is not None
                            else None
                        ),
                    },
                    sort_keys=False,
                ),
            )
