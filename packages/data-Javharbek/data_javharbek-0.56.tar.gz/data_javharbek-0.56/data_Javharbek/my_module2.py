# increment load task
from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.http.operators.http import SimpleHttpOperator
import pandas as pd
import os
from datetime import datetime
import tempfile
import random
from airflow.decorators import dag, task
from datetime import datetime
import math
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import oracledb
from airflow.providers.oracle.hooks.oracle import OracleHook
import traceback
import sys
import requests
from pandas.core.interchange.dataframe_protocol import DataFrame
from requests.auth import HTTPBasicAuth
from airflow.hooks.base_hook import BaseHook
import pyarrow as pa
import pyarrow.parquet as pq
from .my_module5 import *

def get_one_from_table_by_column_equal_config_task(table_name, id, column='id'):
    sql = f"""
    SELECT * FROM {str(table_name)} WHERE {column} = '{id}' LIMIT 1
"""
    print("sql:")
    print(sql)

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()

    df = pd.read_sql(sql, conn)

    if df.empty:
        print(str(table_name) + ": rows are empty " + str(id))
        raise ValueError(str(table_name) + ": rows are empty " + str(id))

    row = df.iloc[0]

    print(str(table_name) + " / " + str(id))
    print(row)

    return row

def fetch_scalar_result_int_config(query_sql):

    # Подключаемся к PostgreSQL и выполняем запрос
    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()

    cur = conn.cursor()
    cur.execute(query_sql)
    one = cur.fetchone()

    # Получаем количество записей
    result = one[0] if one else 0
    cur.close()

    return result

def create_execute_tasks(target_table_name,target_type):
    print("create_execute_tasks: start")
    counts = get_count_waiting_tasks(target_table_name,target_type)
    if counts == 0:
        print("create_execute_tasks: waiting count is zero")
        return
    df = get_waitings_tasks(target_table_name,target_type)
    if df.empty:
        print("create_execute_tasks: waiting data is empty")
        return
    operators = []

    first_row = df.iloc[0]
    plan_id = first_row['plan_id']
    print("plan_id: " + str(plan_id))
    print("first_row: " + str(first_row))

    plan = get_one_from_table_by_column_equal_config_task('incremental_load_plans', plan_id, column='id')
    work_day_begin_interval = str(plan['work_day_begin_interval'])
    work_day_end_interval = str(plan['work_day_end_interval'])
    print("plan:")
    print(plan)

    check_time_raise(work_day_begin_interval,work_day_end_interval)

    max_thread_counts = int(plan['max_thread_counts'])
    print("max_thread_counts: " + str(max_thread_counts))

    for index, row in df.iterrows():
        if(max_thread_counts < (index + 1)):
            break
        print("create_execute_tasks: ")
        print(f"Row {index} data:")
        print(row)
        sql_query_raw = row['sql_query_raw']
        sql_count_raw = row['sql_count_raw']
        print("sql_query_raw:" + sql_query_raw)
        print("sql_count_raw:" + sql_count_raw)

        make_query_migrate_to_storage_task = PythonOperator(
            task_id=f'make_query_migrate_to_storage_task_{index}',
            python_callable=make_query_migrate_to_storage,
            op_args=[row]
        )
        operators.append(make_query_migrate_to_storage_task)
        print("create_execute_tasks: assign task")

    print("create_execute_tasks: end")
    return operators

