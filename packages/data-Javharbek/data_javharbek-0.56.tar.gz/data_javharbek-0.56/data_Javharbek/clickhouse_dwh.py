import pandas as pd
from datetime import date
import clickhouse_connect
from pyspark.sql.functions import collect_list
from .my_module5 import *
import html


def escape_special_characters_for_sql(value):
    """
    Экранирует специальные символы для SQL-запроса, убирая риск SQL-инъекций.

    Аргументы:
    value -- строка или значение, которое нужно экранировать.

    Возвращает:
    Экранированная строка.
    """
    # Преобразуем значение в строку
    value_str = str(value)

    # Экранируем одинарные кавычки и обратные слэши
    escaped_value = value_str.replace("'", "\\'").replace("\\", "\\\\")

    return escaped_value
def format_value_clickhouse(value):
    value = escape_special_characters_for_sql(value)
    if pd.isna(value):
        return 'NULL'
    elif isinstance(value, str):
        return "'{}'".format(value.replace("'", "''"))
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, pd.Timestamp):
        return "'{}'".format(value.strftime('%Y-%m-%d %H:%M:%S.%f'))
    else:
        raise ValueError(f"Unsupported data type: {type(value)}")

def execute_sql_clickhouse(sql,host,port,username,password):
    client = clickhouse_connect.get_client(host=host,port=port, username=username, password=password)
    client.command(sql)
def execute_sql_all_clickhouse(sql_all,host,port,username,password):
    print("execute_sql_all_clickhouse da sql_all:")
    print(sql_all)
    if len(sql_all) == 0:
        print("sql all is empty")
        return
    for sql in sql_all:
        print("start execute_sql_clickhouse: ")
        execute_sql_clickhouse(sql,host,port,username,password)


def delete_query_for_df_clickhouse(cond_df, id_column='ID', chunk_batch_size=1000):
    if cond_df.count() == 0:
        return []
    ids = cond_df.select(id_column)
    ids_list_df = ids.agg(collect_list(id_column).alias("ids"))
    ids_list = ids_list_df.first()["ids"]

    chunks = list(chunk_list(ids_list, chunk_batch_size))

    delete_queries = []

    for chunk in chunks:
        ids_str = ','.join(map(str, chunk))
        delete_query = f"ALTER TABLE nps_details DELETE WHERE ID IN ({ids_str})"
        delete_queries.append(delete_query)

    return delete_queries

def get_query_spark_clickhouse(query,user,password,driver,url,spark):
    properties = {
        "user": user,
        "password": password,
        "driver": driver
    }
    return spark.read.jdbc(url=url, table=query, properties=properties)
def is_new_data_clickhouse(val_id, val_date, table_name, col_id, col_date,user,password,driver,url,spark):
    query_all_in_id = is_new_data_clickhouse_sql(val_id,table_name, col_id, col_date)
    print("query_all_in_id in is_new_data_clickhouse:")
    print(query_all_in_id)
    df_clickhouse = get_query_spark_clickhouse(query_all_in_id,user,password,driver,url,spark)
    print("df_clickhouse in is_new_data_clickhouse:")
    print(df_clickhouse)

    if df_clickhouse.count() == 0:
        return True

    item = df_clickhouse.first()
    print("item = df_clickhouse.first()")
    print(item)
    item_date = item[col_date]
    print("item_date in is_new_data_clickhouse:")
    print(item_date)
    if val_date is not None:
        if isinstance(item_date, (datetime, date)):
            val_date = datetime.strptime(val_date, '%Y-%m-%d').date() if isinstance(item_date, date) else datetime.strptime(
                val_date, '%Y-%m-%d %H:%M:%S.%f')
        result = item_date < val_date
        print("result if isinstance: ")
        print(result)
        return result
    return False
def is_new_data_clickhouse_sql(val_id, table_name, col_id, col_date,is_str=False):
    query_all_in_id = f"(SELECT {col_id},{col_date} FROM {table_name} WHERE {col_id} = {val_id}) AS subquery"
    if is_str:
        query_all_in_id = f"(SELECT {col_id},{col_date} FROM {table_name} WHERE {col_id} = '{val_id}') AS subquery"
    return query_all_in_id
# helper
def update_query_for_df_clickhouse(cond_df,isOnlyNew = False,table_name = None,col_id = 'ID',col_date = None,user = None,password = None,driver = None,url = None,spark = None):
    if cond_df.count() == 0:
        return []
    data_dict = cond_df.toPandas().to_dict(orient='records')
    update_queries = []
    for record in data_dict:
        id = record.pop(col_id)
        if isOnlyNew == True:
            date_value = record[col_date]
            is_new_data_ok = is_new_data_clickhouse(id,date_value,table_name,col_id,col_date,user,password,driver,url,spark)
            if not is_new_data_ok :
                continue
        update_set_clause = ', '.join([f"{col} = {format_value_clickhouse(value)}" for col, value in record.items()])
        print(update_set_clause)
        update_query = f"""
        ALTER TABLE {table_name} UPDATE {update_set_clause}
        WHERE {col_id} = {id}
        """
        update_queries.append(update_query)
        print(update_queries)
    return update_queries
