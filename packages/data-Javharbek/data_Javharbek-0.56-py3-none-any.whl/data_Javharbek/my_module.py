# increment load plan
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
from .my_module5 import *

def greet(name):
    return f"Hello, {name}!"

def get_config_task(**kwargs):
    # Получите объект TaskInstance из kwargs
    ti = kwargs.get('task_instance')

    # Получите значение из XCom
    target_table_name = str(ti.xcom_pull(task_ids='push_param_task', key='target_table_name'))
    target_type = str(ti.xcom_pull(task_ids='push_param_task', key='target_type'))

    if get_count_waiting_tasks(target_table_name, target_type) > 0:
        raise ValueError("You have tasks on waiting")

    update_status(target_table_name, target_type,'WAITING')

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    query = """
        SELECT  id, 
                max_thread_counts,
                table_name,
                state_current_id, 
                state_current_datetime, 
                operation_type, 
                column_id, 
                columns_watch_datetimes, 
                type_id, 
                column_sort,
                sort_type,
                pagination_offset,
                paginaton_limit,
                pagination_total_elements,
                status,
                driver_db_name,
                operation_datetime,
                connection_id,
                work_day_begin_interval,
                work_day_end_interval,
                select_fields
                FROM incremental_load_plans WHERE table_name=%s AND operation_type=%s AND status IN ('WAITING','ACTIVE','EMPTY_TASK')
        """

    print("SQL: " + query)
    print("target_table_name: " + target_table_name)
    print("target_type: " + target_type)

    cur.execute(query, (target_table_name, target_type))
    result = cur.fetchone()
    cur.close()
    conn.close()

    # Сохранение значений в XCom
    if result:
        id = result[0]
        max_thread_counts = result[1]
        table_name = result[2]
        state_current_id = result[3]
        state_current_datetime = result[4]
        operation_type = result[5]
        column_id = result[6]
        columns_watch_datetimes = result[7]
        type_id = result[8]
        column_sort = result[9]
        sort_type = result[10]
        pagination_offset = result[11]
        pagination_limit = result[12]
        pagination_total_elements = result[13]
        status = result[14]
        driver_db_name = result[15]
        operation_datetime = result[16]
        connection_id = result[17]
        work_day_begin_interval = result[18]
        work_day_end_interval = result[19]
        select_fields = result[20]

        check_time_raise(work_day_begin_interval, work_day_end_interval)

        update_status(target_table_name, target_type, 'CREATE_TASK')
        status = 'CREATE_TASK'

        if state_current_datetime is not None:
            state_current_datetime = state_current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        if operation_datetime is not None:
            operation_datetime = operation_datetime.strftime('%Y-%m-%d %H:%M:%S')
        if state_current_id is not None:
            state_current_id = int(state_current_id)

        print("id: " + str(id))
        print("max_thread_counts: " + str(max_thread_counts))
        print("table_name: " + str(table_name))
        print("state_current_id: " + str(state_current_id))
        print("state_current_datetime: " + str(state_current_datetime))
        print("operation_type: " + str(operation_type))
        print("column_id: " + str(column_id))
        print("columns_watch_datetimes: " + str(columns_watch_datetimes))
        print("type_id: " + str(type_id))
        print("column_sort: " + str(column_sort))
        print("sort_type: " + str(sort_type))
        print("pagination_offset: " + str(pagination_offset))
        print("pagination_limit: " + str(pagination_limit))
        print("pagination_total_elements: " + str(pagination_total_elements))
        print("status: " + str(status))
        print("driver_db_name: " + str(driver_db_name))
        print("operation_datetime: " + str(operation_datetime))
        print("connection_id: " + str(connection_id))
        print("work_day_begin_interval: " + str(work_day_begin_interval))
        print("work_day_end_interval: " + str(work_day_end_interval))
        print("select_fields: " + str(select_fields))

        ti.xcom_push(key='id', value=id)
        ti.xcom_push(key='max_thread_counts', value=max_thread_counts)
        ti.xcom_push(key='table_name', value=table_name)
        ti.xcom_push(key='state_current_id', value=state_current_id)
        ti.xcom_push(key='state_current_datetime', value=state_current_datetime)
        ti.xcom_push(key='operation_type', value=operation_type)
        ti.xcom_push(key='column_id', value=column_id)
        ti.xcom_push(key='columns_watch_datetimes', value=columns_watch_datetimes)
        ti.xcom_push(key='type_id', value=type_id)
        ti.xcom_push(key='column_sort', value=column_sort)
        ti.xcom_push(key='sort_type', value=sort_type)
        ti.xcom_push(key='pagination_offset', value=pagination_offset)
        ti.xcom_push(key='pagination_limit', value=pagination_limit)
        ti.xcom_push(key='pagination_total_elements', value=pagination_total_elements)
        ti.xcom_push(key='status', value=status)
        ti.xcom_push(key='driver_db_name', value=driver_db_name)
        ti.xcom_push(key='operation_datetime', value=operation_datetime)
        ti.xcom_push(key='connection_id', value=connection_id)
        ti.xcom_push(key='work_day_begin_interval', value=work_day_begin_interval)
        ti.xcom_push(key='work_day_end_interval', value=work_day_end_interval)
        ti.xcom_push(key='select_fields', value=select_fields)

        print("load config success!!!")
    else:
        raise ValueError('Result is Empty')


