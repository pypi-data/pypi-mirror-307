from jinja2 import Template
import pandas as pd

def _validate_insert_table_name(insert_table_name):
    if "#" in insert_table_name:
        raise ValueError("Can not enter '#' in insert_table_name, use keyword: 'make_temptable' instead")

def _append_temp_table_name(insert_table_name):
    return "#" + insert_table_name

def _get_col_dtypes(df, convert_dtypes = True):
    if convert_dtypes:
        _df = df.convert_dtypes() #TODO check me

    dtype_mapping = {
        'int64': 'INT',
        'float64': 'FLOAT',
        'object': 'NVARCHAR(MAX)',
        'bool': 'BIT',
        'datetime64[ns]': 'DATETIME',
    }

    return [(col, dtype_mapping.get(str(df[col].dtype), 'NVARCHAR(MAX)')) for col in df.columns]

def _get_join_key_values(df):
    # Step 3: Prepare rows for insertion
    rows = []
    for _, row in df.iterrows():
        formatted_row = []
        for val in row:
            if pd.isna(val):
                formatted_row.append('NULL')
            elif isinstance(val, str):
                formatted_row.append(f"'{val}'")
            else:
                formatted_row.append(str(val))
        rows.append(formatted_row)
    return rows

def _render_insert_header(insert_table_name,col_types,joinkey_values):
    # Step 4: Define the Jinja template for the SQL script
    sql_template = """SET NOCOUNT ON;
    CREATE TABLE {{ temp_table_name }} (
        {%- for column, dtype in columns %}
        {{ column }} {{ dtype }}{%- if not loop.last %},{% endif %}
        {%- endfor %}
    );
{% for row in rows %}
    INSERT INTO {{ temp_table_name }} ({{ columns | map(attribute=0) | join(', ') }}) VALUES ({{ row | join(', ') }});
{%- endfor %}
    """

    # Step 5: Create a Jinja template object and render it
    template = Template(sql_template)
    rendered_sql = template.render(temp_table_name=insert_table_name, columns=col_types, rows=joinkey_values)

    return rendered_sql

def generate_mssql_inserts(df, insert_table_name="MiPiTempTable", make_temptable=True) -> str:
    _validate_insert_table_name(insert_table_name)
    if make_temptable:
        insert_table_name = _append_temp_table_name(insert_table_name)
    col_types = _get_col_dtypes(df)
    join_key_values = _get_join_key_values(df)
    return _render_insert_header(insert_table_name,col_types,join_key_values)

    # TODO drop values after