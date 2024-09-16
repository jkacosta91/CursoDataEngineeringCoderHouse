# Curso Data_Engineer_CoderHouse entrega final

Para arrancar el proyecto escribir en la terminal

  ```bash
    docker-compose up
  ```

## Descripción del Proyecto

Este proyecto de ingeniería de datos está diseñado para extraer, transformar y cargar datos desde una API hacia una base de datos Redshift utilizando Apache Airflow.

### Funcionamiento del Proyecto

1. **Extracción de Datos**: Los datos se extraen desde la API de "Jikan API".

2. **Transformación de Datos**: Los datos extraídos no seran transformados ya que los mismos son proporcionados por la API de manera que puedan ser utilizados correctamente.

3. **Carga de Datos**: Los datos se cargan en una base de datos Redshift. .

4. **Orquestación con Apache Airflow**:
   - **Configuración**: El proyecto utiliza Apache Airflow para gestionar el flujo de trabajo ETL. Este está configurado para ejecutar el proceso diariamente.
   - **Ejecución**: Para probar el funcionamiento del DAG, debes acceder a la interfaz de usuario de Apache Airflow con las credenciales predeterminadas (usuario: `airflow`, contraseña: `airflow`). Desde allí, puedes activar manualmente el DAG para verificar su funcionamiento.

## Estructura del Proyecto

1. **`dags/`**
   - **`dag_anime.py`**: Define el DAG (Directed Acyclic Graph) para Apache Airflow que orquesta el proceso ETL. Utiliza el operador `PythonOperator` para ejecutar la función `etl()` del módulo `main.py` en un intervalo diario.

2. **`modules/`**
   - **`get_data_from_api.py`**: Contiene la función `extract_data()`, que extrae datos financieros desde la API de Twelve Data y los organiza en un DataFrame de Pandas. Limita la cantidad de registros a los más recientes y maneja errores de extracción.
   - **`main.py`**: Define la función `etl()`, que ejecuta el proceso ETL completo: extracción de datos, transformación y carga. También incluye una línea comentada para probar el proceso ETL manualmente.
   - **`data_con.py`**: Contiene la función `connect_redshift()` para manejar la conexión a la base de datos Redshift utilizando `psycopg2`.
   - **`email_notification.py`**: Este archivo gestiona el envío de correos electrónicos para notificar el estado del DAG en Airflow. Aquí se detallan sus componentes:

3. **`dependencies/`**
   - **`requirements.txt`**: Lista las dependencias necesarias para el proyecto, como `pandas`, `requests`, `psycopg2`, y `apache-airflow`.

4. **`docker-compose.yml`**: Configura los servicios necesarios para el proyecto, incluyendo la base de datos y el entorno de Airflow, utilizando Docker Compose.

5. **`.gitignore`**: Especifica los archivos y directorios que deben ser ignorados por Git, como el entorno virtual y archivos temporales.

6. **`README.md`**: Documento que proporciona una visión general del proyecto, incluyendo instrucciones de uso y detalles de configuración.

## Funciones y tareas del DAG

El DAG `curso_data_engineering` automatiza un proceso ETL (Extracción, Transformación y Carga) de datos financieros ejecutandolo diariamente.

### Sistema de Alertas

El DAG cuenta con un sistema de alertas configurado para notificar el estado del proceso. Utiliza el archivo `email_notification.py` para gestionar el envío de correos electrónicos. Este sistema proporciona:

- **Alertas en caso de fallo**: Si alguna tarea del DAG falla, se envía un correo electrónico con detalles del error, incluyendo el asunto del mensaje, el cuerpo del correo (que incluye información del error y un enlace al log), y la fecha de ejecución.
- **Confirmaciones de éxito**: Al completar correctamente todas las tareas, se envía un correo de confirmación indicando que el DAG se ejecutó con éxito. Estos mensajes son editables y configurables a través del archivo `email_notification.py`.

### Resumen de Tareas

- **Extracción de Datos** (`get_data_from_api`): Extrae los datos y los organiza en un DataFrame.
- **Carga de Datos** (`upload_data_to_redshift`): Carga el DataFrame transformado en Redshift.

Este enfoque garantiza una ejecución fluida del proceso ETL y una gestión efectiva de errores y archivos temporales.`

## Dependencias

Las tareas están organizadas de manera que:

- La extracción de datos ocurre primero.
- La verificación del archivo de extracción sigue a la extracción de datos.
- La transformación de datos ocurre después de la verificación del archivo de extracción.
- La verificación del archivo transformado sigue a la transformación de datos.
- La carga de datos ocurre después de la verificación del archivo transformado.
- Finalmente, se realiza la limpieza de archivos temporales después de la carga de datos.

## Configuración local del proyecto

1. **Clona el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. **Crea un entorno virtual y actívalo**

   - **Crea un entorno virtual:**

     ```bash
     python -m venv venv
     ```

   - **Activa el entorno virtual:**

     - En Windows:

       ```bash
       venv\Scripts\activate
       ```

     - En macOS y Linux:

       ```bash
       source venv/bin/activate
       ```

3. **Instala las dependencias**

    ```bash
    pip install -r dependencies/requirements.txt
    ```

4. **Configura el archivo `.env`**

    Asegúrate de que el archivo `.env` esté correctamente renombrado (elimina el guion bajo `_` del nombre del archivo), llena estas variables con la información requerida, como las credenciales de conexión a Redshift y otras configuraciones pertinentes, dentro del archivo `.env`.

5. **Ejecuta el proyectos**

    ```bash
    docker-compose up
    ```

## Configuración en GitHub Codespaces del proyecto

1. **Abre el repositorio en GitHub Codespaces

    Haz clic en el botón Code y selecciona Open with Codespaces.
    Crea un nuevo Codespace.

2. **Configura el archivo `.env`**

    Asegúrate de que el archivo `.env` esté correctamente renombrado (elimina el guion bajo `_` del nombre del archivo), llena estas variables con la información requerida, como las credenciales de conexión a Redshift y otras configuraciones pertinentes, dentro del archivo `.env`.

3. **Ejecuta el proyecto**

    Ejecuta el siguiente comando en la terminal integrada de Codespaces:

    ```bash
    docker-comnpose up
    ```