def show_params_function_task(**kwargs):
    # Получите контекст выполнения
    task_instance = kwargs.get('task_instance')  # Объект TaskInstance
    execution_date = kwargs.get('execution_date')  # Дата и время выполнения
    dag = kwargs.get('dag')  # Объект DAG
    dag_id = dag.dag_id if dag else None

    # Получите значение из XCom
    id = task_instance.xcom_pull(task_ids='get_config_task', key='id')
    max_thread_counts = task_instance.xcom_pull(task_ids='get_config_task', key='max_thread_counts')
    table_name = task_instance.xcom_pull(task_ids='get_config_task', key='table_name')
    state_current_id = task_instance.xcom_pull(task_ids='get_config_task', key='state_current_id')
    state_current_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='state_current_datetime')
    operation_type = task_instance.xcom_pull(task_ids='get_config_task', key='operation_type')
    column_id = task_instance.xcom_pull(task_ids='get_config_task', key='column_id')
    columns_watch_datetimes = task_instance.xcom_pull(task_ids='get_config_task', key='columns_watch_datetimes')
    type_id = task_instance.xcom_pull(task_ids='get_config_task', key='type_id')
    column_sort = task_instance.xcom_pull(task_ids='get_config_task', key='column_sort')
    sort_type = task_instance.xcom_pull(task_ids='get_config_task', key='sort_type')
    pagination_offset = task_instance.xcom_pull(task_ids='get_config_task', key='pagination_offset')
    pagination_limit = task_instance.xcom_pull(task_ids='get_config_task', key='pagination_limit')
    pagination_total_elements = task_instance.xcom_pull(task_ids='get_config_task', key='pagination_total_elements')
    status = task_instance.xcom_pull(task_ids='get_config_task', key='status')
    driver_db_name = task_instance.xcom_pull(task_ids='get_config_task', key='driver_db_name')
    operation_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='operation_datetime')
    connection_id = task_instance.xcom_pull(task_ids='get_config_task', key='connection_id')
    work_day_begin_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_begin_interval')
    work_day_end_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_end_interval')
    select_fields = task_instance.xcom_pull(task_ids='get_config_task', key='select_fields')

    print(f"Task instance: {task_instance.task_id}")
    print(f"Execution date: {execution_date}")
    print(f"DAG ID: {dag_id}")
    print(f"Pulled parameter value: id: {str(id)}")
    print(f"Pulled parameter value: max_thread_counts: {str(max_thread_counts)}")
    print(f"Pulled parameter value: table_name: {str(table_name)}")
    print(f"Pulled parameter value: state_current_id: {str(state_current_id)}")
    print(f"Pulled parameter value: state_current_datetime: {str(state_current_datetime)}")
    print(f"Pulled parameter value: operation_type: {str(operation_type)}")
    print(f"Pulled parameter value: column_id: {str(column_id)}")
    print(f"Pulled parameter value: columns_watch_datetimes: {str(columns_watch_datetimes)}")
    print(f"Pulled parameter value: type_id: {str(type_id)}")
    print(f"Pulled parameter value: column_sort: {str(column_sort)}")
    print(f"Pulled parameter value: sort_type: {str(sort_type)}")
    print(f"Pulled parameter value: pagination_offset: {str(pagination_offset)}")
    print(f"Pulled parameter value: pagination_limit: {str(pagination_limit)}")
    print(f"Pulled parameter value: pagination_total_elements: {str(pagination_total_elements)}")
    print(f"Pulled parameter value: status: {str(status)}")
    print(f"Pulled parameter value: driver_db_name: {str(driver_db_name)}")
    print(f"Pulled parameter value: operation_datetime: {str(operation_datetime)}")
    print(f"Pulled parameter value: connection_id: {str(connection_id)}")
    print(f"Pulled parameter value: work_day_begin_interval: {str(work_day_begin_interval)}")
    print(f"Pulled parameter value: work_day_end_interval: {str(work_day_end_interval)}")
    print(f"Pulled parameter value: select_fields: {str(select_fields)}")


