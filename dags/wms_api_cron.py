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
    dag_id='wms_api_cron',
    default_args=default_args,
    schedule_interval='15 0 * * *',  # UTC时间每天0点30分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=360),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # 获取库存总体积数
    get_inventory_total_volume_task = SSHOperator(
        task_id='get_inventory_total_volume',
        command='wms_api_cron_sh/get_inventory_total_volume.sh',
        ssh_hook=sshHook
    )

    # 获取库存总价值
    get_inventory_total_price_task = SSHOperator(
        task_id='get_inventory_total_price',
        command='wms_api_cron_sh/get_inventory_total_price.sh',
        ssh_hook=sshHook
    )

    # 获取DPD追踪信息
    get_dpd_tracking_info = SSHOperator(
        task_id='get_dpd_tracking_info',
        command='wms_api_cron_sh/get_dpd_tracking_info.sh',
        ssh_hook=sshHook
    )

    # 计算运单时效
    get_express_bill_tempo = SSHOperator(
        task_id='get_express_bill_tempo',
        command='wms_api_cron_sh/get_express_bill_tempo.sh',
        ssh_hook=sshHook
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='{{ ds }}库存总体积数/库存总价值/DPD追踪信息/运单时效批处理已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    [get_inventory_total_volume_task, get_inventory_total_price_task, get_dpd_tracking_info >> get_express_bill_tempo] >> email_task
