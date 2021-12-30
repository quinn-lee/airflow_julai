from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook

sshHook = SSHHook(remote_host='172.105.3.134', ssh_conn_id='172.105.3.134')

default_args = {
    'owner': 'julai_bi',
    'email': ['levine.li@quaie.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=120),
}

# 数据库备份
with DAG(
    dag_id='daily_monitor',
    default_args=default_args,
    schedule_interval='52 1,9 * * *',  # UTC时间每天1点和9点52分启动
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # mp4 fba wms数据库备份清理
    hourly_monitor_task = SSHOperator(
        task_id='daily_monitor',
        command='monitor_sh/daily_mail.sh',
        ssh_hook=sshHook
    )

