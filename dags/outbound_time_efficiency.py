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
    dag_id='outbound_time_efficiency',
    default_args=default_args,
    schedule_interval='5 0 * * 1',  # UTC时间每周一0点5分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:

    # 统计15天内的出单
    waybill_statistics_task = SSHOperator(
        task_id='waybill_statistics',
        command='outbound_time_efficiency_sh/waybill_statistics.sh',
        ssh_hook=sshHook
    )

    # 统计15天内的出库
    outbound_statistics_task = SSHOperator(
        task_id='outbound_statistics',
        command='outbound_time_efficiency_sh/outbound_statistics.sh',
        ssh_hook=sshHook
    )

    # 生成plotly.html文件
    gen_plotly_task = SSHOperator(
        task_id='gen_plotly',
        command='outbound_time_efficiency_sh/gen_plotly.sh',
        ssh_hook=sshHook
    )

    # 同步plotly.html文件到客户端项目
    sftp_plotly_task = SSHOperator(
        task_id='sftp_plotly',
        command='outbound_time_efficiency_sh/sftp_plotly.sh',
        ssh_hook=sshHook
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='levine.li@quaie.com',
        subject='出库时效统计批处理已完成',
        html_content="""<h3>任务正常结束<h3>"""
    )

    [waybill_statistics_task, outbound_statistics_task] >> gen_plotly_task >> sftp_plotly_task >> email_task
