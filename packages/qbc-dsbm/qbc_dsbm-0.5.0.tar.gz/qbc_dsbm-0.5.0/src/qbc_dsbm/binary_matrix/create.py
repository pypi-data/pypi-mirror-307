"""Binary matrix create module."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

from qbc_dsbm.binary_matrix.items import BinMatrix

if TYPE_CHECKING:
    from qbc_dsbm.binary_matrix import configs

_LOGGER = logging.getLogger(__name__)


def generate_bin_dataframe(
    number_of_rows: int,
    number_of_columns: int,
    sparsicity: float,
) -> pd.DataFrame:
    """Generate a binary dataframe.

    Parameters
    ----------
    number_of_rows : int
        Number of rows
    number_of_columns : int
        Number of columns
    sparsicity : float
        Sparsicity of the matrix

    Returns
    -------
    pd.DataFrame
        A binary dataframe

    """
    data = np.random.default_rng().binomial(
        1,
        p=(1 - sparsicity),
        size=(number_of_rows, number_of_columns),
    )
    return pd.DataFrame(
        data,
        index=pd.Index(range(number_of_rows), name="row"),
        columns=pd.Index(range(number_of_columns), name="column"),
    )


def encapsulate_permutate_bin_dataframe(
    number_of_rows: int,
    number_of_columns: int,
    sparsicity: float,
    number_of_rows_super: int,
    number_of_columns_super: int,
) -> tuple[BinMatrix, BinMatrix]:
    """Create a binary dataframe containing a hidden binary dataframe.

    There exists a permutation of the rows and the columns of the super
    binary matrix such its top-left corner contains the smaller binary matrix.

    Parameters
    ----------
    number_of_rows : int
        Number of rows of the contained matrix
    number_of_columns : int
        Number of columns of the contained matrix
    sparsicity : float
        Sparsicity of the contained binary matrix
    number_of_rows_super : int
        Number of rows of the containing matrix >= number_of_rows
    number_of_columns_super : int
        Number of columns of the containing matrix >= number_of_columns

    Returns
    -------
    BinMatrix
        Contained binary matrix
    BinMatrix
        Containing binary matrix

    Raises
    ------
    ValueError
        If number_of_rows_super < number_of_rows
        or if number_of_columns_super < number_of_columns

    """
    if number_of_rows_super < number_of_rows:
        msg = (
            "super number of rows < sub number of rows"
            f" ({number_of_rows_super} < {number_of_rows})"
        )
        raise ValueError(msg)
    if number_of_columns_super < number_of_columns:
        msg = (
            "super number of columns < sub number of columns"
            f" ({number_of_columns_super} < {number_of_columns})"
        )
        raise ValueError(msg)

    contained_dataframe = generate_bin_dataframe(
        number_of_rows,
        number_of_columns,
        sparsicity,
    )
    super_dataframe = pd.DataFrame(
        False,  # noqa: FBT003
        index=range(number_of_rows_super),
        columns=range(number_of_columns_super),
    )
    super_dataframe.update(contained_dataframe)
    return (
        BinMatrix.new_unsafe(contained_dataframe),
        BinMatrix.new_unsafe(
            super_dataframe.reindex(
                index=np.random.default_rng().permutation(super_dataframe.index),
                columns=np.random.default_rng().permutation(super_dataframe.columns),
            ),
        ),
    )


def generate_bin_matrix(
    number_of_rows: int,
    number_of_columns: int,
    sparsity: float,
) -> BinMatrix:
    """Generate a binary matrix.

    Parameters
    ----------
    number_of_rows : int
        Number of rows
    number_of_columns : int
        Number of columns
    sparsity : float
        Sparsity of the matrix

    Returns
    -------
    BinMatrix
        A binary matrix

    """
    return BinMatrix.new_unsafe(
        generate_bin_dataframe(number_of_rows, number_of_columns, sparsity),
    )


def complete_dataframe_with_knn(
    unfilled_df: pd.DataFrame,
    config: configs.KNNFillingConfig,
) -> BinMatrix | None:
    """Complete a dataframe with KNN.

    Parameters
    ----------
    unfilled_df : pd.DataFrame
        Dataframe with unfilled values
    config : bm_cfg.KNNFillingConfig
        KNN completion parameters

    Returns
    -------
    BinMatrix | None
        KNN-completed binary matrix or None if cannot be completed

    """
    _LOGGER.info("Complete the dataframe with KNN")
    _LOGGER.info("Configuration:\n%s\n", config)

    if unfilled_df.shape[0] < 2 or unfilled_df.shape[1] < 2:  # noqa: PLR2004
        return None

    imputer = KNNImputer(n_neighbors=config.number_of_neighbours())
    matrix = imputer.fit_transform(unfilled_df)
    matrix[(matrix >= config.threshold())] = 1
    matrix[(matrix < config.threshold())] = 0
    matrix = pd.DataFrame(
        matrix,
        index=unfilled_df.index,
        columns=unfilled_df.columns,
    )
    return BinMatrix(matrix)
