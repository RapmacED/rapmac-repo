from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner':'Dataship',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}

with DAG (
    dag_id='our_first_dag_v2',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2023, 1, 16, 18, 21), #start date is 17/01/2023 at 2am
    schedule_interval='@hourly'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo Hello world, this is the first task'
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo Hey, I am the second task'
    )

    task1.set_downstream(task2)