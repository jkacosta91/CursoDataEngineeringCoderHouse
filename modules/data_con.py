import pandas as pd
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError, InterfaceError

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s :: DataConnectionModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

class DataConn:
    def __init__(self, config: dict, schema: str):
        self.config = config
        self.schema = schema
        self.db_engine = None

    def get_conn(self):
        if self.db_engine is not None:
            logging.info("Connection already exists. Reusing the existing connection.")
            return

        username = self.config.get('REDSHIFT_USERNAME')
        password = self.config.get('REDSHIFT_PASSWORD')
        host = self.config.get('REDSHIFT_HOST')
        port = self.config.get('REDSHIFT_PORT', '5439')
        dbname = self.config.get('REDSHIFT_DBNAME')

        # Construir la URL de conexión
        connection_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
        self.db_engine = create_engine(connection_url, pool_pre_ping=True)  # pool_pre_ping para comprobar la conexión

        try:
            with self.db_engine.connect() as connection:
                result = connection.execute('SELECT 1;')
                if result:
                    logging.info("Connection to Redshift created successfully.")
        except (SQLAlchemyError, OperationalError, InterfaceError) as e:
            logging.error(f"Failed to create connection: {e}")
            self.db_engine = None  # Reset the engine if connection fails
            raise

    def check_table_exists(self, table_name: str) -> bool:
        self.get_conn()  # Ensure the connection is established

        try:
            with self.db_engine.connect() as connection:
                query_checker = f"""
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = '{self.schema}'
                    AND table_name = '{table_name}';
                """
                result = connection.execute(query_checker).fetchone()

                if not result:
                    logging.error(f"Table {table_name} does not exist in schema {self.schema}.")
                    raise ValueError(f"Table {table_name} does not exist in schema {self.schema}.")
                
                logging.info(f"Table {table_name} exists in schema {self.schema}.")
                return True

        except (SQLAlchemyError, OperationalError, InterfaceError) as e:
            logging.error(f"Failed to check if table {table_name} exists: {e}")
            raise

    def upload_data(self, data: pd.DataFrame, table: str):
        self.get_conn()  # Ensure the connection is established

        # Verify if the table exists before uploading data
        if not self.check_table_exists(table):
            logging.error(f"Cannot upload data because the table {table} does not exist in schema {self.schema}.")
            raise ValueError(f"Table {table} does not exist in schema {self.schema}.")

        try:
            data.to_sql(
                table,
                con=self.db_engine,
                schema=self.schema,
                if_exists='append',
                index=False,
                chunksize=5000,  # Define el tamaño de los lotes para evitar problemas de memoria
                method='multi'  # Optimiza la inserción para grandes volúmenes de datos
            )

            logging.info(f"Data from DataFrame has been uploaded to {self.schema}.{table} in Redshift.")
        except (SQLAlchemyError, OperationalError, InterfaceError) as e:
            logging.error(f"Failed to upload data to {self.schema}.{table}:\n{e}")
            raise

    def close_conn(self):
        if self.db_engine:
            self.db_engine.dispose()
            logging.info("Connection to Redshift closed.")
        else:
            logging.warning("No active connection to close.")