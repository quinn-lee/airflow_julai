from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.operators.email import EmailOperator

sshHook = SSHHook(remote_host='178.79.168.53', ssh_conn_id='178.79.168.53')
default_args = {
    'owner': 'julai_bi',
    'email': ['levine.li@quaie.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=120),
}

# pjs_dhl
with DAG(
    dag_id='dhl_pjs_trigger_cron_30',
    default_args=default_args,
    schedule_interval='15,45 8-16 * * *',  # 每半小时跑一次
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=30),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # pjs_dhl每半小时批处理
    dhl_pjs_trigger_cron_task = SSHOperator(
        task_id='dhl_pjs_trigger_cron_30',
        command='dhl_pjs_trigger_cron_sh/dhl_pjs_trigger_cron.sh',
        ssh_hook=sshHook
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ ds }}pjs_dhl每半小时批处理',
        html_content="""<h3>任务正常结束<h3>"""
    )

    dhl_pjs_trigger_cron_task >> email_task
