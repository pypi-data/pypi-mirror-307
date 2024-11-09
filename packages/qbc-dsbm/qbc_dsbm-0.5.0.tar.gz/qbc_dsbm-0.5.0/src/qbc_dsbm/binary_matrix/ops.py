"""Binary matrix operations."""

from qbc_dsbm.binary_matrix import BinMatrix


# ---------------------------------------------------------------------------- #
#                                Row Operations                                #
# ---------------------------------------------------------------------------- #
def a_minus_b_rows(a: BinMatrix, b: BinMatrix) -> BinMatrix:
    """Subtract two binary matrices on the rows.

    Parameters
    ----------
    a : BinMatrix
        A binary matrix
    b : BinMatrix
        A binary matrix

    Returns
    -------
    BinMatrix
        A binary matrix c with the rows of a without the rows of b

    Raises
    ------
    DegeneratedMatrixError
        Degenerated matrix error

    """
    row_mask = [True for _ in range(a.number_of_rows())]
    column_mask = [True for _ in range(a.number_of_columns())]

    a_row_header = a.row_header()
    b_row_header_set = set(b.row_header())

    for k, col_id in enumerate(a_row_header):
        if col_id in b_row_header_set:
            row_mask[k] = False

    return a.to_sub_matrix(row_mask, column_mask)


def a_inter_b_rows(a: BinMatrix, b: BinMatrix) -> BinMatrix:
    """Intersect two binary matrices on the rows.

    Parameters
    ----------
    a : BinMatrix
        A binary matrix
    b : BinMatrix
        A binary matrix

    Returns
    -------
    BinMatrix
        A binary matrix c with the rows in common in a and b

    Raises
    ------
    DegeneratedMatrixError
        Degenerated matrix error

    """
    row_mask = [False for _ in range(a.number_of_rows())]
    column_mask = [True for _ in range(a.number_of_columns())]

    a_row_header = a.row_header()
    b_row_header_set = set(b.row_header())

    for k, row_id in enumerate(a_row_header):
        if row_id in b_row_header_set:
            row_mask[k] = True

    return a.to_sub_matrix(row_mask, column_mask)


# ---------------------------------------------------------------------------- #
#                               Column Operations                              #
# ---------------------------------------------------------------------------- #
def a_minus_b_columns(a: BinMatrix, b: BinMatrix) -> BinMatrix:
    """Subtract two binary matrices on the columns.

    Parameters
    ----------
    a : BinMatrix
        A binary matrix
    b : BinMatrix
        A binary matrix

    Returns
    -------
    BinMatrix
        A binary matrix c with the columns of a without the columns of b

    Raises
    ------
    DegeneratedMatrixError
        Degenerated matrix error

    """
    row_mask = [True for _ in range(a.number_of_rows())]
    column_mask = [True for _ in range(a.number_of_columns())]

    a_col_header = a.column_header()
    b_col_header_set = set(b.column_header())

    for k, col_id in enumerate(a_col_header):
        if col_id in b_col_header_set:
            column_mask[k] = False

    return a.to_sub_matrix(row_mask, column_mask)


def a_inter_b_columns(a: BinMatrix, b: BinMatrix) -> BinMatrix:
    """Intersect two binary matrices on the columns.

    Parameters
    ----------
    a : BinMatrix
        A binary matrix
    b : BinMatrix
        A binary matrix

    Returns
    -------
    BinMatrix
        A binary matrix c with the columns in common in a and b

    Raises
    ------
    DegeneratedMatrixError
        Degenerated matrix error

    """
    row_mask = [True for _ in range(a.number_of_rows())]
    column_mask = [False for _ in range(a.number_of_columns())]

    a_col_header = a.column_header()
    b_col_header_set = set(b.column_header())

    for k, col_id in enumerate(a_col_header):
        if col_id in b_col_header_set:
            column_mask[k] = True

    return a.to_sub_matrix(row_mask, column_mask)
