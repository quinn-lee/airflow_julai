from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import requests
import xlsxwriter
import os

default_args = {
    'owner': 'julai_bi',
    'email': ['levine.li@quaie.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=120),
}


def get_jd_data():
    end_date = days_ago(1).strftime("%F")
    print(end_date)
    url = "https://api.nordlicht-fba.com/api/v1.0/statistics/jd_dpd_express_bills?end_date={}"\
        .format(end_date)
    resp = requests.get(url)
    res_data = resp.json().get('data')
    return [res_data.get('num'), end_date]


# 出库时效统计
with DAG(
    dag_id='jd_api_mail',
    default_args=default_args,
    schedule_interval='5 0 * * *',  # UTC时间每天0点5分跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=360),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:
    jd_api_data_task = PythonOperator(
        task_id="jd_api_data",
        python_callable=get_jd_data
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='ext.zhangzhuangyi1@jd.com',
        cc='service@nordlicht.cn',
        subject="""{{task_instance.xcom_pull(task_ids='jd_api_data')[1]}} DPD出单统计""",
        html_content="""<h3>您好，{{task_instance.xcom_pull(task_ids='jd_api_data')[1]}} Nordlicht使用DPD API下单件数为：{{task_instance.xcom_pull(task_ids='jd_api_data')[0]}}。<h3>"""
    )

    jd_api_data_task >> email_task