def query_task(**kwargs):
    # Получите контекст выполнения
    task_instance = kwargs.get('task_instance')  # Объект TaskInstance
    execution_date = kwargs.get('execution_date')  # Дата и время выполнения
    dag = kwargs.get('dag')  # Объект DAG
    dag_id = dag.dag_id if dag else None

    id = task_instance.xcom_pull(task_ids='get_config_task', key='id')
    max_thread_counts = task_instance.xcom_pull(task_ids='get_config_task', key='max_thread_counts')
    table_name = task_instance.xcom_pull(task_ids='get_config_task', key='table_name')
    state_current_id = task_instance.xcom_pull(task_ids='get_config_task', key='state_current_id')
    state_current_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='state_current_datetime')
    operation_type = task_instance.xcom_pull(task_ids='get_config_task', key='operation_type')
    column_id = task_instance.xcom_pull(task_ids='get_config_task', key='column_id')
    columns_watch_datetimes = task_instance.xcom_pull(task_ids='get_config_task', key='columns_watch_datetimes')
    type_id = task_instance.xcom_pull(task_ids='get_config_task', key='type_id')
    column_sort = task_instance.xcom_pull(task_ids='get_config_task', key='column_sort')
    sort_type = task_instance.xcom_pull(task_ids='get_config_task', key='sort_type')
    pagination_offset = task_instance.xcom_pull(task_ids='get_config_task', key='pagination_offset')
    pagination_limit = task_instance.xcom_pull(task_ids='get_config_task', key='pagination_limit')
    pagination_total_elements = task_instance.xcom_pull(task_ids='get_config_task', key='pagination_total_elements')
    status = task_instance.xcom_pull(task_ids='get_config_task', key='status')
    driver_db_name = task_instance.xcom_pull(task_ids='get_config_task', key='driver_db_name')
    operation_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='operation_datetime')
    connection_id = task_instance.xcom_pull(task_ids='get_config_task', key='connection_id')
    work_day_begin_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_begin_interval')
    work_day_end_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_end_interval')
    select_fields = task_instance.xcom_pull(task_ids='get_config_task', key='select_fields')
    target_table_name = str(task_instance.xcom_pull(task_ids='push_param_task', key='target_table_name'))
    target_type = str(task_instance.xcom_pull(task_ids='push_param_task', key='target_type'))

    query_result_sql = get_query(target_table_name, target_type, id, max_thread_counts, state_current_id,
                                 state_current_datetime, operation_type, column_id, columns_watch_datetimes, type_id,
                                 column_sort, sort_type, pagination_offset, pagination_limit, pagination_total_elements,
                                 status, driver_db_name, operation_datetime,select_fields)
    query_count = query_result_sql['query_count']
    query_max_id_all = query_result_sql['query_max_id_all']
    print("query_count_sql:" + query_count)
    print("query_max_id_all:" + query_max_id_all)

    count_result = fetch_scalar_result_int_source(query_count,connection_id,driver_db_name)

    print("Count result: " + str(count_result))

    pagination_total_elements = count_result
    update_pagination_total_elements(target_table_name, target_type, pagination_total_elements)

    offset_count = 0

    if count_result > pagination_offset:
        offset_count = int(count_result - pagination_offset)

    if offset_count == 0:
        update_status(target_table_name, target_type, 'EMPTY_TASK')
        print("Full Scan: " + str(count_result) + " - " + str(pagination_offset))
        return

    all_tasks = math.ceil(offset_count / int(pagination_limit))

    print('all tasks: ' + str(all_tasks))

    for task_number in range(0, all_tasks):
        try:
            print("task_number: " + str(task_number))
            if task_number > 0:
                pagination_offset = pagination_offset + pagination_limit
            print("pagination_offset: " + str(pagination_offset))
            print("pagination_limit: " + str(pagination_limit))
            print("pagination_total_elements: " + str(pagination_total_elements))
            query_result_sql = get_query(target_table_name, target_type, id, max_thread_counts, state_current_id,
                                         state_current_datetime, operation_type, column_id, columns_watch_datetimes,
                                         type_id,
                                         column_sort, sort_type, pagination_offset, pagination_limit,
                                         pagination_total_elements,
                                         status, driver_db_name, operation_datetime,select_fields)
            query = query_result_sql['query']
            print("create_load_task_record  start :" + str(task_number))
            create_load_task_record(id, pagination_offset, pagination_limit, dag_id, pagination_total_elements,
                                    columns_watch_datetimes, column_id, type_id, column_sort, sort_type, driver_db_name,
                                    query, query_count,state_current_id,state_current_datetime,operation_type,target_table_name,connection_id,select_fields)
            update_pagination_offset(target_table_name, target_type, pagination_offset)
            print("create_load_task_record  end :" + str(task_number))
            print("Created Success!!!")
        except Exception as e:
            update_status(target_table_name, target_type, 'ERROR')
            # Capture the traceback as a string
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            update_message(id, str(tb_str))
            print("error:  " + str(tb_str))
            return
    if type_id == 'INC':
        query_max_id_all_result = fetch_scalar_result_int_source(query_max_id_all,connection_id,driver_db_name)
        update_state_current_id_plan(target_table_name, target_type, query_max_id_all_result)
    if type_id == 'GUID':
        update_state_current_datetime_plan(target_table_name, target_type)
    update_pagination_offset(target_table_name, target_type, 0)
    update_status(target_table_name, target_type, 'ON_EXECUTE')