def create_load_file_record(filename, filepath, table_name, storage_type, storage_name, bucket, file_type, counts_rows,
                            min_id, max_id, type_data, min_datetime, max_datetime,plan_id,task_id,task_created_at):
    """
    Создает запись в таблице load_files.

    :param filename: Имя файла
    :param filepath: Путь к файлу
    :param table_name: Имя таблицы
    :param storage_type: Тип хранилища
    :param storage_name: Имя хранилища
    """
    # Получите соединение с PostgreSQL из Airflow
    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Получите текущее время
    created_at = datetime.utcnow()

    # SQL-запрос для вставки данных
    sql = """
    INSERT INTO load_files (filename, filepath, created_at, table_name, storage_type, storage_name, bucket, file_type,counts_rows,min_id,max_id,type_data,min_datetime,max_datetime,plan_id,task_id,task_created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Выполните SQL-запрос
    cur.execute(sql, (
    filename, filepath, created_at, table_name, storage_type, storage_name, bucket, file_type, counts_rows, min_id,
    max_id, type_data, min_datetime, max_datetime,plan_id,task_id,task_created_at))

    # Зафиксируйте изменения
    conn.commit()

    # Закройте соединение
    cur.close()
    conn.close()


def make_query_migrate_to_storage(row):
    query = row['sql_query_raw']
    target_table_name = row['table_name']
    operation_type = row['operation_type']
    type_id = row['type_id']
    column_id = row['column_id']
    id = row['id']
    plan_id = row['plan_id']
    created_at = row['created_at']
    status = row['status']
    query_connection_id = row['connection_id']
    driver_db_name = row['driver_db_name']

    if status != 'WAITING':
        print("On executing on another task")
        return

    state_current_datetime = row['state_current_datetime']
    hook = None
    try:
        # update_status_tasks(id, 'EXECUTING')
        if driver_db_name == 'ORACLE':
            hook = OracleHook(oracle_conn_id=query_connection_id)
        elif driver_db_name == 'POSTGRES':
            hook = PostgresHook(postgres_conn_id=query_connection_id)
        else:
            raise ValueError("Invalid driver db name")
        conn = hook.get_conn()
        df = pd.read_sql(query, conn)
        if df.empty:
            update_status_tasks(id, 'COMPLETE')
            print("data is empty")
            return
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        counts_rows = df.shape[0]  # Количество строк в DataFrame

        filename = f'{target_table_name}_{operation_type}_{type_id}_incremental_{current_time}_{id}_{plan_id}_.parquet'
        min_id = 0
        max_id = 0

        if type_id == "INC":
            min_id = df[column_id].min()
            max_id = df[column_id].max()
        for column in df.columns:
            unique_type = df[column].apply(type).unique()[0]
            # Print the column name and its unique types
            print(f"Column '{column}' has types: {df[column].dtype} == {unique_type}")

            if unique_type is dict:
                print("The element is a dictionary.")
                df[column] = df[column].apply(lambda x: str(x))
            else:
                print("The element is not a dictionary.")

        # Сохраняем данные во временную папку в формате Parquet
        with tempfile.TemporaryDirectory() as tmpdirname:
            parquet_file_path = os.path.join(tmpdirname, filename)
            #table = pa.Table.from_pandas(df)
            #pq.write_table(table, parquet_file_path)

            df.to_parquet(parquet_file_path, index=False)

            uploaded_data = migrate_data_to_storage(parquet_file_path,filename,target_table_name)
            storage_type = uploaded_data['storage_type']
            storage_s3_bucket_name = uploaded_data['storage_s3_bucket_name']
            storage_file_full_path = uploaded_data['storage_file_full_path']
            storage_connection_id = uploaded_data['storage_connection_id']
            print("uploaded_data:" + str(uploaded_data))

            counts_rows = int(counts_rows)
            min_id = int(min_id)
            max_id = int(max_id)

            create_load_file_record(filename, storage_file_full_path, target_table_name, storage_type, storage_connection_id, storage_s3_bucket_name,
                                    'parquet', counts_rows, min_id, max_id, operation_type, state_current_datetime,
                                    None, plan_id, id,created_at)
            print(f'make_query_migrate_to_storage >> INC: Data saved to {parquet_file_path}')
        update_status_tasks(id, 'COMPLETE')
        print(f'make_query_migrate_to_storage >> COMPLETE: {id}')
    except Exception as e:
        update_status_tasks(id, 'ERROR')
        # Capture the traceback as a string
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        update_message_tasks(id, str(tb_str))
        print("ERROR: " + str(tb_str))
        raise ValueError("Error on Execute Task")

def get_storage_host(tablename):
    sql = f"""
    SELECT * FROM (
    (SELECT *,1 as sort_storage FROM storage_hosts WHERE in_rotation IS TRUE AND for_table LIKE '{tablename}' ORDER BY RANDOM() LIMIT 1)
    UNION ALL
    (SELECT *,2 as sort_storage FROM storage_hosts WHERE in_rotation IS TRUE AND for_table IS NULL ORDER BY RANDOM() LIMIT 1)
    ) t ORDER BY sort_storage ASC LIMIT 1
