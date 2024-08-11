import pandas as pd
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

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
        username = self.config.get('REDSHIFT_USERNAME')
        password = self.config.get('REDSHIFT_PASSWORD')
        host = self.config.get('REDSHIFT_HOST')
        port = self.config.get('REDSHIFT_PORT', '5439')
        dbname = self.config.get('REDSHIFT_DBNAME')

        # Construir la URL de conexión
        connection_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
        self.db_engine = create_engine(connection_url)

        try:
            with self.db_engine.connect() as connection:
                result = connection.execute('SELECT 1;')
                if result:
                    logging.info("Connection created")
                    return
        except SQLAlchemyError as e:
            logging.error(f"Failed to create connection: {e}")
            raise

    def check_table_exists(self, table_name: str) -> bool:
        try:
            with self.db_engine.connect() as connection:
                query_checker = f"""
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = '{self.schema}'
                    AND table_name = '{Marvel_Characters}';
                """
                result = connection.execute(query_checker).fetchone()

                if not result:
                    logging.error(f"Table {table_name} does not exist in schema {self.schema}.")
                    raise ValueError(f"Table {table_name} does not exist in schema {self.schema}.")
                
                logging.info(f"Table {table_name} exists in schema {self.schema}.")
                return True

        except SQLAlchemyError as e:
            logging.error(f"Failed to check if table {table_name} exists: {e}")
            raise

    def upload_data(self, data: pd.DataFrame, table: str):
        if self.db_engine is None:
            logging.warning("Connection has not been established. Attempting to establish connection...")
            self.get_conn()

        try:
            data.to_sql(
                table,
                con=self.db_engine,
                schema=self.schema,
                if_exists='append',
                index=False
            )

            logging.info(f"Data from DataFrame has been uploaded to {self.schema}.{table} in Redshift.")
        except SQLAlchemyError as e:
            logging.error(f"Failed to upload data to {self.schema}.{table}:\n{e}")
            raise

    def close_conn(self):
        if self.db_engine:
            self.db_engine.dispose()
            logging.info("Connection to Redshift closed.")
        else:
            logging.warning("No active connection to close.")