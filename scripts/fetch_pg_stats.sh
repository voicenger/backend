#!/bin/bash

# Credentials from environment variables
export PGUSER=${PGUSER:-postgres}
export PGPASSWORD=${PGPASSWORD:-postgres}
export PGDATABASE=${PGDATABASE:-postgres}
export PGHOST=${PGHOST:-localhost}
export PGPORT=${PGPORT:-5432}

# Connection string
CONN="psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE"

# Output file
OUTPUT_FILE="./pg_stats.md"

# Write results to Markdown file
{
  echo "# PostgreSQL Statistics"
  echo
  echo "## Total Connections"
  echo '```sql'
  $CONN -c "SELECT COUNT(*) AS total_connections FROM pg_stat_activity;"
  echo '```'
  echo

  echo "## Connections by Database"
  echo '```sql'
  $CONN -c "SELECT datname AS database, COUNT(*) AS connections FROM pg_stat_activity GROUP BY datname;"
  echo '```'
  echo

  echo "## Connections by State"
  echo '```sql'
  $CONN -c "SELECT state, COUNT(*) AS connections FROM pg_stat_activity GROUP BY state;"
  echo '```'
  echo

  echo "## Detailed Connection Info"
  echo '```sql'
  $CONN -c "SELECT pid, usename AS username, datname AS database, client_addr AS client_address, client_port, backend_start, state, state_change, query FROM pg_stat_activity ORDER BY backend_start DESC;"
  echo '```'
  echo

  echo "## Long Running Queries"
  echo '```sql'
  $CONN -c "SELECT query, state, ROUND(EXTRACT(EPOCH FROM (clock_timestamp() - query_start))::NUMERIC, 2) AS duration, pid, usename AS username, datname AS database, client_addr AS client_address FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC LIMIT 10;"
  echo '```'
  echo

  echo "## Database Sizes"
  echo '```sql'
  $CONN -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;"
  echo '```'
  echo

  echo "## Configuration Settings"
  echo '```sql'
  $CONN -c "SHOW max_connections;"
  $CONN -c "SHOW superuser_reserved_connections;"
  $CONN -c "SHOW shared_buffers;"
  echo '```'
  echo

  echo "## Blocking and Blocked Queries"
  echo '```sql'
  $CONN -c "
    SELECT 
      blocked_locks.pid AS blocked_pid,
      blocked_activity.usename AS blocked_user,
      blocking_locks.pid AS blocking_pid,
      blocking_activity.usename AS blocking_user,
      blocked_activity.query AS blocked_query,
      blocking_activity.query AS blocking_query
    FROM 
      pg_catalog.pg_locks blocked_locks
    JOIN 
      pg_catalog.pg_stat_activity blocked_activity 
      ON blocked_activity.pid = blocked_locks.pid
    JOIN 
      pg_catalog.pg_locks blocking_locks 
      ON blocking_locks.locktype = blocked_locks.locktype 
      AND blocking_locks.database = blocked_locks.database 
      AND blocking_locks.relation = blocked_locks.relation 
      AND blocking_locks.page = blocked_locks.page 
      AND blocking_locks.tuple = blocked_locks.tuple::text::int
      AND blocking_locks.virtualxid = blocked_locks.virtualxid 
      AND blocking_locks.transactionid = blocked_locks.transactionid 
      AND blocking_locks.classid = blocked_locks.classid 
      AND blocking_locks.objid = blocked_locks.objid 
      AND blocking_locks.objsubid = blocked_locks.objsubid 
    JOIN 
      pg_catalog.pg_stat_activity blocking_activity 
      ON blocking_activity.pid = blocking_locks.pid
    WHERE 
      NOT blocked_locks.granted;
  "
  echo '```'
  echo

  echo "## PostgreSQL Settings"
  echo '```sql'
  $CONN -c "SELECT name, setting, unit, source, context, vartype, boot_val, reset_val FROM pg_settings;"
  echo '```'
} | tee "$OUTPUT_FILE"
