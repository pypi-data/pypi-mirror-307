"""Binary matrix items module."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Hashable

if TYPE_CHECKING:
    from pathlib import Path

from typing import Any, Iterable, Iterator, Literal

import numpy as np
import pandas as pd


# ============================================================================ #
#                                    CLASSES                                   #
# ============================================================================ #
class BinMatrix:
    """Binary matrix.

    The given dataframe must only contain 0-1 values.

    Raises
    ------
    NotABinaryMatrixError
        The non 0-1 values are not replaced and the safe option is set

    """

    @classmethod
    def new_unsafe(
        cls,
        bin_matrix: pd.DataFrame,
        replace_value_map: dict[Any, Literal[0, 1]] | None = None,
    ) -> BinMatrix:
        """Create a new binary matrix without verification.

        Parameters
        ----------
        bin_matrix : pd.DataFrame
            Binary matrix
        replace_value_map : dict
            Replace value map

        Returns
        -------
        BinMatrix
            A binary matrix

        """
        __df: pd.DataFrame = bin_matrix.copy()
        # Replace non 0-1 values
        if replace_value_map is not None:
            if None in replace_value_map:
                replace_value_map[np.nan] = replace_value_map.pop(None)
            __df = __df.replace(replace_value_map)

        self = cls.__new__(cls)

        self.__dataframe = __df
        self.__number_of_ones = int((self.__dataframe == 1).sum().sum())
        return self

    @classmethod
    def from_csv(
        cls,
        csv_path: Path,
        replace_value_map: dict[Any, Literal[0, 1]] | None = None,
    ) -> BinMatrix:
        """Instantiate a binary matrix from CSV file.

        Parameters
        ----------
        csv_path : Path
            CSV path
        replace_value_map : dict[Any, Literal[0, 1]], optional
            Replace value map

        Returns
        -------
        BinMatrix
            A binary matrix

        """
        df: pd.DataFrame = pd.read_csv(csv_path, header=0, index_col=0)
        return cls(df, replace_value_map=replace_value_map)

    @classmethod
    def unsafe_from_csv(
        cls,
        csv_path: Path,
        replace_value_map: dict[Any, Literal[0, 1]] | None = None,
    ) -> BinMatrix:
        """Instantiate a binary matrix from CSV file.

        Parameters
        ----------
        csv_path : Path
            CSV path
        replace_value_map : dict[Any, Literal[0, 1]], optional
            Replace value map

        Returns
        -------
        BinMatrix
            A binary matrix

        """
        df: pd.DataFrame = pd.read_csv(csv_path, header=0, index_col=0)
        return cls.new_unsafe(df, replace_value_map=replace_value_map)

    def __init__(
        self,
        bin_matrix: pd.DataFrame,
        replace_value_map: dict[Any, Literal[0, 1]] | None = None,
    ) -> None:
        """Instantiate a binary matrix.

        It verifies that the given dataframe only contains 0-1 values.
        """
        __df: pd.DataFrame = bin_matrix.copy()
        # Replace non 0-1 values
        if replace_value_map is not None:
            if None in replace_value_map:
                replace_value_map[np.nan] = replace_value_map.pop(None)
            __df = __df.replace(replace_value_map)

        # Verify it takes value in 0, 1
        for value in __df.to_numpy().flatten():
            if value not in (0, 1):
                raise NotABinaryMatrixError(value)

        self.__dataframe = __df
        self.__number_of_ones = int((self.__dataframe == 1).sum().sum())

    def to_dataframe(self) -> pd.DataFrame:
        """Binary matrix dataframe.

        Returns
        -------
        pd.DataFrame
            Binary matrix dataframe

        """
        return self.__dataframe

    def cell_values(self) -> Iterator[tuple[tuple[int, int], Literal[0, 1]]]:
        """Cell values.

        Yields
        ------
        tuple of int
            Cell coordinates
        Literal[0, 1]
            Cell value

        """
        for i in range(self.__dataframe.shape[0]):
            for j in range(self.__dataframe.shape[1]):
                yield (i, j), self.__dataframe.iloc[i, j]

    def dimensions(self) -> tuple[int, int]:
        """Matrix dimensions.

        Returns
        -------
        tuple of int
            Matrix dimensions

        """
        return (
            int(self.__dataframe.shape[0]),
            int(self.__dataframe.shape[1]),
        )

    def number_of_rows(self) -> int:
        """Give the number of rows.

        Returns
        -------
        int
            Number of rows

        """
        return int(self.__dataframe.shape[0])

    def number_of_columns(self) -> int:
        """Give the number of columns.

        Returns
        -------
        int
            Number of columns

        """
        return int(self.__dataframe.shape[1])

    def number_of_cells(self) -> int:
        """Give the number of cells.

        Returns
        -------
        int
            Number of cells

        """
        return int(self.__dataframe.size)

    def row(self, row_id: np.object_) -> pd.Series:
        """Get row.

        Parameters
        ----------
        row_id : np.object_
            Row id

        Returns
        -------
        pd.Series
            A row

        """
        return self.__dataframe.loc[row_id]

    def column(self, column_id: np.object_) -> pd.Series:
        """Get column.

        Parameters
        ----------
        column_id : np.object_
            Column id

        Returns
        -------
        pd.Series
            A column

        """
        return self.__dataframe[column_id]

    def row_degrees(self) -> tuple[int, ...]:
        """Row degrees.

        Returns
        -------
        tuple of int
            Row degrees

        """
        return tuple(self.__dataframe.sum(axis=1))

    def column_degrees(self) -> tuple[int, ...]:
        """Column degrees.

        Returns
        -------
        tuple of int
            Column degrees

        """
        return tuple(self.__dataframe.sum(axis=0))

    def cells_of_interest(
        self,
        value_of_interest: Literal[0, 1],
    ) -> Iterator[tuple[int, int]]:
        """Cell of interest.

        Parameters
        ----------
        value_of_interest : Literal[0, 1]
            Value of interest

        Yields
        ------
        couple of int
            Cell coordinates

        """
        yield from zip(
            *np.nonzero(
                self.__dataframe == value_of_interest,
            ),
        )

    def number_of_zeros(self) -> int:
        """Give the number of zeros.

        Returns
        -------
        int
            Number of zeros

        """
        return self.number_of_cells() - self.__number_of_ones

    def number_of_ones(self) -> int:
        """Give the number of ones.

        Returns
        -------
        int
            Number of ones

        """
        return self.__number_of_ones

    def density(self) -> float:
        """Density.

        Returns
        -------
        float
            Density

        """
        return self.__number_of_ones / self.number_of_cells()

    def sparsity(self) -> float:
        """Sparsity.

        Returns
        -------
        float
            Sparsity

        """
        return 1 - self.density()

    def row_header(self) -> pd.Index:
        """Row header.

        Returns
        -------
        pd.Index
            Row header

        """
        return self.__dataframe.index

    def column_header(self) -> pd.Index:
        """Column header.

        Returns
        -------
        pd.Index
            Column header

        """
        return self.__dataframe.columns

    def iter_rows(self) -> Iterable[tuple[Hashable, pd.Series]]:
        """Iterate over rows.

        Returns
        -------
        Iterable of tuple(hashable, pd.Series)
            A row

        """
        return self.__dataframe.iterrows()

    def iter_columns(self) -> Iterable[tuple[Hashable, pd.Series]]:
        """Iterate over columns.

        Returns
        -------
        Iterable of tuple(hashable, pd.Series)
            A column

        """
        return self.__dataframe.iteritems()

    def __getitem__(self, coordinate: tuple[int, int]) -> Literal[0, 1]:
        """Get cell value.

        Parameters
        ----------
        coordinate : tuple of int
            Cell coordinates

        Returns
        -------
        Literal[0, 1]
            Cell value

        """
        return self.__dataframe.iloc[coordinate[0], coordinate[1]]

    def to_sub_matrix(
        self,
        row_mask: Iterable[bool],
        column_mask: Iterable[bool],
    ) -> BinMatrix:
        """Instantiate a binary matrix from mask.

        Parameters
        ----------
        row_mask : Iterable of bool
            Row mask
        column_mask : Iterable of bool
            Column mask

        Returns
        -------
        BinMatrix
            A binary matrix

        Raises
        ------
        DegeneratedMatrixError
            If the row or the column mask is empty

        """
        row_mask = np.array(row_mask)
        column_mask = np.array(column_mask)
        # pylint: disable=singleton-comparison
        if (row_mask == False).all() or (column_mask == False).all():  # noqa: E712
            raise DegeneratedMatrixError(
                int(sum(row_mask)),
                int(sum(column_mask)),
            )
        return BinMatrix.new_unsafe(self.__dataframe.iloc[row_mask, column_mask])

    def reverse_zeros_and_ones(self) -> BinMatrix:
        """Reverse zeros and ones.

        Returns
        -------
        BinMatrix
            A binary matrix

        """
        return BinMatrix.new_unsafe(
            deepcopy(self.__dataframe).map(lambda x: 1 - x),
        )

    def to_csv(self, csv_path: Path) -> None:
        """Write the binary matrix to a csv file.

        Parameters
        ----------
        csv_path : Path
            Path to the csv file

        Warnings
        --------
        The csv file will be overwritten if it already exists

        """
        self.__dataframe.to_csv(csv_path)


# ============================================================================ #
#                                  EXCEPTIONS                                  #
# ============================================================================ #
class NotABinaryMatrixError(Exception):
    """Not a binary matrix exception."""

    def __init__(self, unexpected_value: Any) -> None:  # noqa: ANN401
        """Initialize the exception."""
        self.__unexpected_value: Any = unexpected_value

    def unexpected_value(self) -> Any:  # noqa: ANN401
        """Unexpected value.

        Returns
        -------
        Any
            Unexpected value

        """
        return self.__unexpected_value

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message

        """
        return (
            f"Unexpected value: {self.__unexpected_value}\n"
            "The given CSV file or dataframe must contain"
            " only 0 and 1 values.\n"
            "\tHELP: use the `replace_map_value` argument in the"
            " `BinMatrix.from_csv` class method or in `BinMatrix` constructor."
        )


class DegeneratedMatrixError(Exception):
    """Degenerated matrix exception."""

    def __init__(self, number_of_rows: int, number_of_columns: int) -> None:
        """Initialize the exception."""
        self.__nrow: int = number_of_rows
        self.__ncol: int = number_of_columns

    def number_of_rows(self) -> int:
        """Give the number of rows.

        Returns
        -------
        int
            Number of rows

        """
        return self.__nrow

    def number_of_columns(self) -> int:
        """Give the number of columns.

        Returns
        -------
        int
            Number of columns

        """
        return self.__ncol

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message

        """
        return f"The matrix is degenerated ({self.__nrow}x{self.__ncol})."
