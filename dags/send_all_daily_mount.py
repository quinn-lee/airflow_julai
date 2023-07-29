from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.operators.email import EmailOperator

sshHook = SSHHook(remote_host='178.79.168.53', ssh_conn_id='178.79.168.53')
default_args = {
    'owner': 'julai_bi',
    'email': ['levine.li@quaie.com', 'chang.cai@quaie.com', 'samuel.uling@quaie.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=120),
}

# 上架数据，发邮件通知全部客户
with DAG(
    dag_id='daily_mount_email',
    default_args=default_args,
    schedule_interval='0 21 * * *',  # UTC时间每天21点0分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # 上架数据，发邮件通知全部客户
    send_daily_mount_email = SSHOperator(
        task_id='send_daily_mount_email',
        command='send_daily_mount_email/send_all_daily_mount.sh',
        ssh_hook=sshHook
    )


    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ ds }}上架数据邮件发送已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    send_daily_mount_email >> email_task
