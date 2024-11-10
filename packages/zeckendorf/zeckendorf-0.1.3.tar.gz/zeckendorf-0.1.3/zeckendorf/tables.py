from typing import List


def create_matrix_table(column_label: str, row_label: str, data: List[List], dynamic: bool = False, padding: int = 0, zero_in_N: bool = False, transpose: bool = False) -> str:
    """
    Create a matrix table with row and column labels.

    :param column_label: Label for the columns.
    :param row_label: Label for the rows.
    :param data: 2D list containing the table data. Must not be empty.
    :param dynamic: If True, adjusts the column width based on content. If False, uses the maximum column width.
    :param padding: Additional padding for each cell. Must be non-negative.
    :param zero_in_N: If True, starts the labeling with 0. If False, starts the labeling with 1.
    :paran transpose: If True, the data is transposed. If False, it is not.
    :return: A formatted matrix table as a string.
    """

    if padding < 0:
        raise ValueError('Invalid padding.')
    if len(data) == 0:
        raise ValueError('Empty data.')
    if len(set(len(row) for row in data)) != 1:
        raise ValueError('Inconsistent data.')
    if len(data[0]) == 0:
        raise ValueError('Empty data.')
    
    d = 0 if zero_in_N else 1

    if transpose:
        data = [list(row) for row in zip(*data)]
    
    info_row = [str(i + d) for i in range(len(data[0]))]
    info_column = [str(i + d) for i in range(len(data))]

    column_widths = [max(len(str(elem)) + padding for elem in col) for col in zip(*([info_row] + data))]
    if not dynamic:
        max_width = max(column_widths)
        column_widths = len(info_row) * [max_width]

    first_column_width = max(len(column_label), len(row_label), len(str(len(data))))

    header = column_label.rjust(first_column_width) + '  ' + " ".join(
        str(cell).ljust(column_widths[i]) for i, cell in enumerate(info_row))

    data_rows = "\n".join(
        info_column[i].rjust(first_column_width) + '  ' + " ".join(
            str(cell).ljust(column_widths[j]) for j, cell in enumerate(row))
        for i, row in enumerate(data))

    return f"{header}\n{row_label.rjust(first_column_width)}\n{data_rows}"


def create_table(column_labels: List[str], data: List[List], dynamic: bool = False, padding: int = 0) -> str:
    """
    Create a table with given column labels.

    :param column_labels: List of labels for the columns.
    :param data: 2D list containing the table data.
    :param dynamic: If True, adjusts the column width based on content. If False, uses the maximum column width.
    :param padding: Additional padding for each cell. Must be non-negative.
    :return: A formatted table as a string.
    """
    if padding < 0:
        raise ValueError('Invalid padding.')

    column_widths = [max(len(str(elem)) + padding for elem in col) for col in zip(*([column_labels] + data))]
    if not dynamic:
        max_width = max(column_widths)
        column_widths = len(column_labels) * [max_width]

    header = " ".join(
        column_labels[i].ljust(column_widths[i]) for i, cell in enumerate(column_labels))

    data_rows = "\n".join(" ".join(
        str(cell).ljust(column_widths[j]) for j, cell in enumerate(row))
                          for i, row in enumerate(data))

    return f"{header}\n{data_rows}"
