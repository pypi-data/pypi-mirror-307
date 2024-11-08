# data_Javharbek

A description of your package.
python3 setup.py sdist bdist_wheel
twine upload dist/*

```sql
-- auto-generated definition
create table incremental_load_plans
(
    id                        varchar(255) default uuid_generate_v4()            not null,
    max_thread_counts         integer      default 1                             not null,
    table_name                varchar(255)                                       not null,
    state_current_id          bigint,
    state_current_datetime    timestamp,
    operation_type            varchar(255) default 'NEW'::character varying      not null,
    column_id                 varchar(255),
    columns_watch_datetimes   text,
    type_id                   varchar(255),
    column_sort               varchar(255),
    sort_type                 varchar(255) default 'ASC'::character varying      not null,
    pagination_offset         bigint,
    paginaton_limit           bigint,
    pagination_total_elements bigint,
    status                    varchar(255) default 'WAITING'::character varying  not null,
    driver_db_name            varchar(255) default 'POSTGRES'::character varying not null,
    operation_datetime        timestamp,
    connection_id             varchar(255),
    message                   text
);

comment on column incremental_load_plans.columns_watch_datetimes is 'with_comma_for_multi';

comment on column incremental_load_plans.type_id is 'inc or guid';

comment on column incremental_load_plans.status is 'WAIT,ACTIVE,ERROR';

comment on column incremental_load_plans.driver_db_name is 'POSTGRES,ORACLE';

alter table incremental_load_plans
    owner to postgres;
```


```sql

-- auto-generated definition
create table incremental_load_tasks
(
    id                        varchar(255) default uuid_generate_v4()           not null,
    plan_id                   varchar(255)                                      not null,
    pagination_offset         bigint,
    pagination_limit          bigint,
    status                    varchar(255) default 'WAITING'::character varying not null,
    started_at                timestamp,
    end_at                    timestamp,
    log_id                    varchar(255),
    created_at                timestamp,
    pagination_total_elements bigint       default 0                            not null,
    state_current_id          bigint,
    state_current_datetime    timestamp,
    operation_type            varchar(255),
    columns_watch_datetimes   text,
    column_id                 varchar(255),
    type_id                   varchar(255),
    column_sort               varchar(255),
    sort_type                 varchar(255),
    driver_db_name            varchar(255),
    sql_query_raw             text,
    sql_count_raw             text,
    table_name                varchar(255),
    message                   text,
    connection_id             varchar(255)
);

comment on column incremental_load_tasks.status is 'WAITING,EXECUTING,COMPLETE,ERROR';

alter table incremental_load_tasks
    owner to postgres;

```

```sql
-- auto-generated definition
create table load_files
(
    id           uuid default uuid_generate_v4() not null
        primary key,
    filename     text                            not null,
    filepath     text                            not null,
    created_at   timestamp,
    table_name   varchar(255),
    storage_type varchar(255),
    storage_name varchar(255),
    bucket       varchar(255),
    file_type    varchar(255),
    counts_rows  bigint,
    min_id       bigint,
    max_id       bigint,
    type_data    varchar(255),
    min_datetime timestamp,
    max_datetime timestamp,
    plan_id      varchar(255),
    task_id      varchar(255)
);

alter table load_files
    owner to postgres;

```

```sql
-- auto-generated definition
create table storage_hosts
(
    connection_id      varchar(255)          not null
        constraint storage_hosts_pk
            primary key,
    type               varchar(255)          not null,
    in_rotation        boolean default false not null,
    extra              json,
    s3_key             text,
    s3_bucket_name     varchar(255),
    hdfs_endpoint_path varchar(255)
);

comment on column storage_hosts.type is 'MINIO,HDFS';

alter table storage_hosts
    owner to postgres;

```

Deprecated:
```sql
-- auto-generated definition
create table incremental_load_status
(
    table_name           varchar                                 not null
        primary key,
    max_id               bigint,
    updated_at           timestamp,
    operation_date       timestamp,
    type                 varchar(255),
    id_col               varchar(255),
    watch_datetimes_cols text,
    type_id              varchar(255),
    data_offset          integer,
    data_limit           integer,
    data_sort_column     varchar(255),
    id                   varchar(255) default uuid_generate_v4() not null
);

comment on table incremental_load_status is 'DEPRECATED';

alter table incremental_load_status
    owner to postgres;

```


```json
[
  {
    "connection_id": "minio1",
    "type": "MINIO",
    "in_rotation": false,
    "extra": null,
    "s3_key": "data",
    "s3_bucket_name": "dwh",
    "hdfs_endpoint_path": null
  },
  {
    "connection_id": "hdfs1",
    "type": "HDFS",
    "in_rotation": true,
    "extra": null,
    "s3_key": null,
    "s3_bucket_name": null,
    "hdfs_endpoint_path": "dwh/storage1"
  }
]

```


```json
[
  {
    "id": "b3f98ca9-190e-41f6-922e-bed9dc13f259",
    "max_thread_counts": 10,
    "table_name": "leads_cur",
    "state_current_id": 19771294959,
    "state_current_datetime": "2024-08-21 12:33:44.358927",
    "operation_type": "NEW",
    "column_id": "ID",
    "columns_watch_datetimes": "CURR_DAY",
    "type_id": "INC",
    "column_sort": "ID",
    "sort_type": "ASC",
    "pagination_offset": 0,
    "paginaton_limit": 50000,
    "pagination_total_elements": 0,
    "status": "ON_EXECUTE",
    "driver_db_name": "ORACLE",
    "operation_datetime": "2024-08-21 12:33:44.394752",
    "connection_id": "iabs_prod",
    "message": ""
  },
  {
    "id": "b3f98ca9-190e-41f6-922e-bed9dc13f256",
    "max_thread_counts": 10,
    "table_name": "employees",
    "state_current_id": 0,
    "state_current_datetime": "2024-08-21 14:43:38.177100",
    "operation_type": "NEW",
    "column_id": "id",
    "columns_watch_datetimes": "created_at,updated_at",
    "type_id": "GUID",
    "column_sort": "created_at",
    "sort_type": "ASC",
    "pagination_offset": 0,
    "paginaton_limit": 1000,
    "pagination_total_elements": 0,
    "status": "ON_EXECUTE",
    "driver_db_name": "POSTGRES",
    "operation_datetime": "2024-08-21 14:43:38.209187",
    "connection_id": "pg2",
    "message": null
  },
  {
    "id": "b3f98ca9-190e-41f6-922e-bed9dc13f258",
    "max_thread_counts": 10,
    "table_name": "leads_fs",
    "state_current_id": 0,
    "state_current_datetime": "1970-08-20 12:09:09.470000",
    "operation_type": "NEW",
    "column_id": "ID",
    "columns_watch_datetimes": "DATE_EXECUTE",
    "type_id": "INC",
    "column_sort": "ID",
    "sort_type": "ASC",
    "pagination_offset": 0,
    "paginaton_limit": 1000,
    "pagination_total_elements": 0,
    "status": "WAITING",
    "driver_db_name": "ORACLE",
    "operation_datetime": "2024-08-21 12:02:28.654891",
    "connection_id": "iabs_prod",
    "message": null
  },
  {
    "id": "b3f98ca9-190e-41f6-922e-bed9dc13f257",
    "max_thread_counts": 10,
    "table_name": "v_bank",
    "state_current_id": 0,
    "state_current_datetime": "1970-08-20 12:09:09.470000",
    "operation_type": "NEW",
    "column_id": "CODE",
    "columns_watch_datetimes": "DATE_OPEN",
    "type_id": "INC",
    "column_sort": "CODE",
    "sort_type": "ASC",
    "pagination_offset": 0,
    "paginaton_limit": 1000,
    "pagination_total_elements": 0,
    "status": "WAITING",
    "driver_db_name": "ORACLE",
    "operation_datetime": "2024-08-21 12:02:28.654891",
    "connection_id": "iabs_prod",
    "message": null
  },
  {
    "id": "b3f98ca9-190e-41f6-922e-bed9dc13f260",
    "max_thread_counts": 10,
    "table_name": "ln_card",
    "state_current_id": 5439414,
    "state_current_datetime": "2024-08-21 16:23:49.527770",
    "operation_type": "NEW",
    "column_id": "LOAN_ID",
    "columns_watch_datetimes": "DATE_MODIFY",
    "type_id": "INC",
    "column_sort": "LOAN_ID",
    "sort_type": "ASC",
    "pagination_offset": 0,
    "paginaton_limit": 50000,
    "pagination_total_elements": 0,
    "status": "ON_EXECUTE",
    "driver_db_name": "ORACLE",
    "operation_datetime": "2024-08-21 16:23:49.564023",
    "connection_id": "iabs_prod",
    "message": ""
  },
  {
    "id": "b3f98ca9-190e-41f6-922e-bed9dc13f268",
    "max_thread_counts": 10,
    "table_name": "nps_h_details",
    "state_current_id": 1158706580,
    "state_current_datetime": "2024-08-21 18:13:55.339506",
    "operation_type": "NEW",
    "column_id": "ID",
    "columns_watch_datetimes": "",
    "type_id": "INC",
    "column_sort": "ID",
    "sort_type": "ASC",
    "pagination_offset": 0,
    "paginaton_limit": 100000,
    "pagination_total_elements": 0,
    "status": "ON_EXECUTE",
    "driver_db_name": "ORACLE",
    "operation_datetime": "2024-08-21 18:13:55.378926",
    "connection_id": "iabs_prod",
    "message": null
  }
```
 