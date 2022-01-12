from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.operators.email import EmailOperator

sshHook1 = SSHHook(remote_host='178.79.168.53', ssh_conn_id='178.79.168.53')
sshHook2 = SSHHook(remote_host='172.105.3.134', ssh_conn_id='172.105.3.134')

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
    dag_id='clean_log',
    default_args=default_args,
    schedule_interval='15 23 * * *',  # UTC时间每天晚上23点15分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # mp4admin日志清理
    clean_mp4admin_log_task = SSHOperator(
        task_id='clean_mp4admin_log',
        command='clean_log_sh/178_79_168_53_clean_log_mp4admin.sh',
        ssh_hook=sshHook1
    )

    # 仓库端wms日志清理
    clean_wms_log_task = SSHOperator(
        task_id='clean_wms_log',
        command='clean_log_sh/178_79_168_53_clean_log_wms.sh',
        ssh_hook=sshHook1
    )

    # 移动端wms日志清理
    clean_wms_mobile_log_task = SSHOperator(
        task_id='clean_wms_mobile_log',
        command='clean_log_sh/178_79_168_53_clean_log_wms_mobile.sh',
        ssh_hook=sshHook1
    )

    # 仓库端wms日志清理
    clean_wms_customer_log_task = SSHOperator(
        task_id='clean_wms_customer_log',
        command='clean_log_sh/172_105_3_134_clean_log_wms.sh',
        ssh_hook=sshHook2
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ ds }}日志清理批处理已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    [clean_mp4admin_log_task, clean_wms_log_task, clean_wms_mobile_log_task, clean_wms_customer_log_task] >> email_task
