# increment transform plan
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import oracledb
from data_Javharbek import *
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

def get_count_transform_tasks_plan(script_id):
    sql = f"""
    SELECT COUNT(id)
    FROM incremental_transform_tasks
    WHERE script_id = '{script_id}'
    AND status IN ('WAITING', 'RUNNING','ERROR')
    """

    return fetch_scalar_result_int_config(sql)
def get_config_task_transform_plan(**kwargs):
    # Получите объект TaskInstance из kwargs
    ti = kwargs.get('task_instance')

    # Получите значение из XCom
    script_id = str(ti.xcom_pull(task_ids='push_param_task', key='script_id'))

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    query = """
        SELECT  id, 
                script_id,
                state_current_datetime,
                title, 
                operation_datetime,  
                table_name, 
                type,
                script_python_3,
                script_python_3_init
                FROM incremental_transform_plans WHERE script_id=%s
        """

    print("SQL: " + query)
    print("script_id: " + script_id)

    cur.execute(query, (script_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    # Сохранение значений в XCom
    if result:
        id = result[0]
        script_id = result[1]
        state_current_datetime = result[2]
        title = result[3]
        operation_datetime = result[4]
        table_name = result[5]
        type = result[6]
        script_python_3 = result[7]
        script_python_3_init = result[8]

        if state_current_datetime is not None:
            state_current_datetime = state_current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        if operation_datetime is not None:
            operation_datetime = operation_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')

        print("id: " + str(id))
        print("script_id: " + str(script_id))
        print("table_name: " + str(table_name))
        print("state_current_datetime: " + str(state_current_datetime))
        print("title: " + str(title))
        print("operation_datetime: " + str(operation_datetime))
        print("table_name: " + str(table_name))
        print("type: " + str(type))
        print("script_python_3: " + str(script_python_3))
        print("script_python_3_init: " + str(script_python_3_init))

        ti.xcom_push(key='id', value=id)
        ti.xcom_push(key='script_id', value=script_id)
        ti.xcom_push(key='state_current_datetime', value=state_current_datetime)
        ti.xcom_push(key='title', value=title)
        ti.xcom_push(key='operation_datetime', value=operation_datetime)
        ti.xcom_push(key='table_name', value=table_name)
        ti.xcom_push(key='type', value=type)
        ti.xcom_push(key='script_python_3', value=script_python_3)
        ti.xcom_push(key='script_python_3_init', value=script_python_3_init)
        print("load config success!!!")
    else:
        raise ValueError('Result is Empty')

    counts_waiting_task = get_count_transform_tasks_plan(script_id)
    print("counts_waiting_task: " + str(counts_waiting_task))
    if counts_waiting_task > 0 :
        raise ValueError("You have tasks on waiting or error")
def show_params_function_task_transform_plan(**kwargs):
    # Получите контекст выполнения
    task_instance = kwargs.get('task_instance')  # Объект TaskInstance
    execution_date = kwargs.get('execution_date')  # Дата и время выполнения
    dag = kwargs.get('dag')  # Объект DAG
    dag_id = dag.dag_id if dag else None

    # Получите значение из XCom
    id = task_instance.xcom_pull(task_ids='get_config_task', key='id')
    script_id = task_instance.xcom_pull(task_ids='get_config_task', key='script_id')
    state_current_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='state_current_datetime')
    title = task_instance.xcom_pull(task_ids='get_config_task', key='title')
    operation_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='operation_datetime')
    table_name = task_instance.xcom_pull(task_ids='get_config_task', key='table_name')
    type = task_instance.xcom_pull(task_ids='get_config_task', key='type')
    script_python_3 = task_instance.xcom_pull(task_ids='get_config_task', key='script_python_3')
    script_python_3_init = task_instance.xcom_pull(task_ids='get_config_task', key='script_python_3_init')

    print(f"Task instance: {task_instance.task_id}")
    print(f"Execution date: {execution_date}")
    print(f"DAG ID: {dag_id}")
    print(f"Pulled parameter value: id: {str(id)}")
    print(f"Pulled parameter value: script_id: {str(script_id)}")
    print(f"Pulled parameter value: state_current_datetime: {str(state_current_datetime)}")
    print(f"Pulled parameter value: title: {str(title)}")
    print(f"Pulled parameter value: operation_datetime: {str(operation_datetime)}")
    print(f"Pulled parameter value: table_name: {str(table_name)}")
    print(f"Pulled parameter value: type: {str(type)}")
    print(f"Pulled parameter value: script_python_3:")
    print(str(script_python_3))
    print(f"Pulled parameter value: script_python_3_init:")
    print(str(script_python_3_init))
