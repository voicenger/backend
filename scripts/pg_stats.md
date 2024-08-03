# PostgreSQL Statistics

## Total Connections
 total_connections 
-------------------
                 7
(1 row)

## Connections by Database
 database | connections 
----------+-------------
 postgres |           2
          |           5
(2 rows)

## Connections by State
 state  | connections 
--------+-------------
        |           5
 active |           1
 idle   |           1
(3 rows)

## Detailed Connection Info
 pid | username | database | client_address | client_port |         backend_start         | state  |         state_change          |                                                                                             query                                                                                              
-----+----------+----------+----------------+-------------+-------------------------------+--------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 129 | postgres | postgres | 192.168.65.1   |       51508 | 2024-08-03 14:47:50.817352+00 | active | 2024-08-03 14:47:50.833144+00 | SELECT pid, usename AS username, datname AS database, client_addr AS client_address, client_port, backend_start, state, state_change, query FROM pg_stat_activity ORDER BY backend_start DESC;
  56 | postgres | postgres | 192.168.65.1   |       61103 | 2024-08-03 14:35:36.107036+00 | idle   | 2024-08-03 14:35:36.125826+00 | SELECT name, setting, unit, source, context, vartype, boot_val, reset_val FROM pg_settings;
  32 | postgres |          |                |             | 2024-08-03 14:29:37.585411+00 |        |                               | 
  31 |          |          |                |             | 2024-08-03 14:29:37.585148+00 |        |                               | 
  30 |          |          |                |             | 2024-08-03 14:29:37.58471+00  |        |                               | 
  28 |          |          |                |             | 2024-08-03 14:29:37.579087+00 |        |                               | 
  27 |          |          |                |             | 2024-08-03 14:29:37.578925+00 |        |                               | 
(7 rows)

## Long Running Queries
                                                                                                                                query                                                                                                                                 | state  | duration | pid | username | database | client_address 
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------+----------+-----+----------+----------+----------------
 SELECT query, state, ROUND(EXTRACT(EPOCH FROM (clock_timestamp() - query_start))::NUMERIC, 2) AS duration, pid, usename AS username, datname AS database, client_addr AS client_address FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC LIMIT 10; | active |     0.00 | 130 | postgres | postgres | 192.168.65.1
(1 row)

## Database Sizes
  datname  |  size   
-----------+---------
 postgres  | 8789 kB
 template1 | 7525 kB
 template0 | 7297 kB
(3 rows)

## Configuration Settings
 max_connections 
-----------------
 100
(1 row)

 superuser_reserved_connections 
--------------------------------
 3
(1 row)

 shared_buffers 
----------------
 128MB
(1 row)

## Blocking and Blocked Queries
 blocked_pid | blocked_user | blocking_pid | blocking_user | blocked_query | blocking_query 
-------------+--------------+--------------+---------------+---------------+----------------
(0 rows)

## PostgreSQL Settings
                  name                  |                 setting                  | unit |       source       |      context      | vartype |                boot_val                 |                reset_val                 
