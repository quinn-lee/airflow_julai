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
    dag_id='storage_fee',
    default_args=default_args,
    schedule_interval='5 2 * * *',  # UTC时间每天2点5分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # 一件代发仓储费批处理
    dropshipping_task = SSHOperator(
        task_id='storage_fee_for_dropshipping',
        command='storage_fee_sh/storage_fee_for_dropshipping.sh',
        ssh_hook=sshHook
    )

    # 前置中转(FBA-NSIN)仓储费批处理
    fbansin_task = SSHOperator(
        task_id='storage_fee_for_fbansin',
        command='storage_fee_sh/storage_fee_for_fbansin.sh',
        ssh_hook=sshHook
    )

    # 前置中转(FBA)仓储费批处理
    fba_task = SSHOperator(
        task_id='storage_fee_for_fba',
        command='storage_fee_sh/storage_fee_for_fba.sh',
        ssh_hook=sshHook
    )

    # 移除换标仓储费批处理
    fbaremove_task = SSHOperator(
        task_id='storage_fee_for_fbaremove',
        command='storage_fee_sh/storage_fee_for_fbaremove.sh',
        ssh_hook=sshHook
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ yesterday_ds }}仓储费批处理已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    [dropshipping_task, fbansin_task, fba_task, fbaremove_task] >> email_task