def fetch_scalar_result_int_source(query_sql,connection_id,driver_name):
    hook = None

    if driver_name == 'ORACLE':
        hook = OracleHook(oracle_conn_id=connection_id)
    elif driver_name == 'POSTGRES':
        hook = PostgresHook(postgres_conn_id=connection_id)
    else:
        raise ValueError('driver_name must be ORACLE or POSTGRES')

    conn = hook.get_conn()

    cur = conn.cursor()
    cur.execute(query_sql)
    one = cur.fetchone()

    # Получаем количество записей
    result = one[0] if one else 0
    cur.close()

    return result
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

def create_load_task_record(plan_id, pagination_offset, pagination_limit, log_id, pagination_total_elements,
                            columns_watch_datetimes, column_id, type_id, column_sort, sort_type, driver_db_name,
                            sql_query_raw, sql_count_raw,state_current_id,state_current_datetime,operation_type,table_name,connection_id,select_fields):

    # Получите соединение с PostgreSQL из Airflow
    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Получите текущее время
    created_at = datetime.utcnow()

    # SQL-запрос для вставки данных
    sql = """
    INSERT INTO incremental_load_tasks (plan_id, pagination_offset, pagination_limit, status, log_id, created_at, pagination_total_elements,columns_watch_datetimes,column_id,type_id,column_sort,sort_type,driver_db_name,sql_query_raw,sql_count_raw,state_current_id,state_current_datetime,operation_type,table_name,connection_id,select_fields)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Выполните SQL-запрос
    cur.execute(sql, (
        plan_id, pagination_offset, pagination_limit, 'WAITING', log_id, created_at, pagination_total_elements,
        columns_watch_datetimes, column_id, type_id, column_sort, sort_type, driver_db_name, sql_query_raw,
        sql_count_raw,state_current_id,state_current_datetime,operation_type,table_name,connection_id,select_fields))

    # Зафиксируйте изменения
    conn.commit()

    # Закройте соединение
    cur.close()
    conn.close()


def update_pagination_total_elements(target_table_name, target_type, pagination_total_elements):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_plans 
        SET pagination_total_elements = %s , operation_datetime = %s
        WHERE table_name = %s AND operation_type=%s
    """, (pagination_total_elements, now, target_table_name, target_type))

    conn.commit()
    cur.close()
    conn.close()

