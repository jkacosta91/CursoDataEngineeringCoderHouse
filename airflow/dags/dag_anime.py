from datetime import datetime, timedelta
from email import message
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator


from modules import get_data_from_api, data_con

default_args={
    'owner': 'JKACOSTA',
    'retries': 5,
    'retry_delay': timedelta(minutes=2) # 2 min de espera antes de cualquier re intento
}

DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id="desafio3_pipeline",
    default_args= default_args,
    description="DAG para consumir API y vaciar datos en Redshift",
    start_date=datetime(2024,8,1),
    schedule_interval='@daily',
    catchup=False
    ) as dag:

    # Tasks
    # 1. 
    task_1 = BashOperator(
        task_id='primera_tarea',
        bash_command='echo Iniciando...'
        )
    
    # 2.
    task_2 = PythonOperator(
        task_id="get_data_from_api",
        python_callable=get_data_from_api
        )

    # 3. 
    task_3 = PythonOperator(
        task_id="data_con",
        python_callable=data_con
        )

    # 4. Loading
    task_4 = BashOperator(
        task_id= 'tercera_tarea',
        bash_command='echo Proceso completado...'
    )

    # Task dependencies
    task_1 >> task_2 >> task_3 >> task_4