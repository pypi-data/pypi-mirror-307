import importlib.util
import sys
import warnings, os, json
from collections import ChainMap
from typing import Callable, overload, final, Self
from pathlib import Path
from pandas.errors import MergeError
import pandas as pd
from jinja2 import Template

from mipi_datamanager.formatters import FormatDict
from mipi_datamanager import query,connection, generate_inserts
from mipi_datamanager.core import common as com
from mipi_datamanager.core import meta
from mipi_datamanager.types import JoinLiterals, Mask
from mipi_datamanager.errors import ConfigError
from mipi_datamanager.core.jinja import JinjaLibrary, JinjaRepo


def _get_df_and_sql_from_jinja_template(jenv, script_path, connection,
                                        jinja_parameters_dict):  # TODO these are redundant
    df = jenv.execute_file(script_path, connection, jinja_parameters_dict)
    sql = jenv.resolve_file(script_path, jinja_parameters_dict)
    del jenv
    return df, sql


def _get_df_and_sql_from_jinja_repo(jinja_repo_source, inner_path, connection, jinja_parameters_dict):
    jenv = JinjaRepo(jinja_repo_source.root_dir)
    return _get_df_and_sql_from_jinja_template(jenv, inner_path, connection, jinja_parameters_dict)


def _get_df_and_sql_from_jinja(script_path, connection, jinja_parameters_dict):
    path = Path(script_path)
    jenv = JinjaLibrary(path.parent)
    return _get_df_and_sql_from_jinja_template(jenv, path.name, connection, jinja_parameters_dict)


def _get_df_and_sql_from_sql(script_path, format_parameters_list, connection):
    df = query.execute_sql_file(script_path, connection, format_parameters_list)
    sql = query.read_sql(script_path, format_parameters_list)
    return df, sql


def _maybe_get_frame_name(frame_name, script_path):
    return frame_name or Path(script_path).stem


def _get_config_from_master(inner_path, jinja_repo_source):
    _inner_path = Path(inner_path)
    with open(os.path.join(jinja_repo_source.root_dir, "master_config.json"), 'r') as f:
        master_config = json.load(f)
    return master_config[str(_inner_path.parent).replace("\\", "/")][str(_inner_path.name)]

def _load_user_setup():
    # List of possible directories where mipi_setup.py might be located
    possible_paths = []

    # 1. Path specified by an environment variable
    env_path = os.environ.get('MIPI_PATH')
    if env_path:
        possible_paths.append(env_path)

    # 2. Current working directory
    possible_paths.append(os.getcwd())

    # 3. User's home directory
    home_dir = os.path.expanduser("~")
    possible_paths.append(home_dir)

    # 4. Virtual environment directory (where the package is installed)
    if hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix:
        # In a virtual environment
        venv_site_packages = Path(sys.prefix) / 'Lib' / 'site-packages'
        possible_paths.append(str(venv_site_packages))
    else:
        # Not in a virtual environment
        site_packages = Path(sys.prefix) / 'Lib' / 'site-packages'
        possible_paths.append(str(site_packages))

    # 5. Directory of this file (where the package module is located)
    package_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths.append(package_dir)

    # 6. Standard configuration directories
    # For Windows
    appdata_dir = os.environ.get('APPDATA')  # Typically C:\Users\Username\AppData\Roaming
    if appdata_dir:
        possible_paths.append(appdata_dir)

    local_appdata_dir = os.environ.get('LOCALAPPDATA')  # Typically C:\Users\Username\AppData\Local
    if local_appdata_dir:
        possible_paths.append(local_appdata_dir)

    # For cross-platform compatibility, include ~/.config
    config_dir = os.path.join(home_dir, ".config")
    possible_paths.append(config_dir)

    # Search for mipi_setup.py in the possible paths
    for path in possible_paths:
        setup_path = os.path.join(path, "mipi_setup.py")
        if os.path.isfile(setup_path):
            # Dynamically import the setup file
            spec = importlib.util.spec_from_file_location("mipi_setup", setup_path)
            user_setup = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_setup)
            return user_setup

    # If mipi_setup.py is not found in any of the paths
    return None

def _get_jungle_and_format(jinja_repo_source_input,format_dict_input):
    _user_setup = _load_user_setup()
    jinja_repo_source = jinja_repo_source_input or (_user_setup.mipi_repo if _user_setup else None)
    format_dict = format_dict_input or (_user_setup.mipi_format_dict if _user_setup else None)

    if format_dict is None:
       format_dict = dict()

    return jinja_repo_source, format_dict

class _FormattedFunctions:
    def __init__(self, format_func_dict: dict | ChainMap = None):

        self._validate(format_func_dict)
        _format_func_dict = format_func_dict or dict()
        self.format_func_dict = _format_func_dict

    def _validate(self, format_func_dict):
        '''assert that the single func is callable and the dict is a dict of callables'''

        if format_func_dict:
            for k, v in format_func_dict.items():
                if not callable(v):
                    raise ValueError(f"Function {k} must be callable")

    @final
    def format_series(self, series):

        if not isinstance(series, pd.Series):
            raise ValueError(f"series must be pd.Series, got {type(series)}")

        key = series.name
        if key in self.format_func_dict:
            format_func = self.format_func_dict[key]
            return format_func(series)
        else:
            return series


class _FormattedJoinOperation:
    def __init__(self, format_funcs: list[_FormattedFunctions]):
        self._validate(format_funcs)
        format_dicts = [i.format_func_dict for i in format_funcs]
        self._final_dict = ChainMap(*format_dicts)
        self.final_formatter = _FormattedFunctions(self._final_dict)

    def _validate(self, format_funcs):
        if not isinstance(format_funcs, list):
            raise ValueError(f"format_funcs must be a list, got {type(format_funcs)}")
        else:
            for f in format_funcs:
                if not isinstance(f, _FormattedFunctions):
                    raise ValueError(f"formatter must be type of _FormattedFunctions, got {type(f)}")

    @overload
    def _format_df_slice(self, slice: pd.DataFrame) -> pd.DataFrame:
        ...

    @overload
    def _format_df_slice(self, slice: pd.Series) -> pd.Series:
        ...

    def _format_df_slice(self, df):
        if isinstance(df, pd.DataFrame):
            for c in df.columns:
                df[c] = self.final_formatter.format_series(df[c])
        elif isinstance(df, pd.Series):
            df = self.final_formatter.format_series(df)

        return df

    def _format_slice_by_key(self, df, key):
        key = com._maybe_convert_tuple_to_list(key)
        df[key] = self._format_df_slice(df[key])
        return df

    def _format_pair_by_keys(self, df, key, use_index):
        if not use_index:
            _df = self._format_slice_by_key(df, key)
        else:
            _df = df
        return _df

    # def _format_index(self,df): # TODO
    #     df.index = #self.final_formatter.format_series()

    @final
    def format_incoming_df(self, df):  # , on=None, side_on=None, use_index=False):
        for c in df.columns:
            if c in self._final_dict:
                df[c] = self.final_formatter.format_series(df[c])
        return df

    def validate_join(self):
        pass