def update_state_current_id_plan(target_table_name, target_type, state_current_id):
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_plans 
        SET state_current_id = %s , state_current_datetime = %s , operation_datetime = %s
        WHERE table_name = %s AND operation_type=%s
    """, (state_current_id, now, now, target_table_name, target_type))

    conn.commit()
    cur.close()
    conn.close()


def update_state_current_datetime_plan(target_table_name, target_type):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_plans 
        SET state_current_datetime = %s, operation_datetime = %s 
        WHERE table_name = %s AND operation_type=%s
    """, (now, now, target_table_name, target_type))

    conn.commit()
    cur.close()
    conn.close()


def update_pagination_offset(target_table_name, target_type, pagination_offset):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_plans 
        SET pagination_total_elements = %s, operation_datetime = %s
        WHERE table_name = %s AND operation_type=%s
    """, (pagination_offset, now, target_table_name, target_type))

    conn.commit()
    cur.close()
    conn.close()

def update_status(target_table_name, target_type, status):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_plans 
        SET status = %s, operation_datetime = %s
        WHERE table_name = %s AND operation_type=%s
    """, (status, now, target_table_name, target_type))

    conn.commit()
    cur.close()
    conn.close()

def update_message(id, message):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_load_plans 
        SET message = %s, operation_datetime = %s
        WHERE id = %s
    """, (message, now, id))

    conn.commit()
    cur.close()
    conn.close()

def get_query(target_table_name, target_type, id, max_thread_counts, state_current_id, state_current_datetime,
              operation_type, column_id, columns_watch_datetimes, type_id, column_sort, sort_type, pagination_offset,
              pagination_limit, pagination_total_elements, status, driver_db_name, operation_datetime,select_fields):
    if driver_db_name == 'POSTGRES':
        print("get_query_postgres")
        return get_query_postgres(target_table_name, target_type, id, max_thread_counts, state_current_id, state_current_datetime,
              operation_type, column_id, columns_watch_datetimes, type_id, column_sort, sort_type, pagination_offset,
              pagination_limit, pagination_total_elements, status, driver_db_name, operation_datetime,select_fields)
    elif driver_db_name == 'ORACLE':
        print("get_query_oracle")
        return get_query_oracle(target_table_name, target_type, id, max_thread_counts, state_current_id, state_current_datetime,
              operation_type, column_id, columns_watch_datetimes, type_id, column_sort, sort_type, pagination_offset,
              pagination_limit, pagination_total_elements, status, driver_db_name, operation_datetime,select_fields)
    else:
        raise ValueError("get_query only POSTGRES OR ORACLE")

def get_query_postgres(target_table_name, target_type, id, max_thread_counts, state_current_id, state_current_datetime,
              operation_type, column_id, columns_watch_datetimes, type_id, column_sort, sort_type, pagination_offset,
              pagination_limit, pagination_total_elements, status, driver_db_name, operation_datetime,select_fields):
    watch_datetimes_cols_query = ''

    # Проверяем, не является ли строка пустой
    if (
            columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none' and
            state_current_datetime is not None and state_current_datetime.strip() and state_current_datetime.strip().lower() != 'none'
    ):
        # Строка не пустая
        print("watch_datetimes_cols не пустой:", columns_watch_datetimes)
        # Разделяем строку по запятой
        watch_datetimes_cols_list = columns_watch_datetimes.split(',')
        for watch_datetimes_col in watch_datetimes_cols_list:
            print("watch_datetimes_col: " + watch_datetimes_col)
            watch_datetimes_cols_query = f""" 

                    {watch_datetimes_cols_query}
                    OR ({watch_datetimes_col}::timestamp > '{state_current_datetime}'::timestamp)

                """


    else:
        # Строка пустая
        print("columns_watch_datetimes пустой или state_current_datetime пустой")

    query_pagination_post = f"""
        ORDER BY {column_sort} {sort_type} LIMIT {pagination_limit} OFFSET {pagination_offset}
    """

    # SQL-запрос с фильтрацией по инкрементальному id query
    query = f"""
    SELECT {select_fields} FROM {target_table_name} WHERE {column_id} > {state_current_id} {watch_datetimes_cols_query} {query_pagination_post}
    """

    if type_id == 'GUID':
        if columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none':
            query = f"""
        SELECT {select_fields} FROM {target_table_name} WHERE 1=1 AND (1=2 {watch_datetimes_cols_query}) {query_pagination_post}
        """
        else:
            query = f"""
        SELECT {select_fields} FROM {target_table_name} WHERE 1=1 {query_pagination_post}
        """

    # SQL-запрос с фильтрацией по инкрементальному id query_count
    query_count = f"""
    SELECT COUNT({column_id}) FROM {target_table_name} WHERE {column_id} > {state_current_id} {watch_datetimes_cols_query}
    """

    if type_id == 'GUID':
        if columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none':
            query_count = f"""
        SELECT COUNT({column_id}) FROM {target_table_name} WHERE 1=1 AND (1=2 {watch_datetimes_cols_query})
        """
        else:
            query_count = f"""
        SELECT COUNT({column_id}) FROM {target_table_name} WHERE 1=1
        """



    # SQL-запрос с фильтрацией по инкрементальному id query_count
    query_max_id_all = f"""
    SELECT MAX({column_id}) FROM {target_table_name} WHERE {column_id} > {state_current_id} {watch_datetimes_cols_query}
    """

    if type_id == 'GUID':
        if columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none':
            query_max_id_all = f"""
        SELECT MAX({column_id}) FROM {target_table_name} WHERE 1=1 AND (1=2 {watch_datetimes_cols_query})
        """
        else:
            query_max_id_all = f"""
        SELECT MAX({column_id}) FROM {target_table_name} WHERE 1=1
        """

    print("query: " + query)
    print("query_count: " + query_count)
    print("query_max_id_all: " + query_max_id_all)

    return {
        'query': query,
        'query_count': query_count,
        'query_max_id_all': query_max_id_all
    }


def get_query_oracle(target_table_name, target_type, id, max_thread_counts, state_current_id, state_current_datetime,
              operation_type, column_id, columns_watch_datetimes, type_id, column_sort, sort_type, pagination_offset,
              pagination_limit, pagination_total_elements, status, driver_db_name, operation_datetime,select_fields):
    watch_datetimes_cols_query = ''
    query_order_by = f"""
 ORDER BY {column_sort} {sort_type} 
