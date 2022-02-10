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


def get_api_data():
    start_date = days_ago(7).strftime("%F")
    end_date = days_ago(1).strftime("%F")
    print(start_date)
    print(end_date)
    url = "https://api.nordlicht-fba.com/api/v1.0/statistics/david_dpd_express_bills?start_date={}&end_date={}"\
        .format(start_date, end_date)
    resp = requests.get(url)
    res_data = resp.json().get('data')
    # 创建工作簿
    filename = "{}/dags/david_api_files/{}~{}出单明细.xlsx".format(os.getenv("AIRFLOW_HOME"), start_date, end_date)
    workbook = xlsxwriter.Workbook(filename)
    sh = workbook.add_worksheet('明细')
    sh.set_column('A:A', 20)
    sh.set_column('B:B', 15)
    sh.set_column('C:C', 5)
    sh.set_column('D:D', 5)
    fmt1 = workbook.add_format()
    fmt2 = workbook.add_format()
    # 字体加粗
    fmt1.set_bold(True)
    # 设置左对齐
    fmt2.set_align('left')
    sh.write_row('A1', ['包裹单号', '打单日期', '国家', '邮编'], fmt1)
    i = 2
    for express_bill in res_data.get('express_bills'):
        sh.write_row("A{}".format(i), express_bill, fmt2)
        i += 1
    workbook.close()
    return [res_data.get('de_num'), res_data.get('not_de_num'), filename, start_date, end_date]


# 出库时效统计
with DAG(
    dag_id='david_api_mail',
    default_args=default_args,
    schedule_interval='0 4 * * 5',  # UTC时间每周五4点跑
    start_date=days_ago(0),
    dagrun_timeout=timedelta(minutes=360),
    catchup=False,
    max_active_runs=1,  # 每次只能有一个dagrun
) as dag:
    david_api_data_task = PythonOperator(
        task_id="david_api_data",
        python_callable=get_api_data
    )

    # 批处理正常结束后发送邮件
    email_task = EmailOperator(
        task_id='send_email',
        to='david@amsma.nl, nordlicht@novalinks.cn, tim.mao@novalinks.cn',
        subject="""{{task_instance.xcom_pull(task_ids='david_api_data')[3]}} ~ 
        {{task_instance.xcom_pull(task_ids='david_api_data')[4]}} NORDLICHT DPD出单统计""",
        html_content="""<h3>从{{task_instance.xcom_pull(task_ids='david_api_data')[3]}} 到 
        {{task_instance.xcom_pull(task_ids='david_api_data')[4]}},
        德国总件数： {{task_instance.xcom_pull(task_ids='david_api_data')[0]}},
        其它国家总件数： {{task_instance.xcom_pull(task_ids='david_api_data')[1]}}<h3>""",
        files=["{{task_instance.xcom_pull(task_ids='david_api_data')[2]}}"]
    )

    david_api_data_task >> email_task