def get_new_load_files_transform_plan(state_current_datetime, type_data, table_name):
    sql = f"""
    SELECT * FROM load_files 
    WHERE task_created_at > '{state_current_datetime}'::timestamp
    AND type_data = '{type_data}'
    AND table_name = '{table_name}'
    ORDER BY task_created_at ASC
    """

    pg_hook = PostgresHook(postgres_conn_id='pg-config')
    conn = pg_hook.get_conn()

    df = pd.read_sql(sql, conn)

    return df
def get_count_new_load_files_transform_plan(state_current_datetime, type_data, table_name):
    sql = f"""
    SELECT COUNT(*) FROM load_files 
    WHERE task_created_at > '{state_current_datetime}'::timestamp
    AND type_data = '{type_data}'
    AND table_name = '{table_name}'
    """

    return fetch_scalar_result_int_config(sql)
def get_count_not_transformed_tasks_transform_plan(script_id, transform_plan_id, table_name):
    sql = f"""
SELECT COUNT(*) FROM incremental_transform_tasks WHERE status IN ('NOT_TRANSFORMED','ERROR')
 AND script_id='{script_id}'
 AND transform_plan_id='{transform_plan_id}'
 AND table_name='{table_name}'
    """

    return fetch_scalar_result_int_config(sql)
def create_incremental_transform_tasks_plan(task_id, script_id, status, load_file_id, load_plan_id, task_created_at, transform_plan_id, table_name, script_python_3,script_python_3_init):
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
    INSERT INTO incremental_transform_tasks (task_id, script_id, status, load_file_id, load_plan_id, task_created_at,transform_plan_id,table_name, created_at,script_python_3,script_python_3_init)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Выполните SQL-запрос
    cur.execute(sql, (
    task_id, script_id, status, load_file_id, load_plan_id, task_created_at,transform_plan_id,table_name,created_at,script_python_3,script_python_3_init))

    # Зафиксируйте изменения
    conn.commit()

    # Закройте соединение
    cur.close()
    conn.close()
