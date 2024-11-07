import pandas as pd

def rename_select_columns(df: pd.DataFrame, column_rename_dict: dict) -> pd.DataFrame:
    """
    changes the name of dataframe columns and filters to columns in the dictionary.
    assigning new value to None includes the column but does not rename it

    Args:
        df: dataframe to modify
        column_rename_dict: dictionary of column values {old_name:new_name}

    Returns: dataframe only containing specified columns

    See Also: [print_columns_dict][mipi_datamanager.DataManager.print_target_column_dict]

    """

    column_rename_dict = {k: (v if v is not None else k) for (k, v) in column_rename_dict.items()}

    df1 = df.copy()
    target_columns = list(column_rename_dict.keys())

    invalid_cols = [col for col in target_columns if col not in df1.columns]
    if invalid_cols:
        raise KeyError(f"Columns: ({invalid_cols}) not found in dataframe.")
    df1 = df1[target_columns]
    df1 = df1.rename(columns=column_rename_dict)

    return df1

def coalesce(df: pd.DataFrame, columns: list) -> pd.Series:
    """
    Coalesces columns from a dataframe into a single series. This function is the same as SQL's coalesce() function.
    Column values are given priority in the order that they are passed in.

    Args:
        df: dataframe to coalesce
        columns: list of columns to coalesce

    Returns: coalesced series

    """

    if len(columns) < 2:
        raise KeyError("Must enter at least 2 *column arguments")

    series = df[columns[0]].copy()

    for col in columns[1:]:

        if col not in df.columns:
            raise KeyError("One or more *columns does not exist in the dataframe")

        series = series.combine_first(df[col])
        series.name = None

    return series
