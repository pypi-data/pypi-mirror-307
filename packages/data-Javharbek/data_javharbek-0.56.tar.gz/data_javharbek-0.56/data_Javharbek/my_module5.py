# utils
from datetime import datetime

def check_time_raise_operator(**kwargs):

    # Получите контекст выполнения
    task_instance = kwargs.get('task_instance')  # Объект TaskInstance
    execution_date = kwargs.get('execution_date')  # Дата и время выполнения
    dag = kwargs.get('dag')  # Объект DAG
    dag_id = dag.dag_id if dag else None

    work_day_begin_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_begin_interval')
    work_day_end_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_end_interval')
    check_time_raise(work_day_begin_interval, work_day_end_interval)

def check_time_raise(work_day_begin_interval,work_day_end_interval):
    start_time = datetime.strptime(work_day_begin_interval, '%H:%M:%S').time()
    end_time = datetime.strptime(work_day_end_interval, '%H:%M:%S').time()
    now = datetime.now().time()
    if now < start_time or now > end_time:
        raise ValueError("Task is running outside the allowed time range")
    else:
        print("You work is correctly in the allowed time range between: " + str(work_day_begin_interval) + " - " + str(work_day_end_interval))

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def get_ids_list_from_df_str(cond_df, column_id='ID', separate=', '):
    ids = [row[column_id] for row in cond_df.select(column_id).collect()]
    ids_str = separate.join(map(str, ids))
    return ids_str


def get_ids_list_from_df(cond_df, column_id='ID', separate=', '):
    ids = [row[column_id] for row in cond_df.select(column_id).collect()]
    return ids

def batch_array(arr, batch_size):
    return [arr[i:i + batch_size] for i in range(0, len(arr), batch_size)]

def generate_sql_in_clause(arrays, column_name='ID'):
    # Формируем список SQL-частей
    sql_parts = []

    for sub_array in arrays:
        # Преобразуем каждый подмассив в строку вида (n1, n2, n3, ...)
        in_clause = f"{column_name} IN ({', '.join(map(str, sub_array))})"
        sql_parts.append(in_clause)

    # Объединяем части, добавляя OR между ними
    sql_statement = " OR ".join(sql_parts)
    return sql_statement