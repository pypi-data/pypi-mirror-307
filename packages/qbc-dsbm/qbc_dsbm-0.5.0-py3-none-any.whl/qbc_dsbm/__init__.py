"""Init file for module path shortcuts."""

from __future__ import annotations

from enum import Enum


# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
class QBCExactModels(Enum):
    """QBC exact model enum."""

    MAX_ONES = "max_ones"
    MAX_SURFACE = "max_surface"
    MAX_PERIMETER = "max_perimeter"
    MAX_ONES_COMPACT = "max_ones_compact"


class BCModels(Enum):
    """BC model enum."""

    KONIG_V = "König_V"
    KONIG_E = "König_E"


class QBCHeuristicModels(Enum):
    """QBC heuristic model enum."""

    MIN_DEL_RC = "min_del_rc"
    MIN_DEL_ROWS = "min_del_rows"
    MIN_DEL_COLS = "min_del_cols"
    MIN_DEL_ROWS_RELAX = "min_del_rows_relax"
    MIN_DEL_COLS_RELAX = "min_del_cols_relax"
    MIN_DEL_ONES = "min_del_ones"
    KP_QB = "KP_QB"


UniqueModels = QBCExactModels | BCModels | QBCHeuristicModels


# ============================================================================ #
#                                  EXCEPTIONS                                  #
# ============================================================================ #
class InvalidModelNameError(Exception):
    """Invalid model name."""

    def __init__(self, invalid_model_str: str) -> None:
        """Initialize exception."""
        self.__invalid_model_str = invalid_model_str

    def invalid_model_str(self) -> str:
        """Invalid model string.

        Returns
        -------
        str
            Invalid model string

        """
        return self.__invalid_model_str

    def __str__(self) -> str:
        """Give the string representation."""
        return f"Invalid model name: {self.__invalid_model_str}"


def string_to_model_enum(model_str: str) -> UniqueModels:
    """Convert string to model enum.

    Parameters
    ----------
    model_str : str
        Model string

    Returns
    -------
    UniqueModels
        Model enum

    Raises
    ------
    InvalidModelNameError
        Invalid model name

    """
    if model_str in QBCExactModels.__members__:
        return QBCExactModels[model_str]
    if model_str in BCModels.__members__:
        return BCModels[model_str]
    if model_str in QBCHeuristicModels.__members__:
        return QBCHeuristicModels[model_str]
    raise InvalidModelNameError(model_str)
