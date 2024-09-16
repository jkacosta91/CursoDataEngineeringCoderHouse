import sys
import os

# Añade el directorio 'dags/modules' al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from modules.get_data_from_api import DataRetriever
from modules.data_con import DataConn
from modules import email_notification
import os


# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': email_notification.handle_dag_status,
    'on_success_callback': email_notification.handle_dag_status,
}

# Definición del DAG
with DAG(
    'ETL_JKACOSTA91',
    default_args=default_args,
    description='DAG para consumir API y vaciar datos en Redshif',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Definir las tareas
    task_1 = BashOperator(
        task_id='primera_tarea',
        bash_command='echo Iniciando...',
        dag=dag
    )

    task_2 = PythonOperator(
        task_id='get_data_from_api',
        python_callable=DataRetriever,
        provide_context=True,
        dag=dag
    )

    task_3 = PythonOperator(
        task_id='upload_data_to_redshift',
        python_callable=DataConn,
        provide_context=True,
        dag=dag
    )

    task_4 = BashOperator(
        task_id='proyecto_final',
        bash_command='echo Proceso completado...',
        dag=dag
    )

# Definir dependencias
task_1 >> task_2 >> task_3 >> task_4