class DataManager:
    """
    Queries, stores, and combines data from a library of SQL scripts and other data sources. This class serves as a
    workspace to additively build a data set. Data primarily added from modular SQL templates. This class can build
    subsequent queries from those templates. This class also tracks useful information about the data and its sources.

    An object of this class is always build from a a "Base Population" using a constructor prefixed with `from_`.
    Additional data can be added to the "Target Population" using join methods, which are all prefixed with `join_from_`.
    Additional data will always be added to the working "Target Population".
    Data joined from SQL will match the granularity of the current Target Population.

    TODO:
        Clarify interactions between on, left_on, and right_on, especially in cases where they are None.
        Add further details on how format_func_dict modifies the columns during joins.
        For SQL-related joins, explain how format_parameters_list interacts with SQL placeholders in more detail.

        mipi_setup.py
    """

    def __init__(self, frame: meta.Frame,
                 jinja_repo_source: JinjaRepo = None,  # TODO maybe change name to jinja_repo
                 store_deep_frames: bool = False,
                 store_deep_base: bool = False,
                 default_format_func_dict: FormatDict | dict = None,
                 dialect: str = "mssql"):

        self.dialect = dialect
        self.default_formatter = _FormattedFunctions(default_format_func_dict)

        self.jinja_repo_source,self.default_format_func_dict =_get_jungle_and_format(jinja_repo_source,default_format_func_dict)

        self._user_added_func_dict = default_format_func_dict.copy() if default_format_func_dict is not None else {}

        assert isinstance(frame, meta.Frame)
        self._frames = com.IndexedDict()

        self.store_deep_frames = store_deep_frames
        self.store_deep_base = store_deep_base

        # copy to target population, mutable, formatting done in meta.frame
        self._target_population = frame.df_query.copy()
        self.default_formatter_chain = _FormattedJoinOperation([self.default_formatter])
        self._target_population = self.default_formatter_chain.format_incoming_df(self._target_population)
        frame._set_target(self._target_population)

        self._column_sources = dict()  # stores frame_index of columns. used to add frame number as join suffix for duped cols
        self._set_column_source_from_frame(frame, 0)

        if self.store_deep_base is False and self.store_deep_frames is False:
            del frame.df_query
            del frame.df_target
        self._store_frame(frame, 0)

    @classmethod
    def from_jinja_repo(cls, inner_path: str,
                        jinja_repo_source: JinjaRepo = None,
                        jinja_parameters_dict: dict = None,
                        store_deep_base: bool = False,
                        store_deep_frames: bool = False,
                        default_format_func_dict: FormatDict | dict = None,
                        dialect: str = "mssql") -> Self:

        """
        Creates a MiPi DataManager from a Jinja script stored in a MiPi Repository.
        This is the most concise way to create a DataManager from frequently used scripts.
        All scripts in the repo are tied to the appropriate connection, frame name, and documentation.

        !!! info
            Please see the [JinjaRepo documentation][mipi_datamanager.core.jinja.JinjaRepo] for example usage and setup.

        Args:
            inner_path: Path from the root of the JinjaRepo to the jinja sql script.
            jinja_repo_source: Object that defines a repo. Points the repo directory and contains the Repo's connections.
            jinja_parameters_dict: Keyword parameters to pass into jinja tags.
            store_deep_frames: If `True`, each `DM.Frame` stores a full DataFrame for both the `df_query` and `df_target`.
                This is useful for troubleshooting as it provides detailed snapshots of each frame during creation,
                but this can be memory-intensive. Supersedes store_deep_base.
            store_deep_base: If `True`, the base frame only `DM.Frame[0]` stores a full DataFrame for both the `df_query` and `df_target`.
            default_format_func_dict: A dictionary where the keys are column names and the values are callable. Each
                Callable must take a series input and return the formatted series. The formatting is applied every time
                the respective column enters the DM see [Format Tools](/auto/data_manager/#format-tools) for more information.
            dialect: SQL dialect being used in the database, this determines the temp table syntax.
                Currently only 'mysql' is available but more to come

        Returns
            DataManager: A datamanager object

        """
        jinja_repo_source, _ = _get_jungle_and_format(jinja_repo_source,default_format_func_dict)
        config = _get_config_from_master(inner_path, jinja_repo_source)

        if not config["meta"]["population"]:
            raise ConfigError(f'expected population status is True script got: {config["meta"]['population']}')

        con = jinja_repo_source.conn_list[config['meta']['connection']]
        df, sql = _get_df_and_sql_from_jinja_repo(jinja_repo_source, inner_path, con, jinja_parameters_dict)
        frame = meta.Frame(config["meta"]["name"], "JinjaRepo", df, sql=sql)

        return cls(frame,
                   jinja_repo_source=jinja_repo_source,
                   store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict,
                   dialect=dialect)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, frame_name: str = None,
                       jinja_repo_source: JinjaRepo = None,
                       store_deep_frames: bool = False, store_deep_base: bool = False,
                       default_format_func_dict: FormatDict | dict = None,
                       dialect: str = "mssql"
                       ) -> Self:
        """
        Creates a MiPi DataManager(DM) from a pandas dataframe.

        Args:
            df: Pandas dataframe to set as the base population
            frame_name: Name of the frame that is stored in the DM. If None, defaults to `unnamed-dataframe`
            jinja_repo_source: Object that defines a repo. Points the repo directory and contains the Repo's connections.
            store_deep_frames: If `True`, each `DM.Frame` stores a full DataFrame for both the `df_query` and `df_target`.
                This is useful for troubleshooting as it provides detailed snapshots of each frame during creation,
                but this can be memory-intensive. Supersedes store_deep_base.
            store_deep_base: If `True`, the base frame only `DM.Frame[0]` stores a full DataFrame for both the `df_query` and `df_target`.
            default_format_func_dict: A dictionary where the keys are column names and the values are callable. Each
                Callable must take a series input and return the formatted series. The formatting is applied every time
                the respective column enters the DM see [Format Tools](/auto/data_manager/#format-tools) for more information.
            dialect: SQL dialect being used in the database, this determines the temp table syntax.
                Currently only 'mysql' is available but more to come

        Returns: DataManager: A datamanager object


        !!! example
            ```python
            from mipi_datamanager import DataManager
            import pandas as pd

            data = {
                'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
                'Age': [25, 30, 35, 40, 45],
                'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Boston'],
                'Salary': [80000, 90000, 100000, 110000, 120000]
            }

            # Creating a DataFrame
            df = pd.DataFrame(data)

            mipi = DataManager.from_dataframe(df)
            ```

        """
        _frame_name = frame_name or "unnamed-dataframe"

        frame = meta.Frame(_frame_name, "Data Frame", df, None, None)
        return cls(frame, jinja_repo_source=jinja_repo_source,
                   store_deep_frames=store_deep_frames, store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict,
                   dialect=dialect)

    @classmethod
    def from_sql(cls, script_path: str, connection: connection.Odbc, format_parameters_list: list = None,
                 frame_name: str = None,
                 jinja_repo_source: JinjaRepo = None,
                 store_deep_frames: bool = False, store_deep_base: bool = False,
                 default_format_func_dict: FormatDict | dict = None,
                 dialect: str = "mssql") -> Self:

        """
        Creates a MiPi DataManager(DM) from the results of a SQL script. The SQL script can have '{}' placeholders which
        will be resolved using string formatting. The values of `format_parameters_list` will be passed into the
        placeholders in order.

        !!! info "Script Setup"
            The SQL script uses python string formatting syntax. You can place optional placeholders '{}' in your
            script to accept the parameters of 'format_parameters_list'.

        Args:
            script_path: The absolute or relative path to the SQL script.
            connection: MiPi Connection Object
            format_parameters_list: A list of values to be placed into string format placeholders "{}".
                Values will be entered into placeholders in the order of the list.
                This is equivalent to using python string formatting ie. `"{} {}".format(["hello","world"])`
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to the name of the SQL script file.
            jinja_repo_source: Object that defines a repo. Points the repo directory and contains the Repo's connections.
            store_deep_frames: If `True`, each `DM.Frame` stores a full DataFrame for both the `df_query` and `df_target`.
                This is useful for troubleshooting as it provides detailed snapshots of each frame during creation,
                but this can be memory-intensive. Supersedes store_deep_base.
            store_deep_base: If `True`, the base frame only `DM.Frame[0]` stores a full DataFrame for both the `df_query` and `df_target`.
            default_format_func_dict: A dictionary where the keys are column names and the values are callable. Each
                Callable must take a series input and return the formatted series. The formatting is applied every time
                the respective column enters the DM see [Format Tools](/auto/data_manager/#format-tools) for more information.
            dialect: SQL dialect being used in the database, this determines the temp table syntax.
                Currently only 'mysql' is available but more to come

        !!! example
            Main Python Script
            ```python
            from mipi_datamanager import DataManager
            from mipi_datamanager.odbc import Odbc

            con = Odbc(dsn = "my_dsn")

            mipi = DataManager.from_sql("path/to/sql_script.sql",con,
                                          format_parameters_list = ["2023-01-01","2024-01-01"])
            ```
            <details>
            <summary>Click to expand the accompanying SQL example</summary>
            Script Template
            ```tsql
            SELECT PrimaryKey, Value
            LEFT Table1 tbl
            where tbl.date IS BETWEEN '{}' AND '{}'

            ```
            Resolved Query
            ```tsql
            SELECT PrimaryKey, Value
            LEFT Table1 tbl
            where tbl.date IS BETWEEN '2023-01-01' AND '2024-01-01'
            ```
            </details>

        Returns: DataManager: A datamanager object

        """

        _frame_name = _maybe_get_frame_name(frame_name, script_path)
        df, sql = _get_df_and_sql_from_sql(script_path, format_parameters_list, connection)

        built_from = "Format SQL" if format_parameters_list else "SQL"

        frame = meta.Frame(_frame_name, built_from, df, sql=sql)
        return cls(frame, jinja_repo_source=jinja_repo_source, store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict, dialect=dialect)

    @classmethod
    def from_jinja(cls, script_path: str, connection: connection.Odbc,
                   jinja_parameters_dict: dict = None,
                   frame_name: str = None,
                   jinja_repo_source: JinjaRepo = None,
                   store_deep_frames: bool = False, store_deep_base: bool = False,
                   default_format_func_dict: FormatDict | dict = None,
                   dialect: str = "mssql"):
        """

        Creates a MiPi DataManager(DM) from a Jinja script Script. Jinja Scripts use named keyword tags {{ key }} and
        can include jinja logic. For details on Jinja syntax view the [official documentation](https://jinja.palletsprojects.com/en/3.1.x/).

        !!! info "Script Setup"
            The SQL script uses Jinja syntax, see [Jinja2 official documentation](https://jinja.palletsprojects.com/en/3.1.x/)
            You can place optional jinja tags '{{...}}' to accept the keyword pairs of 'jinja_parameters_dict'.

        Args:
            script_path: The absolute or relative path to the Jinja SQL script.
            connection: MiPi Connection Object
            jinja_parameters_dict: Keyword parameters to pass into jinja tags.
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to the name of the SQL script file.
            jinja_repo_source: Object that defines a repo. The repo stores each script and its meta data.
            store_deep_frames: If `True`, each `DM.Frame` stores a full DataFrame for both the `df_query` and `df_target`.
                This is useful for troubleshooting as it provides detailed snapshots of each frame during creation,
                but this can be memory-intensive. Supersedes store_deep_base.
            store_deep_base: If `True`, the base frame only `DM.Frame[0]` stores a full DataFrame for both the `df_query` and `df_target`.
            default_format_func_dict: A dictionary where the keys are column names and the values are callable. Each
                Callable must take a series input and return the formatted series. The formatting is applied every time
                the respective column enters the DM see [Format Tools](/auto/data_manager/#format-tools) for more information.
            dialect: SQL dialect being used in the database, this determines the temp table syntax.
                Currently only 'mysql' is available but more to come

        !!! example

            Main Python Script:
            ```python
            from mipi_datamanager import DataManager
            from mipi_datamanager.odbc import Odbc

            con = Odbc(dsn = "my_dsn")

            jinja_parameters_dict = {"date_start":"2023-01-01",
                                     "date_end":"2024-01-01"}

            mipi = DataManager.from_jinja("path/to/sql_script.sql",con,
                                          jinja_parameters_dict = jinja_parameters_dict)
            ```

            <details>
            <summary>Click to expand the accompanying SQL example</summary>
            Jinja Script Template:
            ```tsql
            SELECT PrimaryKey, Value
            LEFT Table1 tbl
            where tbl.date IS BETWEEN '{{ date_start }}' AND '{{ date_end }}'

            ```

            Resolves to:
            ```tsql
            SELECT PrimaryKey, Value
            LEFT Table1 tbl
            where tbl.date IS BETWEEN '2023-01-01' AND '2024-01-01'
            ```
            </details>

        Returns: DataManager: A datamanager object

        """

        _frame_name = _maybe_get_frame_name(frame_name, script_path)

        df, sql = _get_df_and_sql_from_jinja(script_path, connection, jinja_parameters_dict)

        frame = meta.Frame(_frame_name, "Jinja", df, sql=sql)

        return cls(frame, jinja_repo_source=jinja_repo_source, store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict, dialect=dialect)

    @classmethod
    def from_excel(cls, excel_path: str, frame_name: str = None,
                   jinja_repo_source: JinjaRepo = None,
                   store_deep_frames: bool = False, store_deep_base: bool = False,
                   default_format_func_dict: FormatDict | dict = None,
                   excel_sheet: str | int | None = None,
                   dialect: str = "mssql") -> Self:
        """

        Creates a MiPi DataManager(DM) from a microsoft Excel file.

        Args:
            excel_path: Absolute or relative path to the Microsoft Excel file.
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to the name of the Excel file.
            jinja_repo_source: Object that defines a repo. Points the repo directory and contains the Repo's connections.
            store_deep_frames: If `True`, each `DM.Frame` stores a full DataFrame for both the `df_query` and `df_target`.
                This is useful for troubleshooting as it provides detailed snapshots of each frame during creation,
                but this can be memory-intensive. Supersedes store_deep_base.
            store_deep_base: If `True`, the base frame only `DM.Frame[0]` stores a full DataFrame for both the `df_query` and `df_target`.
            default_format_func_dict: A dictionary where the keys are column names and the values are callable. Each
                Callable must take a series input and return the formatted series. The formatting is applied every time
                the respective column enters the DM see [Format Tools](/auto/data_manager/#format-tools) for more information.
            excel_sheet: sheet name(str) or sheet index(int)
            dialect: SQL dialect being used in the database, this determines the temp table syntax.
                Currently only 'mysql' is available but more to come
        !!! example
            Main Python Script
            ```python
            from mipi_datamanager import DataManager

            mipi = DataManager.from_excel("path/to/excel_file.xlsx")
            ```

        Returns: DataManager: A datamanager object

        """
        _frame_name = _maybe_get_frame_name(frame_name, excel_path)
        df = pd.read_excel(excel_path, sheet_name=excel_sheet or 0)
        frame = meta.Frame(_frame_name, "Excel", df)
        return cls(frame, jinja_repo_source=jinja_repo_source, store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict,
                   dialect=dialect)

    def _store_frame(self, frame: meta.Frame, idx) -> None:
        """ to store a frame including its index"""
        alias = f"{frame.name}_{idx}"
        self._frames[alias] = frame

    ##############################################################################################
    # Target Data Joins
    ##############################################################################################

    def join_from_jinja_repo(self, inner_path: str, how: JoinLiterals = "left", jinja_parameters_dict: dict = None,
                             format_func_dict: FormatDict | dict = None, left_on: str | tuple = None, left_index: bool = False):

        """
        This function joins the result of a jinja repo script to a DataManager object. Note that the `connection` and
        `right_on` have already been predefined by the repo's config.

        !!! warning
            This function is only available in if you defined a `JinjaRepo` while instantiating the DataManager object.

        !!! info "Script Setup"
            Please see the [JinjaRepo documentation][mipi_datamanager.core.jinja.JinjaRepo] for example usage and setup.


        Args:
            inner_path: Path from the root of the JinjaRepo to the jinja sql script.
            how: {'left', 'right', 'inner', 'outer', 'cross'} Type of join to perform
            jinja_parameters_dict: Keyword parameters to pass into jinja tags.
            format_func_dict: A dictionary where the keys are column names and the values are callable
                that format the series when that column enters the DM. see [Format Tools](/auto/data_manager/#format-tools) for more information.
                Only applies to this frame.
            left_on: Column(s) within the target population dataframe to join on. If a tuple is passed both keys will be used for the merge
            left_index: Use the target population index as the join key.

        Returns:

        """

        if jinja_parameters_dict is None:
            _jinja_parameters_dict = {}
        else:
            _jinja_parameters_dict = jinja_parameters_dict

        config = _get_config_from_master(inner_path, self.jinja_repo_source)  # TODO replace with JinjaRepo.pull

        if config["meta"]["population"]:
            raise ConfigError(f'expected population status is False script got: {config["meta"]['population']}')

        right_on = config["meta"]["join_key"]

        if left_on:
            if isinstance(left_on, str):
                rename_dict = {left_on: right_on}
            else:
                rename_dict = {k: v for k, v in zip(left_on, right_on)}
        else:
            rename_dict = None

        con = self.jinja_repo_source.conn_list[config['meta']['connection']]

        sql = self.resolve_join_jinja_repo_template(inner_path, right_on, jinja_parameters_dict,
                                                    rename_columns=rename_dict,
                                                    temp_table_name=config["meta"]["insert_table_name"])
        df = query.execute_sql(sql, con)

        frame = meta.Frame(config["meta"]["name"], "JinjaRepo", df, sql=sql)

        self._join_from_frame(frame, right_on, how, format_func_dict, None, None, False,
                              False)  # TODO add join funcs to configs

    def join_from_dataframe(self, df: pd.DataFrame, on: str | tuple = None, how: JoinLiterals = "left",
                            frame_name: str = None,
                            format_func_dict: FormatDict | dict = None,
                            left_on: str | tuple = None, right_on: str | tuple = None,
                            left_index: bool = False, right_index: bool = False):
        """

        Joins a dataframe into the DataManager's (DM) target population.

        !!! warning
            Note that unlike the sql methods, the dataframe might have different granularity/records than the target populatoin.
            Take care when choosing join types. Inner joins are particular useful for filtering.

        Args:
            df: Dataframe to join.
            on: Column to join on. Must exist in both the target data frame and incoming dataframe.
                If a tuple is passed both keys will be used for the merge
            how: {'left', 'right', 'inner', 'outer', 'cross'} Type of join to perform
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to `unnamed-dataframe`.
            format_func_dict: A dictionary where the keys are column names and the values are callable
                that format the series when that column enters the DM. see [Format Tools](/auto/data_manager/#format-tools) for more information.
                Only applies to this frame.
            left_on: Column(s) name within the target population to join on. If a tuple is passed both keys will be used for the merge
            right_on: Column(s) name within the result of the query to join on.If a tuple is passed both keys will be used for the merge
            left_index: Use Target population index as join key
            right_index: Use Result of the query's index to join on.

        !!! example
            Main Python Script
            ```
            #Set the base population
            data = {
                'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
                'Age': [25, 30, 35, 40, 45],
                'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Boston'],
                'Salary': [80000, 90000, 100000, 110000, 120000]
            }
            df = pd.DataFrame(data)
            mipi = DataManager.from_dataframe(df)


            #Left Join in another column
            data_job = {
                'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
                'Job': ['Actor', 'Teacher', 'Mechanic', 'lawyer', 'Engineer']
            }
            df_job = pd.DataFrame(data)
            mipi.join_from_dataframe(df_job,on = "Name",how = "left")

            #Filter using inner join
            data_include = {
                'Name': [ 'Bob', 'Charlie'],
            }
            df_include = pd.DataFrame(data)
            mipi.join_from_dataframe(df_include,on = "Name",how = "inner")
            ```
            <details>
            <summary>Click to expand the accompanying output example</summary>
            This would result in the following dataframe

            | Name    | Age | City        | Salary | Job      |
            |---------|-----|-------------|--------|----------|
            | Bob     | 30  | Los Angeles | 90000  | Teacher  |
            | Charlie | 35  | Mechanic    | 100000 | Mechanic |
            </details>

        Returns:

        """

        _frame_name = frame_name or "unnamed-dataframe"
        frame = meta.Frame(_frame_name, "Data Frame", df.copy(), None, None)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def join_from_excel(self, excel_path: str, on: str = None, how: JoinLiterals = "left", frame_name: str = None,
                        excel_sheet: str | int = None, format_func_dict: FormatDict | dict = None,
                        left_on: str | tuple = None, right_on: str | tuple = None,
                        left_index: bool = False, right_index: bool = False):
        """

        A method of the DataManager (DM) that reads an excel file and joins it to the target population.
        !!! warning
            Note that unlike the sql methods, the dataframe might have different granularity/records than the target populatoin.
            Take care when choosing join types. Inner joins are particular useful for filtering.

        Args:
            excel_path: Absolute or relative path to the Microsoft Excel file.
            on: Column to join on. Must exist in both the target data frame and result of the Jinja SQL script.
                If a tuple is passed both keys will be used for the merge
            how: {'left', 'right', 'inner', 'outer', 'cross'} Type of join to perform
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to the name of the SQL script file.
            excel_sheet: sheet name(str) or sheet index(int)
            format_func_dict: A dictionary where the keys are column names and the values are callable
                that format the series when that column enters the DM. see [Format Tools](/auto/data_manager/#format-tools) for more information.
                Only applies to this frame.
            left_on: Column(s) name within the target population to join on. If a tuple is passed both keys will be used for the merge
            right_on: Column(s) name within the result of the query to join on. If a tuple is passed both keys will be used for the merge
            left_index: Use Target population index as join key
            right_index: Use Result of the query's index to join on.

    !!! example
        Main Python Script
        ```python
        from mipi_datamanager import DataManager

        mipi = DataManager.from_excel("path/to/excel_file.xlsx")
        #user left join to add columns
        mipi.join_from_dataframe("path/to/excel_file2.xlsx", on = "JoinColumn", how= "left")
        #use inner join to filter
        mipi.join_from_dataframe("path/to/excel_file3.xlsx", on = "JoinColumn", how= "inner")
        ```

        Returns:

        """
        _frame_name = _maybe_get_frame_name(frame_name, excel_path)
        df = pd.read_excel(excel_path, sheet_name=excel_sheet or 0)
        frame = meta.Frame(_frame_name, "Excel", df, None, None)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def join_from_format_sql(self, script_path: str, connection: connection.Odbc, on: str | tuple = None,
                             how: JoinLiterals = "left",
                             format_parameters_list: list = None,
                             frame_name: str = None, format_func_dict: FormatDict | dict  = None,
                             left_on: str | tuple = None, right_on: str | tuple = None,
                             left_index: bool = False, right_index: bool = False):
        """

        Inserts the records contained in the target population into a format SQL script template, this creates a script
        whose records match the target population. Then runs the script and Joins the results into the DataManager's target population.

        !!! info "Script Setup"
            This script must be setup to accept a temp table from the data manager. The SQL script uses python string formatting syntax.
            You can place optional placeholders '{}' in your script to accept the parameters of 'format_parameters_list'.
            This script assumes that the first placeholder '{}' is where the temp table will be inserted. The following
            placeholders will be used for format parameters.

        Args:
            script_path: The absolute or relative path to the SQL script.
            connection: MiPi Connection Object
            on: Column to join on. Must exist in both the target data frame and result of the SQL script.
                If a tuple is passed both keys will be used for the merge
            how: {'left', 'right', 'inner', 'outer', 'cross'} Type of join to perform
            format_parameters_list: A list of values to be placed into string format placeholders "{}".
                Values will be entered into placeholders in the order of the list.
                This is equivalent to using python string formatting ie. `"{} {}".format(["hello","world"])`
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to the name of the SQL script file.
            format_func_dict: A dictionary where the keys are column names and the values are callable
                that format the series when that column enters the DM. see [Format Tools](/auto/data_manager/#format-tools) for more information.
                Only applies to this frame.
            left_on: Column(s) name within the target population to join on. If a tuple is passed both keys will be used for the merge
            right_on: Column(s) name within the result of the query to join on. If a tuple is passed both keys will be used for the merge
            left_index: Use Target population index as join key
            right_index: Use Result of the query's index to join on.

        !!! example
            Main Python Script
            ```python
            from mipi_datamanager import DataManager
            from mipi_datamanager.odbc import Odbc

            con = Odbc(dsn = "my_dsn")

            mipi = DataManager.from_jinja("path/to/sql_script.sql",con)

            jinja_parameters_dict = {
              "param1":"val1",
              "param2":"val2"
            }

            mipi.join_from_jinja("path/to/sql_script.sql",con,
                                 jinja_parameters_dict=jinja_parameters_dict)
            ```
            <details>
            <summary>Click to expand a SQL Example</summary>
            SQL Template
            ```tsql
            {}

            SELECT tmp.PrimaryKey,Value2
            FROM #MiPiTempTable as tmp
            LEFT JOIN foreign_table ft
                ON tmp.PrimaryKey = ft.Value2;
            WHERE param1 = {}
            AND   param2 = {}

            ```

            Resolved Query
            ```tsql
            CREATE TEMPORARY TABLE #MiPiTempTable (PrimaryKey);
            INSERT INTO #MiPiTempTable Values (1)
            INSERT INTO #MiPiTempTable Values (2)
            INSERT INTO #MiPiTempTable Values (3)

            SELECT tmp.PrimaryKey,Value2
            FROM #MiPiTempTable as tmp
            LEFT JOIN foreign_table ft
                ON tmp.PrimaryKey = ft.Value2;
            WHERE param1 = param_val1
            AND   param2 = param_val2
            ```
            </details>
        """

        _frame_name = _maybe_get_frame_name(frame_name, script_path)

        if on:
            _on = on
            rename_dict = None
        elif left_on:  # TODO add index
            _on = right_on
            if isinstance(left_on, str):
                rename_dict = {left_on: right_on}
            else:
                rename_dict = {k: v for k, v in zip(left_on, right_on)}
        # elif left_index: #TODO add index
        #     _on =
        #     if isinstance(left_on, str):
        #         rename_dict = {left_on: right_on}
        #     else:
        #         rename_dict = {k: v for k, v in zip(left_on, right_on)}
        else:
            raise MergeError("Must define either 'on' or 'left/right")

        sql = self.resolve_join_format_sql_file(script_path, _on, format_parameters_list, rename_columns=rename_dict)
        df = query.execute_sql(sql, connection)

        frame = meta.Frame(_frame_name, "Format SQL", df, sql=sql)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def join_from_jinja(self, script_path: str, connection: connection.Odbc, on: str | tuple = None,
                        how: JoinLiterals = "left",
                        jinja_parameters_dict: dict = None,
                        frame_name: str = None, format_func_dict: dict = None,
                        left_on: str | tuple = None, right_on: str | tuple = None,
                        left_index: bool = False, right_index: bool = False,
                        insert_table_name: str = "MiPiTempTable"):

        """

        Inserts the records contained in the target population into a Jinja SQL script template, this creates a script
        whose records match the target population. Then runs the script and Joins the results into the DataManager's target population.

        !!! info "Script Setup"
            This script must be setup to accept a temp table from the data manager. The SQL script uses Jinja syntax, see [Jinja2 official documentation](https://jinja.palletsprojects.com/en/3.1.x/)
            You can place optional jinja tags '{{...}}' to accept the keyword pairs of 'jinja_parameters_dict'.
            This script is expected to have a tag for the temp table "{{MiPiTempTable}}"

        Args:
            script_path: The absolute or relative path to the Jinja SQL script.
            connection: MiPi Connection Object
            on: Column to join on. Must exist in both the target data frame and result of the Jinja SQL script.
                If a tuple is passed both keys will be used for the merge
            how: {'left', 'right', 'inner', 'outer', 'cross'} Type of join to perform
            jinja_parameters_dict: Keyword parameters to pass into jinja tags.
            frame_name: Name that the frame is stored as in the DM.
                If `None` the frame name will default to the name of the SQL script file.
            format_func_dict: A dictionary where the keys are column names and the values are callable
                that format the series when that column enters the DM. see [Format Tools](/auto/data_manager/#format-tools) for more information.
                Only applies to this frame.
            left_on: Column name within the target population to join on.
            right_on: Column name within the result of the query to join on.
            left_index: Use Target population index as join key
            right_index: Use Result of the query's index to join on.
            insert_table_name: Name of the jinja tag to insert the temp table into

        !!! example
            Main Python Script
            ```python
            from mipi_datamanager import DataManager
            from mipi_datamanager.odbc import Odbc

            con = Odbc(dsn = "my_dsn")

            mipi = DataManager.from_jinja("path/to/sql_script.sql",con)

            jinja_parameters_dict = {
              "param1":"val1",
              "param2":"val2"
            }

            mipi.join_from_jinja("path/to/sql_script.sql",con,
                                 jinja_parameters_dict=jinja_parameters_dict)
            ```
            <details>
            <summary>Click to expand a detailed Example</summary>
            Jinja SQL Template
            ```tsql
            {{MiPiTempTable}}

            SELECT tmp.PrimaryKey,Value2
            FROM #MiPiTempTable as tmp
            LEFT JOIN foreign_table ft
                ON tmp.PrimaryKey = ft.Value2;
            WHERE param1 = {{ param1 }}
            AND   param2 = {{ param2 }}
            ```

            Resolved Query
            ```tsql
            CREATE TEMPORARY TABLE #MiPiTempTable (PrimaryKey);
            INSERT INTO #MiPiTempTable Values (1)
            INSERT INTO #MiPiTempTable Values (2)
            INSERT INTO #MiPiTempTable Values (3)

            SELECT tmp.PrimaryKey,Value2
            FROM #MiPiTempTable as tmp
            LEFT JOIN foreign_table ft
                ON tmp.PrimaryKey = ft.Value2;
            WHERE param1 = param_val1
            AND   param2 = param_val2
            ```
            </details>

        """

        _frame_name = _maybe_get_frame_name(frame_name, script_path)

        if on:
            _on = on
            rename_dict = None
        elif left_on:
            _on = right_on
            if isinstance(left_on, str):
                rename_dict = {left_on: right_on}
            else:
                rename_dict = {k: v for k, v in zip(left_on, right_on)}
        else:
            raise MergeError("Must define either 'on' or 'left/right")

        # elif left_index: # TODO
        #     pass

        sql = self.resolve_join_jinja_template(script_path, _on, jinja_parameters_dict=jinja_parameters_dict,
                                               rename_columns=rename_dict, insert_table_name=insert_table_name)
        df = query.execute_sql(sql, connection)

        frame = meta.Frame(_frame_name, "Jinja", df, sql=sql)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def _join_from_frame(self, frame: meta.Frame, on: str, how: JoinLiterals,
                         format_func_dict, left_on, right_on, left_index, right_index):
        """Joins a frame into target population. used by used join functions"""

        local_join_formatter = _FormattedFunctions(format_func_dict)
        final_formatter = _FormattedJoinOperation([local_join_formatter, self.default_formatter])
        frame.df_query = final_formatter.format_incoming_df(frame.df_query)

        self._target_population = self._target_population.merge(frame.df_query, how=how, on=on, left_on=left_on,
                                                                right_on=right_on, left_index=left_index,
                                                                right_index=right_index)
        frame_idx = len(self._frames)
        frame._set_target(self._target_population)
        self._set_column_source_from_frame(frame, frame_idx)

        if not self.store_deep_frames:
            del frame.df_query
            del frame.df_target

        self._store_frame(frame, frame_idx)

    def _set_column_source_from_frame(self, frame, idx) -> None:
        """
        appends the source column dictionary
        self.source_columns[column_name] = frame_index
        also renames duplicated columns x,y -> '~frame'
        rename also changes the source column dictionary, however it keeps the original value which contains no suffix\
        this identifies any future use of that column as a dupe.
        """

        # loop current frames query
        for column in frame.query_columns:

            # add new column to source dict
            if column not in self._column_sources:
                # no dupe -> assign to source columnm
                self._column_sources[column] = idx

            # for duplicate columns: add to source list and rename suffixes
            if ((f"{column}_x" in self._target_population.columns)
                    and (f"{column}_y" in self._target_population.columns)):
                warnings.warn(
                    f"\nColumn {column} was duplicated during a join.\nThe duplicated column suffixes were renamed in accordance with their origin frame.\ncoalesce duplicate columns with mipi.",
                    stacklevel=2)

                # col origonal source
                old_idx = self._column_sources[column]

                # assign rename vals for join suffixes x,y -> '~frame'
                x_old_target_column_name = f"{column}_x"
                y_old_target_column_name = f"{column}_y"
                x_new_target_column_name = f"{column}~{self._frames[old_idx].name}_{old_idx}"
                y_new_target_column_name = f"{column}~{frame.name}_{idx}"

                # rename target
                self._target_population = self._target_population.rename(
                    columns={x_old_target_column_name: x_new_target_column_name,
                             y_old_target_column_name: y_new_target_column_name})

                # rename source dict to deal with future dupes
                self._column_sources[x_new_target_column_name] = old_idx
                self._column_sources[y_new_target_column_name] = idx

            # third+ dupe will already exist in column key and will be added to the target without a suffix, needs rename
            if (column in self._column_sources
                    and any(f"{column}~{frame.name}" in col for col in self._column_sources)
                    and column in self._target_population.columns):
                self._column_sources[f"{column}~{frame.name}_{idx}"] = idx
                self._target_population = self._target_population.rename(
                    columns={column: f"{column}~{frame.name}_{idx}"})

    ##############################################################################################
    # Target Data Transformations
    ##############################################################################################

    def set_jinja_repo_source(self, jinja_repo_source: JinjaRepo) -> None:

        """
        Defines the jinja repo for this object. This allows queries from the repo. The repo can not be overwritten,
        you need to create a new object instead.

        Args:
            jinja_repo_source:

        Returns:

        """

        if self.jinja_repo_source:
            raise AttributeError(
                f"Mipi object {repr(self)} has already been set. Create a new mipi object, or clone this one to set a different sql repo source")
        else:
            self.jinja_repo_source = jinja_repo_source

    def filter(self, mask: Mask):
        """Filters the target population using a mask.
        use self.trgt[] for the mask"""
        self._target_population = self._target_population[mask]

    def clone(self, base_name: str = None,
              change_jinja_repo_source: JinjaRepo = None,
              store_deep_frames: bool = False, store_deep_base: bool = False,
              rename_columns_dict: dict = None,
              add_to_default_format_func_dict: dict = None):

        """

        Args:
            base_name:
            change_jinja_repo_source:
            store_deep_frames:
            store_deep_base:
            rename_columns_dict:
            add_to_default_format_func_dict:

        Returns:

        """

        df = self.trgt.copy()

        _jinja_repo_source = change_jinja_repo_source or self.jinja_repo_source

        # rename columns to declare new PKs
        if rename_columns_dict is not None:
            df = df.rename(columns=rename_columns_dict)

        base_name = base_name or f"Clone from: {repr(self)}"  # TODO change this

        assert isinstance(add_to_default_format_func_dict, (dict, type(None))), "Format Dict must be type dict"
        if add_to_default_format_func_dict is not None:
            if self._user_added_func_dict is not None:
                new_format_dict = self._user_added_func_dict
            else:
                new_format_dict = dict()
            for k, v in add_to_default_format_func_dict.items():
                new_format_dict.update({k: v})
        else:
            new_format_dict = self._user_added_func_dict

        frame = meta.Frame(base_name, "Clone", df, None, None)

        cls = self.__class__

        mipi2 = cls(frame, jinja_repo_source=_jinja_repo_source,
                    store_deep_frames=store_deep_frames, store_deep_base=store_deep_base,
                    default_format_func_dict=new_format_dict)

        return mipi2

    def get_temp_table(self, key: str, frame=None, rename_columns: dict | None = None):  # TODO test from specific frame
        """Get the most current list of inserts where 'on' is the insert key"""

        df = frame.df_query if frame is not None else self.trgt
        if rename_columns:
            df = df.rename(columns=rename_columns)
        if self.dialect == 'mssql':
            if isinstance(key, str):
                return generate_inserts.generate_mssql_inserts(df[[key]], make_temptable=True)
            elif isinstance(key, (tuple, list)):
                key = com._maybe_convert_tuple_to_list(key)
                return generate_inserts.generate_mssql_inserts(df[key], make_temptable=True)

    def resolve_join_format_sql(self, sql: str, key: str, format_parameters_list=None, frame=None,
                                rename_columns: dict | None = None):
        inserts = self.get_temp_table(key, frame=frame, rename_columns=rename_columns)
        if format_parameters_list:
            _format_parameters_list = [inserts] + format_parameters_list
        else:
            _format_parameters_list = [inserts]

        sql = sql.format(*_format_parameters_list)
        return sql

    def resolve_join_format_sql_file(self, file_path: str, key: str, format_parameters_list=None, frame=None,
                                     rename_columns: dict | None = None):
        sql = self._read_file(file_path)
        return self.resolve_join_format_sql(sql, key, format_parameters_list, frame=frame,
                                            rename_columns=rename_columns)

    def _get_sql_from_jinja_template(self, jenv, script_path, jinja_parameters_dict):
        sql = jenv.resolve_file(script_path, jinja_parameters_dict)
        del jenv
        return sql

    def _maybe_get_jinja_insert_dict(self, key, jinja_parameters_dict=None, frame=None, rename_columns=None,
                                     insert_table_name: str = "MiPiTempTable"):
        if jinja_parameters_dict:
            jinja_parameters_dict[insert_table_name] = self.get_temp_table(key, frame=frame,
                                                                           rename_columns=rename_columns)
        else:
            jinja_parameters_dict = {
                insert_table_name: self.get_temp_table(key, frame=frame, rename_columns=rename_columns)}
        return jinja_parameters_dict

    def resolve_join_jinja_repo_template(self, inner_path, key, jinja_parameters_dict, frame=None,
                                         rename_columns: dict | None = None, temp_table_name: str = "MiPiTempTable"):
        jenv = JinjaRepo(self.jinja_repo_source.root_dir)
        jinja_parameters_dict = self._maybe_get_jinja_insert_dict(key, jinja_parameters_dict, frame, rename_columns,
                                                                  insert_table_name=temp_table_name)
        sql = self._get_sql_from_jinja_template(jenv, inner_path, jinja_parameters_dict)
        return sql

    def resolve_join_jinja_template(self, script_path, key, jinja_parameters_dict, frame=None,
                                    rename_columns: dict | None = None, insert_table_name: str = "MiPiTempTable"):
        path = Path(script_path)
        jenv = JinjaLibrary(path.parent)
        jinja_parameters_dict = self._maybe_get_jinja_insert_dict(key, jinja_parameters_dict, frame, rename_columns,
                                                                  insert_table_name=insert_table_name)
        sql = self._get_sql_from_jinja_template(jenv, path.name, jinja_parameters_dict)

        return sql

    def resolve_join_jinja(self, script: str, key: str, jinja_parameters_dict: dict, frame=None,
                           rename_columns: dict | None = None, insert_table_name: str = "MiPiTempTable"):
        template = Template(script)
        jinja_parameters_dict = self._maybe_get_jinja_insert_dict(key, jinja_parameters_dict, frame, rename_columns,
                                                                  insert_table_name=insert_table_name)
        return template.render(jinja_parameters_dict)

    def _read_file(self, path):
        with open(path, "r") as f:
            contents = f.read()
        return contents

    @property
    def base_population(self) -> pd.DataFrame:

        """
        The dataframe used to create the DataManager Object. This attribute is only stored if
        `store_deep_base = True` or if `store_deep_frames = True` during initialization.
        The meta data for this dataframe is represented in the zeroth Frame in `DataManager.frames`.
        Initially this dataframe defines the granularity and records that are used
        in subsequent queries.

        Returns: self._frames[0].df_query

        Raises:
            AttributeError: If `store_deep_base` or `store_deep_frames` is False, indicating that the base population
                was not saved to the object.

        """

        if self.store_deep_base or self.store_deep_frames:
            return self._frames[0].df_query  # first frame
        else:
            raise AttributeError(
                "base_population is not available because store_deep_base and store_deep_frames are False.")

    @property
    def target_population(self) -> pd.DataFrame:
        """
        This is the "working dataframe" where all changes are applied. Initially it is equal to the `base_population`.
        The meta data for this dataframe is always represented by the maximum in `DataManager.frames`
        This property is writable, but it is recommended to extract the dataframe from the object before editing it.

        Returns: The final dataframe with all operations applied to it.

        See Also:
            [rename_select_columns][mipi_datamanager.wrangle.rename_select_columns]: Your final data set will have extra columns with generalized names.
        """
        return self._target_population

    @target_population.setter
    def target_population(self, target_population):
        self._target_population = target_population

    @property
    def trgt(self):
        """
        This is a read only abbreviated property of the `target_population` dataframe. It is useful for creating
        creating boolean masks.

        Examples:
             >>> dm = DataManager.from_sql(...)
             >>> mask = dm.trgt["column1"] == "my value"
             mask = pd.Series(True,False,True,True)

        Returns: self.target_population

        """
        return self._target_population

    def print_target_columns(self) -> list:
        """
        Returns: List of all columns currently in the target population dataframe
        """
        print(self._target_population.columns.tolist())

    def print_target_column_dict(self):

        """
        A string representation of a dictionary of the columns in the target population dataframe.
        Useful when combined with [rename_selected_columns][mipi_datamanager.wrangle.rename_select_columns]
        """

        col_dict = com._columns_to_dict(self.trgt)
        col_dict_str = com._dict_to_string(col_dict)
        col_dict_str = "columns.rename_select_columns(\n{" + col_dict_str + "})"
        print(col_dict_str)

    @property
    def duplicated_columns(self) -> list:
        """

        List of all columns in the target dataframe that contain a "~" character. When duplicate columns
        are created due to a MiPi join, both duplicate columns will be renamed with a tilde followed by their origin frame.
        This property indicates all values which have been duplicated but have not been renamed or removed.

        Returns: A list of all columns containing a tilde.

        See Also:
            - [coalesce][mipi_datamanager.wrangle.coalesce]: to remove duplicate columns
            - [rename_select_columns][mipi_datamanager.wrangle.rename_select_columns]: to select and rename your prefered column
        """
        return [col for col in self._target_population.columns if "~" in col]  # TODO check if it is a frame name

    @property
    def frames(self) -> com.IndexedDict:
        """
        A dictionary where each entry is a [frame][mipi_datamanager.core.meta.Frame]. A frame represents a snapshot of
        current DataManager its dataframes. Frames are stored in an "indexed dictionary".
        Every frame is suffixed by its index, starting at 0 with the initial base population. Frames can be accessed
        by their integer index or by their full name.

        Examples:
            >>> DataManager.frames["my_base_frame_0"]
            >>> DataManager.frames[0]
        """

        return self._frames
