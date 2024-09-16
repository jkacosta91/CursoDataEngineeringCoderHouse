from dotenv import load_dotenv
import os

# Cargar el archivo de variables de entorno personalizado .env.dag
load_dotenv(dotenv_path='.env.dag')

# Variables de entorno:
REDSHIFT_USER = os.getenv('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_DB = os.getenv('REDSHIFT_DB')
REDSHIFT_SCHEMA = os.getenv('REDSHIFT_SCHEMA')
TWELVE_DATA_API_KEY = os.getenv('TWELVE_DATA_API_KEY')
EMAIL = os.getenv('EMAIL')

# URL de la api
URL = os.getenv('URL')
