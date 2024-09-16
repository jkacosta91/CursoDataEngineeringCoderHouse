import sys
import os

# Añade el directorio 'dags/modules' al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from modules import get_data_from_api
from modules import data_con
from modules import email_notification
import os


# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 15),  # Utiliza una fecha fija para evitar problemas con `datetime.now()`
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': email_notification.handle_dag_status,
    'on_success_callback': email_notification.handle_dag_status,
}

# Definición del DAG
with DAG(
    'ETL_JKACOSTA91',
    default_args=default_args,
    description='DAG para consumir API y vaciar datos en Redshift',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Define la función a llamar para extraer datos
    def extraer_datos():
        data_retriever = get_data_from_api.DataRetriever()
        return data_retriever.get_data()

    # Define la función a llamar para cargar datos
    def cargar_datos(ti):
        data = ti.xcom_pull(task_ids='extraer_datos')
        config = {
            'REDSHIFT_USERNAME': os.getenv('REDSHIFT_USER'),
            'REDSHIFT_PASSWORD': os.getenv('REDSHIFT_PASSWORD'),
            'REDSHIFT_HOST': os.getenv('REDSHIFT_HOST'),
            'REDSHIFT_PORT': os.getenv('REDSHIFT_PORT'),
            'REDSHIFT_DBNAME': os.getenv('REDSHIFT_DBNAME')
        }
        data_conn = data_con.DataConn(config=config, schema=os.getenv('REDSHIFT_SCHEMA'))
        data_conn.upload_data(data, 'jkacosta91_coderhouse')

    # Definir las tareas
    task_1 = BashOperator(
        task_id='primera_tarea',
        bash_command='echo Iniciando...',
        dag=dag
    )

    task_2 = PythonOperator(
        task_id='extraer_datos',
        python_callable=extraer_datos,
        dag=dag
    )

    task_3 = PythonOperator(
        task_id='cargar_datos',
        python_callable=cargar_datos,
        dag=dag
    )

    task_4 = BashOperator(
        task_id='proyecto_final',
        bash_command='echo Proceso completado...',
        dag=dag
    )

    # Definir dependencias
    task_1 >> task_2 >> task_3 >> task_4
