from modules.config import EMAIL
from airflow.utils.email import send_email


# Funcion de monitoreo mediante el envio de mails
def handle_dag_status(context):
    # Determina si el DAG falló o tuvo éxito
    exception = context.get('exception', None)
    
    if exception:
        # Contenido del mail en formato HTML
        asunto = f"DAG {context['dag'].dag_id} ha fallado"
        cuerpo = (
            f"<p>El DAG {context['dag'].dag_id} falló en la ejecución {context['execution_date']}.</p>"
            f"<p>Tarea fallida: {context['task_instance'].task_id}</p>"
            f"<p>Error: {exception}</p>"
            f"<p>Log URL: <a href='{context['task_instance'].log_url}'>{context['task_instance'].log_url}</a></p>"
            f"<p>Fecha de ejecución: {context['execution_date']}</p>"
            f"<p>Estado actual: {context['task_instance'].state}</p>"
        )
        email_notification(email=EMAIL, asunto=asunto, cuerpo=cuerpo)
        
    elif context['task_instance'].task_id == 'cleanup_tmp_files':
        # Contenido del mail en formato HTML
        asunto = f"DAG {context['dag'].dag_id} ha completado con éxito"
        cuerpo = (
            f"<p>El DAG {context['dag'].dag_id} completó con éxito la ejecución {context['execution_date']}.</p>"
            f"<p>Fecha de ejecución: {context['execution_date']}</p>"
            f"<p>Estado final del DAG: {context['task_instance'].state}</p>"
        )
        email_notification(email=EMAIL, asunto=asunto, cuerpo=cuerpo)

def email_notification(email, asunto, cuerpo):    
    send_email(
        to=email,
        subject=asunto,
        html_content=cuerpo
    )