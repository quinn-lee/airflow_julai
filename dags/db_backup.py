from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.operators.email import EmailOperator

sshHook1 = SSHHook(remote_host='178.79.168.53', ssh_conn_id='178.79.168.53')
sshHook2 = SSHHook(remote_host='172.105.3.134', ssh_conn_id='172.105.3.134')
sshHook3 = SSHHook(remote_host='47.103.131.6', ssh_conn_id='47.103.131.6')
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
    dag_id='db_backup',
    default_args=default_args,
    schedule_interval='40 0,12 * * *',  # UTC时间每天0点/12点40分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # mp4数据库备份
    mp4_db_backup_task = SSHOperator(
        task_id='mp4_db_backup',
        command='db_backup_sh/178_79_168_53_db_bak_mp4.sh',
        ssh_hook=sshHook1
    )

    # wms数据库备份
    wms_db_backup_task = SSHOperator(
        task_id='wms_db_backup',
        command='db_backup_sh/178_79_168_53_db_bak_wms.sh',
        ssh_hook=sshHook1
    )

    # finance数据库备份
    finance_db_backup_task = SSHOperator(
        task_id='finance_db_backup',
        command='db_backup_sh/172_105_3_134_db_bak_finance.sh',
        ssh_hook=sshHook2
    )

    # fba数据库备份
    fba_db_backup_task = SSHOperator(
        task_id='fba_db_backup',
        command='db_backup_sh/47_103_131_6_db_bak_fba.sh',
        ssh_hook=sshHook3
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ ds }}数据库备份批处理已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    [mp4_db_backup_task, wms_db_backup_task, finance_db_backup_task, fba_db_backup_task] >> email_task