"""

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()

    df = pd.read_sql(sql, conn)

    if df.empty:
        print("get_storage_hosts: storage hosts are empty")
        raise ValueError("get_storage_hosts: storage hosts are empty")

    storage_row = df.iloc[0]

    print(storage_row['connection_id'])

    return storage_row

def migrate_data_to_storage(file_path_local,filename,tablename):
    storage_row = get_storage_host(tablename)
    storage_connection_id = storage_row['connection_id']
    storage_type = storage_row['type']
    storage_in_rotation = storage_row['in_rotation']
    storage_extra = storage_row['extra']
    storage_s3_key = storage_row['s3_key']
    storage_s3_bucket_name = storage_row['s3_bucket_name']
    storage_hdfs_endpoint_path = storage_row['hdfs_endpoint_path']
    file_full_path = ""
    if storage_type == 'MINIO':
        key = storage_s3_key + '/' + filename
        s3_hook = S3Hook(aws_conn_id=storage_connection_id)
        s3_hook.load_file(filename=file_path_local, key=key, bucket_name=storage_s3_bucket_name, replace=True)
        file_full_path = key
    elif storage_type == 'HDFS':
        file_full_path = storage_hdfs_endpoint_path + '/' + filename
        upload_to_hdfs(file_path_local,file_full_path,storage_connection_id)
    else:
        raise ValueError("Unknown storage type")

    return {
        'storage_file_full_path': file_full_path,
        'storage_s3_bucket_name': storage_s3_bucket_name,
        'storage_type': storage_type,
        'storage_connection_id': storage_connection_id
    }


def upload_to_hdfs(file_path, hdfs_path, connection_id):
    # Fetch connection details from Airflow using the connection ID
    conn = BaseHook.get_connection(connection_id)

    # Extract connection parameters
    hdfs_host = conn.host
    hdfs_port = conn.port if conn.port else 50070  # Default to 50070 if not specified
    user = conn.login if conn.login else 'hdfs'  # Default to 'hdfs' user if not specified
    password = conn.password
    extra = conn.extra_dejson

    # Set up authentication (if username and password are provided)
    auth = HTTPBasicAuth(user, password) if password else None

    # Debug prints
    print(f"HDFS Host: {hdfs_host}")
    print(f"HDFS Port: {hdfs_port}")
    print(f"User: {user}")
    print(f"Extra: {extra}")

    # Step 1: Initiate the file upload (WebHDFS)
    init_url = f"{hdfs_host}:{hdfs_port}/webhdfs/v1/{hdfs_path}?op=CREATE&user.name={user}&overwrite=true"
    print("init_url:" + init_url)
    try:
        init_response = requests.put(init_url, allow_redirects=False, auth=auth)
        init_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise

    # Step 2: Follow the redirect URL to upload the data
    if init_response.status_code == 307:
        upload_url = init_response.headers['Location']
        with open(file_path, 'rb') as f:
            try:
                upload_response = requests.put(upload_url, data=f, auth=auth)
                upload_response.raise_for_status()
            except requests.RequestException as e:
                print(f"Upload failed: {e}")
                raise

        if upload_response.status_code == 201:
            print("File successfully uploaded to HDFS.")
        else:
            raise Exception(f"Failed to upload file: {upload_response.text}")
    else:
        raise Exception(f"Failed to initiate file upload: {init_response.text}")

def get_count_waiting_tasks(target_table_name,target_type):
    sql = f"""
    SELECT COUNT(id)
    FROM incremental_load_tasks
    WHERE table_name = '{target_table_name}'
    AND operation_type = '{target_type}'
    AND status IN('WAITING')
    """

    return fetch_scalar_result_int_config(sql)

def get_waitings_tasks(target_table_name,target_type):
    sql = f"""
    SELECT *
    FROM incremental_load_tasks
    WHERE table_name = '{target_table_name}'
    AND operation_type = '{target_type}'
    AND status IN('WAITING')
    ORDER BY created_at ASC
    """

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()

    df = pd.read_sql(sql, conn)

    return df
def update_status_tasks(id, status):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_tasks 
        SET status = %s
        WHERE id = %s
    """, (status,id))

    conn.commit()
    cur.close()
    conn.close()
def update_message_tasks(id, message):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_tasks 
        SET message = %s
        WHERE id = %s
    """, (message,id))

    conn.commit()
    cur.close()
    conn.close()