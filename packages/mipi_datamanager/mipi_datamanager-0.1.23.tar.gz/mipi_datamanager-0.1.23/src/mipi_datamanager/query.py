from mipi_datamanager import connection
from mipi_datamanager.errors import FormatParameterError
import pandas as pd


def execute_sql_file(file: str, connection: connection.Odbc, format_parameters_list: list = None) -> pd.DataFrame:
    """

    Executes a sql query from a sql file. Optionally renders string formatting into '{}' brackets.

    Args:
        file: file path to the sql
        connection: MiPi connection object
        format_parameters_list: arguments to be passed into sql placeholders

    Returns: dataframe

    """

    sql = read_sql(file, format_parameters_list)
    df = execute_sql(sql, connection)
    print(f"Successfully Read:      File: {file}")

    return df


def execute_sql(sql: str, connection: connection.Odbc, format_parameters_list: list = None) -> pd.DataFrame:
    """
    Executes a sql query from a sql string. Optionally renders string formatting into '{}' brackets.

    Args:
        sql: SQL text string
        connection: MiPi connection object
        format_parameters_list: arguments to be passed into sql placeholders

    Returns:

    """
    if format_parameters_list:
        param_count = sql.count("{}")

        if param_count != len(format_parameters_list):
            raise FormatParameterError(
                f"Number of arguments: {len(format_parameters_list)} does not match the number of place holders")

        _sql = sql.format(*format_parameters_list)

    else:
        _sql = sql

    with connection as con:
        df = pd.read_sql(_sql, con)
    return df


def read_sql(file: str, format_parameters_list: list = None) -> str:
    """

    Reads a SQL file and optionally renders string formatting into '{}' brackets

    Args:
        file: filepath to the sql
        format_parameters_list: arguments to be passed into sql placeholders

    Returns: resolved sql string

    """

    assert isinstance(format_parameters_list,
                      list) or format_parameters_list is None, "Format Parameters list must be type list"

    if not format_parameters_list:
        format_parameters_list = []

    with open(file, 'r') as f:
        sql = f.read()
        param_count = sql.count("{}")
        if param_count != len(format_parameters_list):
            raise FormatParameterError(
                f"Number of arguments: {len(format_parameters_list)} does not match the number of place holders")
        _sql = sql.format(*format_parameters_list)

    return _sql