"""

    # Проверяем, не является ли строка пустой
    if (
            columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none' and
            state_current_datetime is not None and state_current_datetime.strip() and state_current_datetime.strip().lower() != 'none'
    ):
        # Строка не пустая
        print("watch_datetimes_cols не пустой:", columns_watch_datetimes)
        # Разделяем строку по запятой
        watch_datetimes_cols_list = columns_watch_datetimes.split(',')
        for watch_datetimes_col in watch_datetimes_cols_list:
            print("watch_datetimes_col: " + watch_datetimes_col)
            watch_datetimes_cols_query = f""" 

                    {watch_datetimes_cols_query}
                    OR (CAST({watch_datetimes_col} AS TIMESTAMP) > TO_TIMESTAMP('{state_current_datetime}', 'YYYY-MM-DD HH24:MI:SS'))

                """


    else:
        # Строка пустая
        print("columns_watch_datetimes пустой или state_current_datetime пустой")

    query_pagination_before = f"""
    SELECT {select_fields}
FROM (
    SELECT a.*, ROWNUM AS rnum
    FROM (
"""
    query_pagination_after = f"""
    ) a
    WHERE ROWNUM <= {pagination_offset + pagination_limit}
)
WHERE rnum > {pagination_offset}
"""
    # SQL-запрос с фильтрацией по инкрементальному id query
    query = f"""
    SELECT {select_fields} FROM {target_table_name} WHERE {column_id} > {state_current_id} {watch_datetimes_cols_query}
    """

    if type_id == 'GUID':
        if columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none':
            query = f"""
        SELECT {select_fields} FROM {target_table_name} WHERE 1=1 AND (1=2 {watch_datetimes_cols_query})
        """
        else:
            query = f"""
        SELECT {select_fields} FROM {target_table_name} WHERE 1=1
        """

    query  = f"""
    {query_pagination_before}
    {query} {query_order_by}
    {query_pagination_after}