def create_plan_transform_plan(**kwargs):
    # Получите контекст выполнения
    task_instance = kwargs.get('task_instance')  # Объект TaskInstance
    execution_date = kwargs.get('execution_date')  # Дата и время выполнения
    dag = kwargs.get('dag')  # Объект DAG
    dag_id = dag.dag_id if dag else None

    # Получите значение из XCom
    id = task_instance.xcom_pull(task_ids='get_config_task', key='id')
    update_status_plans_transform(id,"WAITING")

    script_id = task_instance.xcom_pull(task_ids='get_config_task', key='script_id')
    state_current_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='state_current_datetime')
    title = task_instance.xcom_pull(task_ids='get_config_task', key='title')
    operation_datetime = task_instance.xcom_pull(task_ids='get_config_task', key='operation_datetime')
    table_name = task_instance.xcom_pull(task_ids='get_config_task', key='table_name')
    type = task_instance.xcom_pull(task_ids='get_config_task', key='type')
    script_python_3 = task_instance.xcom_pull(task_ids='get_config_task', key='script_python_3')
    script_python_3_init = task_instance.xcom_pull(task_ids='get_config_task', key='script_python_3_init')

    counts_new_files = get_count_new_load_files_transform_plan(state_current_datetime=state_current_datetime, type_data=type, table_name=table_name)
    count_not_transformed_tasks = get_count_not_transformed_tasks_transform_plan(script_id=script_id, transform_plan_id=id, table_name=table_name)

    if count_not_transformed_tasks > 0:
        print("YOU HAVE >> NOT_TRANSFORMED << TASK: " + str(count_not_transformed_tasks))
        update_status_plans_transform(id,'ERROR')
        update_message_plans_transform(id,"YOU HAVE >> NOT_TRANSFORMED << TASK: " + str(count_not_transformed_tasks))
        raise ValueError("YOU HAVE >> NOT_TRANSFORMED << TASK: " + str(count_not_transformed_tasks))
    if counts_new_files == 0:
        print("ALL COMPLETE: " + str(counts_new_files))
        update_status_plans_transform(id,'ALL_COMPLETE')
        return

    update_message_plans_transform(id,"---" + str(count_not_transformed_tasks))
    new_files_df = get_new_load_files_transform_plan(state_current_datetime=state_current_datetime, type_data=type, table_name=table_name)
    if new_files_df.empty:
        print("ALL COMPLETE: " + str(counts_new_files))
        update_status_plans_transform(id,'ALL_COMPLETE')
        return
    load_file_task_created_at = None
    update_status_plans_transform(id,"CREATING_TASK")
    for index, row in new_files_df.iterrows():
        try:
            print("new_files_df_item: ")
            print(f"Row {index} data:")
            print(row)
            load_file_id = row['id']
            load_file_filename = row['filename']
            load_file_filepath = row['filepath']
            load_file_created_at = row['created_at']
            load_file_table_name = row['table_name']
            load_file_storage_type = row['storage_type']
            load_file_storage_name = row['storage_name']
            load_file_bucket = row['bucket']
            load_file_file_type = row['file_type']
            load_file_counts_rows = row['counts_rows']
            load_file_min_id = row['min_id']
            load_file_max_id = row['max_id']
            load_file_type_data = row['type_data']
            load_file_min_datetime = row['min_datetime']
            load_file_max_datetime = row['max_datetime']
            load_file_plan_id = row['plan_id']
            load_file_task_id = row['task_id']
            load_file_task_created_at = row['task_created_at']
            print("ID: " + str(load_file_id))
            create_incremental_transform_tasks_plan(load_file_task_id, script_id, 'NOT_TRANSFORMED', load_file_id, load_file_plan_id, load_file_task_created_at, id, table_name, script_python_3,script_python_3_init)
            print("SUCCESS CREATED TRANSFORM TASK")
        except Exception as e:
            update_status_plans_transform(id, 'ERROR')
            # Capture the traceback as a string
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            update_message_plans_transform(id, str(tb_str))
            print("ERROR: " + str(tb_str))
            raise ValueError("Error on Execute Task")
    update_status_plans_transform(id,"PLAN_CREATED_ON_TRANSFORM")
    print("PLAN_CREATED_ON_TRANSFORM")
    if load_file_task_created_at is not None:
        update_state_current_datetime_transform_plan(id, load_file_task_created_at)
def update_status_plans_transform(id, status):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_transform_plans 
        SET status = %s, operation_datetime=%s
        WHERE id = %s
    """, (status,now,id))

    conn.commit()
    cur.close()
    conn.close()
def update_message_plans_transform(id, message):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_transform_plans 
        SET message = %s, operation_datetime=%s
        WHERE id = %s
    """, (message,now,id))

    conn.commit()
    cur.close()
    conn.close()
def update_state_current_datetime_transform_plan(id, state_current_datetime):
    # Получаем текущее время
    now = datetime.now()

    pg_hook = PostgresHook(postgres_conn_id='pg-config', schema='postgres')
    conn = pg_hook.get_conn()
    cur = conn.cursor()

    # Обновляем max_id и устанавливаем текущую дату и время
    cur.execute("""
        UPDATE incremental_transform_plans 
        SET state_current_datetime = %s, operation_datetime=%s
        WHERE id = %s
    """, (state_current_datetime,now,id))

    conn.commit()
    cur.close()
    conn.close()