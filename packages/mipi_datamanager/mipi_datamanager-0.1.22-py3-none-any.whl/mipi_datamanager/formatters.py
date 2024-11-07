import warnings
from typing import Callable
import pandas as pd

class FormatDict(dict):
    """
    This class is designed to store format functions within the [DataManager][mipi_datamanager.DataManager].
    It is a child of dictionary and contains an additional method to assign many keys to the same value.

    TODO show adding one of my callables


    Examples:
        >>> from mipi_datamanager import DataManager
        >>> from mipi_datamanager.formatters import FormatDict
        >>> import pandas as pd
        >>> format_dict = FormatDict({"a":lambda x: 2*x})
        >>> format_dict.update({["b","c"]:lambda x: 10*x})
        >>> df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6],'c':[7,8,9],'d':[10,11,12]})
        >>> mipi = DataManager.from_dataframe(df,default_format_func_dict=format_dict)
        >>> mipi.trgt
        pd.DataFrame({'a':[2,4,6], 'b':[40,50,60],'c':[70,80,90],'d':[10,11,12]})

    """
    def update_group(self,columns:list, func:Callable) -> None:

        """
        Updates a group of keys to be assigned to the same value. This is useful when many columns need to use the
        same format function

        Args:
            columns: Columns to assign to the specified function
            func: Function to assign to the specified keys

        Examples:
            >>> my_format_dict = FormatDict({'a':lambda x: x, 'b':lambda x: 2*x})
            >>> my_format_dict.update_group(['c','d'], lambda x: x*x)
            >>> my_format_dict
            {'a':lambda x: x, 'b':lambda x: 2*x,'c':lambda x: x*x, 'd':lambda x: x*x}
        """

        for c in columns:
            self[c] = func


def _drop_na(series):
    if series.isna().any():
        series = series.dropna()
        warnings.warn("Na values were dropped during formatting.")
    return series


def cast(data_type) -> Callable:
    """
    Cast a series as a specific data type, equivelent to pd.Series.astype()
    Args:
        data_type: builtin formatter to apply to the series

    Examples:
        >>>my_series = pd.Series([1.0,"2",3],name="my_ints")
        >>>formatter = cast(int)
        >>>formatter(my_series)
        pd.Series([1,2,3],name="my_ints")


    Returns:

    """
    def cast_func(series):
        series = _drop_na(series)
        return series.astype(data_type)

    return cast_func


def cast_int_str() -> Callable:
    """
    Casts a series as an interger value represented as a string.

    Returns:

    Examples:
        >>>my_series = pd.Series([1.0,"2",3],name="my_ints")
        >>>formatter = cast_int_str()
        >>>formatter(my_series)
        pd.Series(['1','2','3'],name="my_ints")

    """
    def cast_func(series):
        series = _drop_na(series)
        return series.astype("int64", errors="ignore").astype(str, errors="ignore")

    return cast_func


def cast_padded_int_str(value_length):
    """
    Casts a series as an interger value represented as a string. Values are padded on to the left with zeros.

    Returns:

    Examples:
        >>>my_series = pd.Series([1.0,"2",3],name="my_ints")
        >>>formatter = cast(3)
        >>>formatter(my_series)
        pd.Series(['001','002','003'],name="my_ints")

    """


    def cast_func(series) -> pd.Series:
        series = _drop_na(series)
        cast_int_str_func = cast_int_str()
        series = cast_int_str_func(series)

        return series.where(~series.str.startswith('-'),
                            '-' + series.str[1:].str.rjust(value_length, "0")).str.rjust(value_length, "0")

    return cast_func


def cast_as_datetime():
    def cast_func(series: pd.Series) -> pd.Series:
        _series = _drop_na(series)
        _series = pd.to_datetime(_series)
        return series

    return cast_func


def cast_as_datetime_string(format_code):
    def cast_func(series: pd.Series):
        _series = _drop_na(series)
        _series = pd.to_datetime(_series)
        _series = _series.dt.strftime(format_code)
        return _series

    return cast_func


def cast_as_iso_date_string(date_delim="-", time_delim=":"):
    def cast_func(series: pd.Series):
        _series = _drop_na(series)
        format_string = f"%Y{date_delim}%m{date_delim}%d"
        if time_delim:
            format_string += f" %H{time_delim}%M{time_delim}%S"
        format_func = cast_as_datetime_string(format_string)
        return format_func(series)

    return cast_func


def cast_as_american_date_string(date_delim="/", time_delim=":"):
    def cast_func(series: pd.Series) -> pd.Series:
        _series = _drop_na(series)
        format_string = f"%m{date_delim}%d{date_delim}%Y"
        if time_delim:
            format_string += f" %H{time_delim}%M{time_delim}%S"
        format_func = cast_as_datetime_string(format_string)
        return format_func(series)

    return cast_func
