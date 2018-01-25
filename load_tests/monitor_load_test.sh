#!/bin/bash

# Basic database monitoring when load tests run
# Attention: THIS SCRIPT IS NOT TO BE USED ON STAGING OR PRODUCTION. TRUNCATES IMPORTANT TABLES.

# Usage: ./monitor_load_test.sh <2 * concurrent request count>

total_requests=$1
command="select count(1) from worker_results"

# Set the following environment variables
# export PGHOST='not-set'
# export PGPORT='not-set'
# export PGDATABASE='not-set'
# export PGUSER='not-set'
# export PGPASSWORD='not-set'

while true
do
	result=`psql -c "$command" | xargs | awk '{print $3}'`
	if [ $result -ge $total_requests ]; then
		echo "Test is over. Check out the generated data!!"
		date -u
		command="select worker, task_result->'_audit'->'started_at' as start_time, task_result->'_audit'->'ended_at' as end_time from worker_results"
		psql -c "$command"
		command="truncate table worker_results"
		psql -c "$command"
		command="truncate table stack_analyses_request"
		psql -c "$command"
		exit 0
	fi
	echo "Worker results count till now = $result. Expected = $total_requests"
done
