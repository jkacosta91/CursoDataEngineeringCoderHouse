from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from modules.get_data_from_api import DataRetriever
from modules.data_con import DataConn
import os

# Cargar las variables de entorno
config = {
    'REDSHIFT_USERNAME': os.getenv('REDSHIFT_USERNAME'),
    'REDSHIFT_PASSWORD': os.getenv('REDSHIFT_PASSWORD'),
    'REDSHIFT_HOST': os.getenv('REDSHIFT_HOST'),
    'REDSHIFT_PORT': os.getenv('REDSHIFT_PORT', '5439'),
    'REDSHIFT_DBNAME': os.getenv('REDSHIFT_DBNAME')
}

# Definir argumentos por defecto
default_args = {
    'owner': 'jkacosta91',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': email_notification.handle_dag_status,
    'on_success_callback': email_notification.handle_dag_status,
}

# Crear el DAG
dag = DAG(
    dag_id="curso_data_engineering",
    default_args=default_args,
    description="DAG para consumir API y vaciar datos en Redshift",
    start_date=datetime(2024, 8, 1),
    schedule_interval='@daily',
    catchup=False
)

def retrieve_data():
    retriever = DataRetriever()
    data = retriever.get_data(page=1, limit=25)
    return data

def upload_data(**context):
    data = context['ti'].xcom_pull(task_ids='get_data_from_api')
    if not data.empty:
        schema = os.getenv('REDSHIFT_SCHEMA')
        table = os.getenv('REDSHIFT_TABLE')
        conn = DataConn(config=config, schema=schema)
        conn.upload_data(data, table)

# Definir las tareas
task_1 = BashOperator(
    task_id='primera_tarea',
    bash_command='echo Iniciando...',
    dag=dag
)

task_2 = PythonOperator(
    task_id='get_data_from_api',
    python_callable=retrieve_data,
    provide_context=True,
    dag=dag
)

task_3 = PythonOperator(
    task_id='upload_data_to_redshift',
    python_callable=upload_data,
    provide_context=True,
    dag=dag
)

task_4 = BashOperator(
    task_id='tercera_tarea',
    bash_command='echo Proceso completado...',
    dag=dag
)

# Definir dependencias
task_1 >> task_2 >> task_3 >> task_4