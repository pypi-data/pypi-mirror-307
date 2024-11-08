# increment transform task
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import oracledb
from airflow.hooks.base_hook import BaseHook
from data_Javharbek import *
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
from requests.auth import HTTPBasicAuth
from airflow.hooks.base_hook import BaseHook
from .my_module2 import *
from .my_module5 import *
import chardet

def get_one_from_table_by_column_equal_config(table_name, id, column='id'):
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
def get_max_thread_counts_transform_task(plan_id):
    sql = f"""
SELECT max_thread_counts FROM incremental_transform_plans WHERE id = '{plan_id}'
"""
    return fetch_scalar_result_int_config(sql)

def get_count_waiting_tasks_transform_task(plan_id):
    sql = f"""
    SELECT COUNT(id)
    FROM incremental_transform_tasks
    WHERE transform_plan_id = '{plan_id}'
    AND status IN('NOT_TRANSFORMED')
    """

    return fetch_scalar_result_int_config(sql)
def get_waitings_tasks_transform_task(plan_id):
    sql = f"""
    SELECT *
    FROM incremental_transform_tasks
    WHERE transform_plan_id = '{plan_id}'
    AND status IN('NOT_TRANSFORMED')
    ORDER BY task_created_at ASC
    """

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()

    df = pd.read_sql(sql, conn)

    return df
def update_status_tasks_transform_task(id, status):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_transform_tasks 
        SET status = %s
        WHERE id = %s
    """, (status,id))

    conn.commit()
    cur.close()
    conn.close()
def update_message_tasks_transform_task(id, message):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_transform_tasks 
        SET message = %s
        WHERE id = %s
    """, (message,id))

    conn.commit()
    cur.close()
    conn.close()


def convert_to_utf8(string):
    # Преобразование строки в байты
    byte_string = string.encode() if isinstance(string, str) else string

    # Определение кодировки
    result = chardet.detect(byte_string)
    encoding = result['encoding']

    # Если кодировка не UTF-8, преобразуем в UTF-8
    if encoding.lower() != 'utf-8':
        decoded_string = byte_string.decode(encoding)
        utf8_string = decoded_string.encode('utf-8')
        return utf8_string.decode('utf-8')
    return byte_string.decode('utf-8')
def execute_task_one_transform_task(transform_task, transform_plan, index):

    load_file_id = transform_task['load_file_id']
    load_task_id = transform_task['task_id']
    load_plan_id = transform_task['load_plan_id']
    id = transform_task['id']

    load_file = get_one_from_table_by_column_equal_config('load_files', load_file_id, 'id')
    load_task = get_one_from_table_by_column_equal_config('incremental_load_tasks', load_task_id, 'id')
    load_plan = get_one_from_table_by_column_equal_config('incremental_load_plans', load_plan_id, 'id')
    script_python_3 = transform_task['script_python_3']
    script_python_3_init = transform_task['script_python_3_init']

    print("transform_task: ")
    print(transform_task)
    print("transform_plan: ")
    print(transform_plan)
    print("index: " + str(index))
    print("id: " + str(id))
    print("load_file: ")
    print(load_file)
    print("load_task: ")
    print(load_task)
    print("load_plan: ")
    print(load_plan)
    print("script_python_3: ")
    print(str(script_python_3))

    try:
        update_status_tasks_transform_task(id, 'NOT_TRANSFORMED')
        update_message_tasks_transform_task(id, "---")
        print("start executing")
        print("script_python_3_init")
        print(script_python_3_init)
        if script_python_3_init is not None :
            print("Start Script Init")
            exec(script_python_3_init)
            print("End Script Init")
        print("script_python_3")

        print(script_python_3)
        if script_python_3 is not None :
            print("Start Script")
            exec(script_python_3)
            print("End Script")
        print("end executing")
        update_status_tasks_transform_task(id, 'COMPLETE')
    except Exception as e:
        update_status_tasks_transform_task(id, 'ERROR')
        # Capture the traceback as a string
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        update_message_tasks_transform_task(id, str(tb_str))
        print("ERROR: " + str(tb_str))
        raise ValueError("Error on Execute Task")
def create_execute_tasks_transform(script_id):

    print("create_execute_tasks: start")
    plan = get_one_from_table_by_column_equal_config('incremental_transform_plans', script_id, 'script_id')
    plan_id = plan['id']

    counts = get_count_waiting_tasks_transform_task(plan_id)
    if counts == 0:
        print("create_execute_tasks_transform: waiting count is zero")
        return
    df = get_waitings_tasks_transform_task(plan_id)
    if df.empty:
        print("create_execute_tasks_transform: waiting data is empty")
        return
    operators = []

    print("plan_id: " + str(plan_id))
    max_thread_counts = get_max_thread_counts_transform_task(plan_id)
    print("max_thread_counts: " + str(max_thread_counts))

    for index, row in df.iterrows():
        print("Begin")
        if(max_thread_counts < (index + 1)):
            print("Break")
            break
        print("Start")
        print(f"Row {index} data:")

        make_query_migrate_to_storage_task = PythonOperator(
            task_id=f'execute_task_one_{index}',
            python_callable=execute_task_one_transform_task,
            op_args=[row,plan,index]
        )
        operators.append(make_query_migrate_to_storage_task)
        print("assign task")

    print("create_execute_tasks: end")
    return operators