"""

    # SQL-запрос с фильтрацией по инкрементальному id query_count
    query_count = f"""
    SELECT COUNT({column_id}) FROM {target_table_name} WHERE {column_id} > {state_current_id} {watch_datetimes_cols_query}
    """

    if type_id == 'GUID':
        if columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none':
            query_count = f"""
        SELECT COUNT({column_id}) FROM {target_table_name} WHERE 1=1 AND (1=2 {watch_datetimes_cols_query})
        """
        else:
            query_count = f"""
        SELECT COUNT({column_id}) FROM {target_table_name} WHERE 1=1
        """



    # SQL-запрос с фильтрацией по инкрементальному id query_count
    query_max_id_all = f"""
    SELECT MAX({column_id}) FROM {target_table_name} WHERE {column_id} > {state_current_id} {watch_datetimes_cols_query}
    """

    if type_id == 'GUID':
        if columns_watch_datetimes is not None and columns_watch_datetimes.strip() and columns_watch_datetimes.strip().lower() != 'none':
            query_max_id_all = f"""
        SELECT MAX({column_id}) FROM {target_table_name} WHERE 1=1 AND (1=2 {watch_datetimes_cols_query})
        """
        else:
            query_max_id_all = f"""
        SELECT MAX({column_id}) FROM {target_table_name} WHERE 1=1
        """

    print("query: " + query)
    print("query_count: " + query_count)
    print("query_max_id_all: " + query_max_id_all)

    return {
        'query': query,
        'query_count': query_count,
        'query_max_id_all': query_max_id_all
    }

def get_count_waiting_tasks(target_table_name,target_type):
    sql = f"""
    SELECT COUNT(id)
    FROM incremental_load_tasks
    WHERE table_name = '{target_table_name}'
    AND operation_type = '{target_type}'
    AND status IN('WAITING','EXECUTING')
    """

    return fetch_scalar_result_int_config(sql)