"""Bigraph module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, cast

import numpy as np
import numpy.typing as nptyping

if TYPE_CHECKING:
    from qbc_dsbm.binary_matrix import BinMatrix


# ============================================================================ #
#                                    CLASSES                                   #
# ============================================================================ #
class ZerosBiGraph:
    """Bigraph class.

    The edges represent zeros in the binary matrix.
    """

    def __init__(
        self,
        edges: Iterable[tuple[int, int]],
        u_bipart_size: int,
        v_bipart_size: int,
    ) -> None:
        """Initialize the bigraph."""
        self.__edges: tuple[tuple[int, int], ...] = tuple(edges)

        self.__u_bipart_degrees = np.zeros((u_bipart_size,), dtype=np.uintp)
        self.__v_bipart_degrees = np.zeros((v_bipart_size,), dtype=np.uintp)

        for u, v in self.__edges:
            self.__u_bipart_degrees[u] += 1
            self.__v_bipart_degrees[v] += 1

    @classmethod
    def from_bin_matrix(cls, bin_matrix: BinMatrix) -> ZerosBiGraph:
        """Instantiate a bigraph from a binary matrix.

        Parameters
        ----------
        bin_matrix : BinMatrix
            Binary matrix

        Returns
        -------
        BiGraph
            A bigraph

        """
        return cls(
            bin_matrix.cells_of_interest(0),
            bin_matrix.number_of_rows(),
            bin_matrix.number_of_columns(),
        )

    def card_u_bipart(self) -> int:
        """Cardinality of the first bipartite.

        Returns
        -------
        int
            Cardinality of bipart U

        """
        return len(self.__u_bipart_degrees)

    def card_v_bipart(self) -> int:
        """Cardinality of the second bipartite.

        Returns
        -------
        int
            Cardinality of bipart V

        """
        return len(self.__v_bipart_degrees)

    def u_bipart_degrees(self) -> nptyping.NDArray[np.uintp]:
        """First bipartite degrees.

        Returns
        -------
        vector of int
            First bipartite degrees

        """
        return self.__u_bipart_degrees

    def v_bipart_degrees(self) -> nptyping.NDArray[np.uintp]:
        """Second bipartite degrees.

        Returns
        -------
        vector of int
            Second bipartite degrees

        """
        return self.__v_bipart_degrees

    def u_bipart_anti_degrees(self) -> nptyping.NDArray[np.uintp]:
        """First bipartite anti-degrees.

        Anti-degrees are the number of missing edges on the bipartite
        to make the bigraph complete.

        Returns
        -------
        vector of int
            First bipartite anti-degrees

        """
        return cast(
            nptyping.NDArray[np.uintp],
            len(self.__v_bipart_degrees) - self.__u_bipart_degrees,
        )

    def v_bipart_anti_degrees(self) -> nptyping.NDArray[np.uintp]:
        """Second bipartite anti-degrees.

        Anti-degrees are the number of missing edges on the bipartite
        to make the bigraph complete.

        Returns
        -------
        vector of int
            Second bipartite anti-degrees

        """
        return cast(
            nptyping.NDArray[np.uintp],
            len(self.__u_bipart_degrees) - self.__v_bipart_degrees,
        )

    def edges(self) -> tuple[tuple[int, int], ...]:
        """Edges.

        Returns
        -------
        tuple of tuple of int
            Edges

        """
        return self.__edges
