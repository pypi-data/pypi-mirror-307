"""Binary matrix module."""

from qbc_dsbm.binary_matrix.configs import KNNFillingConfig
from qbc_dsbm.binary_matrix.create import (
    complete_dataframe_with_knn,
    encapsulate_permutate_bin_dataframe,
    generate_bin_dataframe,
    generate_bin_matrix,
)
from qbc_dsbm.binary_matrix.items import (
    BinMatrix,
    DegeneratedMatrixError,
    NotABinaryMatrixError,
)
from qbc_dsbm.binary_matrix.ops import (
    a_inter_b_columns,
    a_inter_b_rows,
    a_minus_b_columns,
    a_minus_b_rows,
)
from qbc_dsbm.binary_matrix.views import BinMatrixStats

__all__ = [
    "BinMatrix",
    "DegeneratedMatrixError",
    "NotABinaryMatrixError",
    "BinMatrixStats",
    "a_inter_b_columns",
    "a_inter_b_rows",
    "a_minus_b_columns",
    "a_minus_b_rows",
    "generate_bin_matrix",
    "generate_bin_dataframe",
    "encapsulate_permutate_bin_dataframe",
    "KNNFillingConfig",
    "complete_dataframe_with_knn",
]
