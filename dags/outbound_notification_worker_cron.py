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

# 出库时效统计
with DAG(
    dag_id='outbound_notification_worker_cron',
    default_args=default_args,
    schedule_interval='0 9 * * 0,6',  # UTC时间每周末9点
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=360),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # 自动出库批处理
    outbound_notification_worker_task = SSHOperator(
        task_id='outbound_notification_worker',
        command='outbound_notification_worker_sh/outbound_notification_worker.sh',
        ssh_hook=sshHook
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ ds }}自动出单批处理已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    outbound_notification_worker_task >> email_task