----------------------------------------+------------------------------------------+------+--------------------+-------------------+---------+-----------------------------------------+------------------------------------------
 allow_in_place_tablespaces             | off                                      |      | default            | superuser         | bool    | off                                     | off
 allow_system_table_mods                | off                                      |      | default            | superuser         | bool    | off                                     | off
 application_name                       | psql                                     |      | client             | user              | string  |                                         | psql
 archive_cleanup_command                |                                          |      | default            | sighup            | string  |                                         | 
 archive_command                        | (disabled)                               |      | default            | sighup            | string  |                                         | 
 archive_library                        |                                          |      | default            | sighup            | string  |                                         | 
 archive_mode                           | off                                      |      | default            | postmaster        | enum    | off                                     | off
 archive_timeout                        | 0                                        | s    | default            | sighup            | integer | 0                                       | 0
 array_nulls                            | on                                       |      | default            | user              | bool    | on                                      | on
 authentication_timeout                 | 60                                       | s    | default            | sighup            | integer | 60                                      | 60
 autovacuum                             | on                                       |      | default            | sighup            | bool    | on                                      | on
 autovacuum_analyze_scale_factor        | 0.1                                      |      | default            | sighup            | real    | 0.1                                     | 0.1
 autovacuum_analyze_threshold           | 50                                       |      | default            | sighup            | integer | 50                                      | 50
 autovacuum_freeze_max_age              | 200000000                                |      | default            | postmaster        | integer | 200000000                               | 200000000
 autovacuum_max_workers                 | 3                                        |      | default            | postmaster        | integer | 3                                       | 3
 autovacuum_multixact_freeze_max_age    | 400000000                                |      | default            | postmaster        | integer | 400000000                               | 400000000
 autovacuum_naptime                     | 60                                       | s    | default            | sighup            | integer | 60                                      | 60
 autovacuum_vacuum_cost_delay           | 2                                        | ms   | default            | sighup            | real    | 2                                       | 2
 autovacuum_vacuum_cost_limit           | -1                                       |      | default            | sighup            | integer | -1                                      | -1
 autovacuum_vacuum_insert_scale_factor  | 0.2                                      |      | default            | sighup            | real    | 0.2                                     | 0.2
 autovacuum_vacuum_insert_threshold     | 1000                                     |      | default            | sighup            | integer | 1000                                    | 1000
 autovacuum_vacuum_scale_factor         | 0.2                                      |      | default            | sighup            | real    | 0.2                                     | 0.2
 autovacuum_vacuum_threshold            | 50                                       |      | default            | sighup            | integer | 50                                      | 50
 autovacuum_work_mem                    | -1                                       | kB   | default            | sighup            | integer | -1                                      | -1
 backend_flush_after                    | 0                                        | 8kB  | default            | user              | integer | 0                                       | 0
 backslash_quote                        | safe_encoding                            |      | default            | user              | enum    | safe_encoding                           | safe_encoding
 backtrace_functions                    |                                          |      | default            | superuser         | string  |                                         | 
 bgwriter_delay                         | 200                                      | ms   | default            | sighup            | integer | 200                                     | 200
 bgwriter_flush_after                   | 64                                       | 8kB  | default            | sighup            | integer | 64                                      | 64
 bgwriter_lru_maxpages                  | 100                                      |      | default            | sighup            | integer | 100                                     | 100
 bgwriter_lru_multiplier                | 2                                        |      | default            | sighup            | real    | 2                                       | 2
 block_size                             | 8192                                     |      | default            | internal          | integer | 8192                                    | 8192
 bonjour                                | off                                      |      | default            | postmaster        | bool    | off                                     | off
 bonjour_name                           |                                          |      | default            | postmaster        | string  |                                         | 
 bytea_output                           | hex                                      |      | default            | user              | enum    | hex                                     | hex
 check_function_bodies                  | on                                       |      | default            | user              | bool    | on                                      | on
 checkpoint_completion_target           | 0.9                                      |      | default            | sighup            | real    | 0.9                                     | 0.9
 checkpoint_flush_after                 | 32                                       | 8kB  | default            | sighup            | integer | 32                                      | 32
 checkpoint_timeout                     | 300                                      | s    | default            | sighup            | integer | 300                                     | 300
 checkpoint_warning                     | 30                                       | s    | default            | sighup            | integer | 30                                      | 30
 client_connection_check_interval       | 0                                        | ms   | default            | user              | integer | 0                                       | 0
 client_encoding                        | UTF8                                     |      | default            | user              | string  | SQL_ASCII                               | UTF8
 client_min_messages                    | notice                                   |      | default            | user              | enum    | notice                                  | notice
 cluster_name                           |                                          |      | default            | postmaster        | string  |                                         | 
 commit_delay                           | 0                                        |      | default            | superuser         | integer | 0                                       | 0
 commit_siblings                        | 5                                        |      | default            | user              | integer | 5                                       | 5
 compute_query_id                       | auto                                     |      | default            | superuser         | enum    | auto                                    | auto
 config_file                            | /var/lib/postgresql/data/postgresql.conf |      | override           | postmaster        | string  |                                         | /var/lib/postgresql/data/postgresql.conf
 constraint_exclusion                   | partition                                |      | default            | user              | enum    | partition                               | partition
 cpu_index_tuple_cost                   | 0.005                                    |      | default            | user              | real    | 0.005                                   | 0.005
 cpu_operator_cost                      | 0.0025                                   |      | default            | user              | real    | 0.0025                                  | 0.0025
 cpu_tuple_cost                         | 0.01                                     |      | default            | user              | real    | 0.01                                    | 0.01
 cursor_tuple_fraction                  | 0.1                                      |      | default            | user              | real    | 0.1                                     | 0.1
 data_checksums                         | off                                      |      | default            | internal          | bool    | off                                     | off
 data_directory                         | /var/lib/postgresql/data                 |      | override           | postmaster        | string  |                                         | /var/lib/postgresql/data
 data_directory_mode                    | 0700                                     |      | default            | internal          | integer | 448                                     | 448
 data_sync_retry                        | off                                      |      | default            | postmaster        | bool    | off                                     | off
 DateStyle                              | ISO, MDY                                 |      | configuration file | user              | string  | ISO, MDY                                | ISO, MDY
 db_user_namespace                      | off                                      |      | default            | sighup            | bool    | off                                     | off
 deadlock_timeout                       | 1000                                     | ms   | default            | superuser         | integer | 1000                                    | 1000
 debug_assertions                       | off                                      |      | default            | internal          | bool    | off                                     | off
 debug_discard_caches                   | 0                                        |      | default            | superuser         | integer | 0                                       | 0
 debug_pretty_print                     | on                                       |      | default            | user              | bool    | on                                      | on
 debug_print_parse                      | off                                      |      | default            | user              | bool    | off                                     | off
 debug_print_plan                       | off                                      |      | default            | user              | bool    | off                                     | off
 debug_print_rewritten                  | off                                      |      | default            | user              | bool    | off                                     | off
 default_statistics_target              | 100                                      |      | default            | user              | integer | 100                                     | 100
 default_table_access_method            | heap                                     |      | default            | user              | string  | heap                                    | heap
 default_tablespace                     |                                          |      | default            | user              | string  |                                         | 
 default_text_search_config             | pg_catalog.english                       |      | configuration file | user              | string  | pg_catalog.simple                       | pg_catalog.english
 default_toast_compression              | pglz                                     |      | default            | user              | enum    | pglz                                    | pglz
 default_transaction_deferrable         | off                                      |      | default            | user              | bool    | off                                     | off
 default_transaction_isolation          | read committed                           |      | default            | user              | enum    | read committed                          | read committed
 default_transaction_read_only          | off                                      |      | default            | user              | bool    | off                                     | off
 dynamic_library_path                   | $libdir                                  |      | default            | superuser         | string  | $libdir                                 | $libdir
 dynamic_shared_memory_type             | posix                                    |      | configuration file | postmaster        | enum    | posix                                   | posix
 effective_cache_size                   | 524288                                   | 8kB  | default            | user              | integer | 524288                                  | 524288
 effective_io_concurrency               | 1                                        |      | default            | user              | integer | 1                                       | 1
 enable_async_append                    | on                                       |      | default            | user              | bool    | on                                      | on
 enable_bitmapscan                      | on                                       |      | default            | user              | bool    | on                                      | on
 enable_gathermerge                     | on                                       |      | default            | user              | bool    | on                                      | on
 enable_hashagg                         | on                                       |      | default            | user              | bool    | on                                      | on
 enable_hashjoin                        | on                                       |      | default            | user              | bool    | on                                      | on
 enable_incremental_sort                | on                                       |      | default            | user              | bool    | on                                      | on
 enable_indexonlyscan                   | on                                       |      | default            | user              | bool    | on                                      | on
 enable_indexscan                       | on                                       |      | default            | user              | bool    | on                                      | on
 enable_material                        | on                                       |      | default            | user              | bool    | on                                      | on
 enable_memoize                         | on                                       |      | default            | user              | bool    | on                                      | on
 enable_mergejoin                       | on                                       |      | default            | user              | bool    | on                                      | on
 enable_nestloop                        | on                                       |      | default            | user              | bool    | on                                      | on
 enable_parallel_append                 | on                                       |      | default            | user              | bool    | on                                      | on
 enable_parallel_hash                   | on                                       |      | default            | user              | bool    | on                                      | on
 enable_partition_pruning               | on                                       |      | default            | user              | bool    | on                                      | on
 enable_partitionwise_aggregate         | off                                      |      | default            | user              | bool    | off                                     | off
 enable_partitionwise_join              | off                                      |      | default            | user              | bool    | off                                     | off
 enable_seqscan                         | on                                       |      | default            | user              | bool    | on                                      | on
 enable_sort                            | on                                       |      | default            | user              | bool    | on                                      | on
 enable_tidscan                         | on                                       |      | default            | user              | bool    | on                                      | on
 escape_string_warning                  | on                                       |      | default            | user              | bool    | on                                      | on
 event_source                           | PostgreSQL                               |      | default            | postmaster        | string  | PostgreSQL                              | PostgreSQL
 exit_on_error                          | off                                      |      | default            | user              | bool    | off                                     | off
 extension_destdir                      |                                          |      | default            | superuser         | string  |                                         | 
 external_pid_file                      |                                          |      | default            | postmaster        | string  |                                         | 
 extra_float_digits                     | 1                                        |      | default            | user              | integer | 1                                       | 1
 force_parallel_mode                    | off                                      |      | default            | user              | enum    | off                                     | off
 from_collapse_limit                    | 8                                        |      | default            | user              | integer | 8                                       | 8
 fsync                                  | on                                       |      | default            | sighup            | bool    | on                                      | on
 full_page_writes                       | on                                       |      | default            | sighup            | bool    | on                                      | on
 geqo                                   | on                                       |      | default            | user              | bool    | on                                      | on
 geqo_effort                            | 5                                        |      | default            | user              | integer | 5                                       | 5
 geqo_generations                       | 0                                        |      | default            | user              | integer | 0                                       | 0
 geqo_pool_size                         | 0                                        |      | default            | user              | integer | 0                                       | 0
 geqo_seed                              | 0                                        |      | default            | user              | real    | 0                                       | 0
 geqo_selection_bias                    | 2                                        |      | default            | user              | real    | 2                                       | 2
 geqo_threshold                         | 12                                       |      | default            | user              | integer | 12                                      | 12
 gin_fuzzy_search_limit                 | 0                                        |      | default            | user              | integer | 0                                       | 0
 gin_pending_list_limit                 | 4096                                     | kB   | default            | user              | integer | 4096                                    | 4096
 hash_mem_multiplier                    | 2                                        |      | default            | user              | real    | 2                                       | 2
 hba_file                               | /var/lib/postgresql/data/pg_hba.conf     |      | override           | postmaster        | string  |                                         | /var/lib/postgresql/data/pg_hba.conf
 hot_standby                            | on                                       |      | default            | postmaster        | bool    | on                                      | on
 hot_standby_feedback                   | off                                      |      | default            | sighup            | bool    | off                                     | off
 huge_page_size                         | 0                                        | kB   | default            | postmaster        | integer | 0                                       | 0
 huge_pages                             | try                                      |      | default            | postmaster        | enum    | try                                     | try
 ident_file                             | /var/lib/postgresql/data/pg_ident.conf   |      | override           | postmaster        | string  |                                         | /var/lib/postgresql/data/pg_ident.conf
 idle_in_transaction_session_timeout    | 0                                        | ms   | default            | user              | integer | 0                                       | 0
 idle_session_timeout                   | 0                                        | ms   | default            | user              | integer | 0                                       | 0
 ignore_checksum_failure                | off                                      |      | default            | superuser         | bool    | off                                     | off
 ignore_invalid_pages                   | off                                      |      | default            | postmaster        | bool    | off                                     | off
 ignore_system_indexes                  | off                                      |      | default            | backend           | bool    | off                                     | off
 in_hot_standby                         | off                                      |      | default            | internal          | bool    | off                                     | off
 integer_datetimes                      | on                                       |      | default            | internal          | bool    | on                                      | on
 IntervalStyle                          | postgres                                 |      | default            | user              | enum    | postgres                                | postgres
 jit                                    | on                                       |      | default            | user              | bool    | on                                      | on
 jit_above_cost                         | 100000                                   |      | default            | user              | real    | 100000                                  | 100000
 jit_debugging_support                  | off                                      |      | default            | superuser-backend | bool    | off                                     | off
 jit_dump_bitcode                       | off                                      |      | default            | superuser         | bool    | off                                     | off
 jit_expressions                        | on                                       |      | default            | user              | bool    | on                                      | on
 jit_inline_above_cost                  | 500000                                   |      | default            | user              | real    | 500000                                  | 500000
 jit_optimize_above_cost                | 500000                                   |      | default            | user              | real    | 500000                                  | 500000
 jit_profiling_support                  | off                                      |      | default            | superuser-backend | bool    | off                                     | off
 jit_provider                           | llvmjit                                  |      | default            | postmaster        | string  | llvmjit                                 | llvmjit
 jit_tuple_deforming                    | on                                       |      | default            | user              | bool    | on                                      | on
 join_collapse_limit                    | 8                                        |      | default            | user              | integer | 8                                       | 8
 krb_caseins_users                      | off                                      |      | default            | sighup            | bool    | off                                     | off
 krb_server_keyfile                     | FILE:/etc/postgresql-common/krb5.keytab  |      | default            | sighup            | string  | FILE:/etc/postgresql-common/krb5.keytab | FILE:/etc/postgresql-common/krb5.keytab
 lc_collate                             | en_US.utf8                               |      | default            | internal          | string  | C                                       | en_US.utf8
 lc_ctype                               | en_US.utf8                               |      | default            | internal          | string  | C                                       | en_US.utf8
 lc_messages                            | en_US.utf8                               |      | configuration file | superuser         | string  |                                         | en_US.utf8
 lc_monetary                            | en_US.utf8                               |      | configuration file | user              | string  | C                                       | en_US.utf8
 lc_numeric                             | en_US.utf8                               |      | configuration file | user              | string  | C                                       | en_US.utf8
 lc_time                                | en_US.utf8                               |      | configuration file | user              | string  | C                                       | en_US.utf8
 listen_addresses                       | *                                        |      | configuration file | postmaster        | string  | localhost                               | *
 lo_compat_privileges                   | off                                      |      | default            | superuser         | bool    | off                                     | off
 local_preload_libraries                |                                          |      | default            | user              | string  |                                         | 
 lock_timeout                           | 0                                        | ms   | default            | user              | integer | 0                                       | 0
 log_autovacuum_min_duration            | 600000                                   | ms   | default            | sighup            | integer | 600000                                  | 600000
 log_checkpoints                        | on                                       |      | default            | sighup            | bool    | on                                      | on
 log_connections                        | off                                      |      | default            | superuser-backend | bool    | off                                     | off
 log_destination                        | stderr                                   |      | default            | sighup            | string  | stderr                                  | stderr
 log_directory                          | log                                      |      | default            | sighup            | string  | log                                     | log
 log_disconnections                     | off                                      |      | default            | superuser-backend | bool    | off                                     | off
 log_duration                           | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_error_verbosity                    | default                                  |      | default            | superuser         | enum    | default                                 | default
 log_executor_stats                     | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_file_mode                          | 0600                                     |      | default            | sighup            | integer | 384                                     | 384
 log_filename                           | postgresql-%Y-%m-%d_%H%M%S.log           |      | default            | sighup            | string  | postgresql-%Y-%m-%d_%H%M%S.log          | postgresql-%Y-%m-%d_%H%M%S.log
 log_hostname                           | off                                      |      | default            | sighup            | bool    | off                                     | off
 log_line_prefix                        | %m [%p]                                  |      | default            | sighup            | string  | %m [%p]                                 | %m [%p] 
 log_lock_waits                         | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_min_duration_sample                | -1                                       | ms   | default            | superuser         | integer | -1                                      | -1
 log_min_duration_statement             | -1                                       | ms   | default            | superuser         | integer | -1                                      | -1
 log_min_error_statement                | error                                    |      | default            | superuser         | enum    | error                                   | error
 log_min_messages                       | warning                                  |      | default            | superuser         | enum    | warning                                 | warning
 log_parameter_max_length               | -1                                       | B    | default            | superuser         | integer | -1                                      | -1
 log_parameter_max_length_on_error      | 0                                        | B    | default            | user              | integer | 0                                       | 0
 log_parser_stats                       | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_planner_stats                      | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_recovery_conflict_waits            | off                                      |      | default            | sighup            | bool    | off                                     | off
 log_replication_commands               | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_rotation_age                       | 1440                                     | min  | default            | sighup            | integer | 1440                                    | 1440
 log_rotation_size                      | 10240                                    | kB   | default            | sighup            | integer | 10240                                   | 10240
 log_startup_progress_interval          | 10000                                    | ms   | default            | sighup            | integer | 10000                                   | 10000
 log_statement                          | none                                     |      | default            | superuser         | enum    | none                                    | none
 log_statement_sample_rate              | 1                                        |      | default            | superuser         | real    | 1                                       | 1
 log_statement_stats                    | off                                      |      | default            | superuser         | bool    | off                                     | off
 log_temp_files                         | -1                                       | kB   | default            | superuser         | integer | -1                                      | -1
 log_timezone                           | Etc/UTC                                  |      | configuration file | sighup            | string  | GMT                                     | Etc/UTC
 log_transaction_sample_rate            | 0                                        |      | default            | superuser         | real    | 0                                       | 0
 log_truncate_on_rotation               | off                                      |      | default            | sighup            | bool    | off                                     | off
 logging_collector                      | off                                      |      | default            | postmaster        | bool    | off                                     | off
 logical_decoding_work_mem              | 65536                                    | kB   | default            | user              | integer | 65536                                   | 65536
 maintenance_io_concurrency             | 10                                       |      | default            | user              | integer | 10                                      | 10
 maintenance_work_mem                   | 65536                                    | kB   | default            | user              | integer | 65536                                   | 65536
 max_connections                        | 100                                      |      | configuration file | postmaster        | integer | 100                                     | 100
 max_files_per_process                  | 1000                                     |      | default            | postmaster        | integer | 1000                                    | 1000
 max_function_args                      | 100                                      |      | default            | internal          | integer | 100                                     | 100
 max_identifier_length                  | 63                                       |      | default            | internal          | integer | 63                                      | 63
 max_index_keys                         | 32                                       |      | default            | internal          | integer | 32                                      | 32
 max_locks_per_transaction              | 64                                       |      | default            | postmaster        | integer | 64                                      | 64
 max_logical_replication_workers        | 4                                        |      | default            | postmaster        | integer | 4                                       | 4
 max_parallel_maintenance_workers       | 2                                        |      | default            | user              | integer | 2                                       | 2
 max_parallel_workers                   | 8                                        |      | default            | user              | integer | 8                                       | 8
 max_parallel_workers_per_gather        | 2                                        |      | default            | user              | integer | 2                                       | 2
 max_pred_locks_per_page                | 2                                        |      | default            | sighup            | integer | 2                                       | 2
 max_pred_locks_per_relation            | -2                                       |      | default            | sighup            | integer | -2                                      | -2
 max_pred_locks_per_transaction         | 64                                       |      | default            | postmaster        | integer | 64                                      | 64
 max_prepared_transactions              | 0                                        |      | default            | postmaster        | integer | 0                                       | 0
 max_replication_slots                  | 10                                       |      | default            | postmaster        | integer | 10                                      | 10
 max_slot_wal_keep_size                 | -1                                       | MB   | default            | sighup            | integer | -1                                      | -1
 max_stack_depth                        | 2048                                     | kB   | default            | superuser         | integer | 100                                     | 2048
 max_standby_archive_delay              | 30000                                    | ms   | default            | sighup            | integer | 30000                                   | 30000
 max_standby_streaming_delay            | 30000                                    | ms   | default            | sighup            | integer | 30000                                   | 30000
 max_sync_workers_per_subscription      | 2                                        |      | default            | sighup            | integer | 2                                       | 2
 max_wal_senders                        | 10                                       |      | default            | postmaster        | integer | 10                                      | 10
 max_wal_size                           | 1024                                     | MB   | configuration file | sighup            | integer | 1024                                    | 1024
 max_worker_processes                   | 8                                        |      | default            | postmaster        | integer | 8                                       | 8
 min_dynamic_shared_memory              | 0                                        | MB   | default            | postmaster        | integer | 0                                       | 0
 min_parallel_index_scan_size           | 64                                       | 8kB  | default            | user              | integer | 64                                      | 64
 min_parallel_table_scan_size           | 1024                                     | 8kB  | default            | user              | integer | 1024                                    | 1024
 min_wal_size                           | 80                                       | MB   | configuration file | sighup            | integer | 80                                      | 80
 old_snapshot_threshold                 | -1                                       | min  | default            | postmaster        | integer | -1                                      | -1
 parallel_leader_participation          | on                                       |      | default            | user              | bool    | on                                      | on
 parallel_setup_cost                    | 1000                                     |      | default            | user              | real    | 1000                                    | 1000
 parallel_tuple_cost                    | 0.1                                      |      | default            | user              | real    | 0.1                                     | 0.1
 password_encryption                    | scram-sha-256                            |      | default            | user              | enum    | scram-sha-256                           | scram-sha-256
 plan_cache_mode                        | auto                                     |      | default            | user              | enum    | auto                                    | auto
 port                                   | 5432                                     |      | default            | postmaster        | integer | 5432                                    | 5432
 post_auth_delay                        | 0                                        | s    | default            | backend           | integer | 0                                       | 0
 pre_auth_delay                         | 0                                        | s    | default            | sighup            | integer | 0                                       | 0
 primary_conninfo                       |                                          |      | default            | sighup            | string  |                                         | 
 primary_slot_name                      |                                          |      | default            | sighup            | string  |                                         | 
 promote_trigger_file                   |                                          |      | default            | sighup            | string  |                                         | 
 quote_all_identifiers                  | off                                      |      | default            | user              | bool    | off                                     | off
 random_page_cost                       | 4                                        |      | default            | user              | real    | 4                                       | 4
 recovery_end_command                   |                                          |      | default            | sighup            | string  |                                         | 
 recovery_init_sync_method              | fsync                                    |      | default            | sighup            | enum    | fsync                                   | fsync
 recovery_min_apply_delay               | 0                                        | ms   | default            | sighup            | integer | 0                                       | 0
 recovery_prefetch                      | try                                      |      | default            | sighup            | enum    | try                                     | try
 recovery_target                        |                                          |      | default            | postmaster        | string  |                                         | 
 recovery_target_action                 | pause                                    |      | default            | postmaster        | enum    | pause                                   | pause
 recovery_target_inclusive              | on                                       |      | default            | postmaster        | bool    | on                                      | on
 recovery_target_lsn                    |                                          |      | default            | postmaster        | string  |                                         | 
 recovery_target_name                   |                                          |      | default            | postmaster        | string  |                                         | 
 recovery_target_time                   |                                          |      | default            | postmaster        | string  |                                         | 
 recovery_target_timeline               | latest                                   |      | default            | postmaster        | string  | latest                                  | latest
 recovery_target_xid                    |                                          |      | default            | postmaster        | string  |                                         | 
 recursive_worktable_factor             | 10                                       |      | default            | user              | real    | 10                                      | 10
 remove_temp_files_after_crash          | on                                       |      | default            | sighup            | bool    | on                                      | on
 restart_after_crash                    | on                                       |      | default            | sighup            | bool    | on                                      | on
 restore_command                        |                                          |      | default            | sighup            | string  |                                         | 
 row_security                           | on                                       |      | default            | user              | bool    | on                                      | on
 search_path                            | "$user", public                          |      | default            | user              | string  | "$user", public                         | "$user", public
 segment_size                           | 131072                                   | 8kB  | default            | internal          | integer | 131072                                  | 131072
 seq_page_cost                          | 1                                        |      | default            | user              | real    | 1                                       | 1
 server_encoding                        | UTF8                                     |      | default            | internal          | string  | SQL_ASCII                               | UTF8
 server_version                         | 15.7 (Debian 15.7-1.pgdg120+1)           |      | default            | internal          | string  | 15.7 (Debian 15.7-1.pgdg120+1)          | 15.7 (Debian 15.7-1.pgdg120+1)
 server_version_num                     | 150007                                   |      | default            | internal          | integer | 150007                                  | 150007
 session_preload_libraries              |                                          |      | default            | superuser         | string  |                                         | 
 session_replication_role               | origin                                   |      | default            | superuser         | enum    | origin                                  | origin
 shared_buffers                         | 16384                                    | 8kB  | configuration file | postmaster        | integer | 16384                                   | 16384
 shared_memory_size                     | 143                                      | MB   | default            | internal          | integer | 0                                       | 143
 shared_memory_size_in_huge_pages       | 72                                       |      | default            | internal          | integer | -1                                      | 72
 shared_memory_type                     | mmap                                     |      | default            | postmaster        | enum    | mmap                                    | mmap
 shared_preload_libraries               |                                          |      | default            | postmaster        | string  |                                         | 
 ssl                                    | off                                      |      | default            | sighup            | bool    | off                                     | off
 ssl_ca_file                            |                                          |      | default            | sighup            | string  |                                         | 
 ssl_cert_file                          | server.crt                               |      | default            | sighup            | string  | server.crt                              | server.crt
 ssl_ciphers                            | HIGH:MEDIUM:+3DES:!aNULL                 |      | default            | sighup            | string  | HIGH:MEDIUM:+3DES:!aNULL                | HIGH:MEDIUM:+3DES:!aNULL
 ssl_crl_dir                            |                                          |      | default            | sighup            | string  |                                         | 
 ssl_crl_file                           |                                          |      | default            | sighup            | string  |                                         | 
 ssl_dh_params_file                     |                                          |      | default            | sighup            | string  |                                         | 
 ssl_ecdh_curve                         | prime256v1                               |      | default            | sighup            | string  | prime256v1                              | prime256v1
 ssl_key_file                           | server.key                               |      | default            | sighup            | string  | server.key                              | server.key
 ssl_library                            | OpenSSL                                  |      | default            | internal          | string  | OpenSSL                                 | OpenSSL
 ssl_max_protocol_version               |                                          |      | default            | sighup            | enum    |                                         | 
 ssl_min_protocol_version               | TLSv1.2                                  |      | default            | sighup            | enum    | TLSv1.2                                 | TLSv1.2
 ssl_passphrase_command                 |                                          |      | default            | sighup            | string  |                                         | 
 ssl_passphrase_command_supports_reload | off                                      |      | default            | sighup            | bool    | off                                     | off
 ssl_prefer_server_ciphers              | on                                       |      | default            | sighup            | bool    | on                                      | on
 standard_conforming_strings            | on                                       |      | default            | user              | bool    | on                                      | on
 statement_timeout                      | 0                                        | ms   | default            | user              | integer | 0                                       | 0
 stats_fetch_consistency                | cache                                    |      | default            | user              | enum    | cache                                   | cache
 superuser_reserved_connections         | 3                                        |      | default            | postmaster        | integer | 3                                       | 3
 synchronize_seqscans                   | on                                       |      | default            | user              | bool    | on                                      | on
 synchronous_commit                     | on                                       |      | default            | user              | enum    | on                                      | on
 synchronous_standby_names              |                                          |      | default            | sighup            | string  |                                         | 
 syslog_facility                        | local0                                   |      | default            | sighup            | enum    | local0                                  | local0
 syslog_ident                           | postgres                                 |      | default            | sighup            | string  | postgres                                | postgres
 syslog_sequence_numbers                | on                                       |      | default            | sighup            | bool    | on                                      | on
 syslog_split_messages                  | on                                       |      | default            | sighup            | bool    | on                                      | on
 tcp_keepalives_count                   | 9                                        |      | default            | user              | integer | 0                                       | 0
 tcp_keepalives_idle                    | 7200                                     | s    | default            | user              | integer | 0                                       | 0
 tcp_keepalives_interval                | 75                                       | s    | default            | user              | integer | 0                                       | 0
 tcp_user_timeout                       | 0                                        | ms   | default            | user              | integer | 0                                       | 0
 temp_buffers                           | 1024                                     | 8kB  | default            | user              | integer | 1024                                    | 1024
 temp_file_limit                        | -1                                       | kB   | default            | superuser         | integer | -1                                      | -1
 temp_tablespaces                       |                                          |      | default            | user              | string  |                                         | 
 TimeZone                               | Etc/UTC                                  |      | configuration file | user              | string  | GMT                                     | Etc/UTC
 timezone_abbreviations                 | Default                                  |      | default            | user              | string  |                                         | Default
 trace_notify                           | off                                      |      | default            | user              | bool    | off                                     | off
 trace_recovery_messages                | log                                      |      | default            | sighup            | enum    | log                                     | log
 trace_sort                             | off                                      |      | default            | user              | bool    | off                                     | off
 track_activities                       | on                                       |      | default            | superuser         | bool    | on                                      | on
 track_activity_query_size              | 1024                                     | B    | default            | postmaster        | integer | 1024                                    | 1024
 track_commit_timestamp                 | off                                      |      | default            | postmaster        | bool    | off                                     | off
 track_counts                           | on                                       |      | default            | superuser         | bool    | on                                      | on
 track_functions                        | none                                     |      | default            | superuser         | enum    | none                                    | none
 track_io_timing                        | off                                      |      | default            | superuser         | bool    | off                                     | off
 track_wal_io_timing                    | off                                      |      | default            | superuser         | bool    | off                                     | off
 transaction_deferrable                 | off                                      |      | override           | user              | bool    | off                                     | off
 transaction_isolation                  | read committed                           |      | override           | user              | enum    | read committed                          | read committed
 transaction_read_only                  | off                                      |      | override           | user              | bool    | off                                     | off
 transform_null_equals                  | off                                      |      | default            | user              | bool    | off                                     | off
 unix_socket_directories                | /var/run/postgresql                      |      | default            | postmaster        | string  | /var/run/postgresql                     | /var/run/postgresql
 unix_socket_group                      |                                          |      | default            | postmaster        | string  |                                         | 
 unix_socket_permissions                | 0777                                     |      | default            | postmaster        | integer | 511                                     | 511
 update_process_title                   | on                                       |      | default            | superuser         | bool    | on                                      | on
 vacuum_cost_delay                      | 0                                        | ms   | default            | user              | real    | 0                                       | 0
 vacuum_cost_limit                      | 200                                      |      | default            | user              | integer | 200                                     | 200
 vacuum_cost_page_dirty                 | 20                                       |      | default            | user              | integer | 20                                      | 20
 vacuum_cost_page_hit                   | 1                                        |      | default            | user              | integer | 1                                       | 1
 vacuum_cost_page_miss                  | 2                                        |      | default            | user              | integer | 2                                       | 2
 vacuum_defer_cleanup_age               | 0                                        |      | default            | sighup            | integer | 0                                       | 0
 vacuum_failsafe_age                    | 1600000000                               |      | default            | user              | integer | 1600000000                              | 1600000000
 vacuum_freeze_min_age                  | 50000000                                 |      | default            | user              | integer | 50000000                                | 50000000
 vacuum_freeze_table_age                | 150000000                                |      | default            | user              | integer | 150000000                               | 150000000
 vacuum_multixact_failsafe_age          | 1600000000                               |      | default            | user              | integer | 1600000000                              | 1600000000
 vacuum_multixact_freeze_min_age        | 5000000                                  |      | default            | user              | integer | 5000000                                 | 5000000
 vacuum_multixact_freeze_table_age      | 150000000                                |      | default            | user              | integer | 150000000                               | 150000000
 wal_block_size                         | 8192                                     |      | default            | internal          | integer | 8192                                    | 8192
 wal_buffers                            | 512                                      | 8kB  | default            | postmaster        | integer | -1                                      | 512
 wal_compression                        | off                                      |      | default            | superuser         | enum    | off                                     | off
 wal_consistency_checking               |                                          |      | default            | superuser         | string  |                                         | 
 wal_decode_buffer_size                 | 524288                                   | B    | default            | postmaster        | integer | 524288                                  | 524288
 wal_init_zero                          | on                                       |      | default            | superuser         | bool    | on                                      | on
 wal_keep_size                          | 0                                        | MB   | default            | sighup            | integer | 0                                       | 0
 wal_level                              | replica                                  |      | default            | postmaster        | enum    | replica                                 | replica
 wal_log_hints                          | off                                      |      | default            | postmaster        | bool    | off                                     | off
 wal_receiver_create_temp_slot          | off                                      |      | default            | sighup            | bool    | off                                     | off
 wal_receiver_status_interval           | 10                                       | s    | default            | sighup            | integer | 10                                      | 10
 wal_receiver_timeout                   | 60000                                    | ms   | default            | sighup            | integer | 60000                                   | 60000
 wal_recycle                            | on                                       |      | default            | superuser         | bool    | on                                      | on
 wal_retrieve_retry_interval            | 5000                                     | ms   | default            | sighup            | integer | 5000                                    | 5000
 wal_segment_size                       | 16777216                                 | B    | default            | internal          | integer | 16777216                                | 16777216
 wal_sender_timeout                     | 60000                                    | ms   | default            | user              | integer | 60000                                   | 60000
 wal_skip_threshold                     | 2048                                     | kB   | default            | user              | integer | 2048                                    | 2048
 wal_sync_method                        | fdatasync                                |      | default            | sighup            | enum    | fdatasync                               | fdatasync
 wal_writer_delay                       | 200                                      | ms   | default            | sighup            | integer | 200                                     | 200
 wal_writer_flush_after                 | 128                                      | 8kB  | default            | sighup            | integer | 128                                     | 128
 work_mem                               | 4096                                     | kB   | default            | user              | integer | 4096                                    | 4096
 xmlbinary                              | base64                                   |      | default            | user              | enum    | base64                                  | base64
 xmloption                              | content                                  |      | default            | user              | enum    | content                                 | content
 zero_damaged_pages                     | off                                      |      | default            | superuser         | bool    | off                                     | off
(353 rows)

