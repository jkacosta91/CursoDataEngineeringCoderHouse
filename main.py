import os
import logging
from modules.data_conn import DataConn # type: ignore
from modules.data_retriever import DataRetriever # type: ignore
from dotenv import load_dotenv # type: ignore

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s :: MainModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

load_dotenv()

def main():
    user_credentials = {
        "REDSHIFT_USERNAME": os.getenv('REDSHIFT_USERNAME'),
        "REDSHIFT_PASSWORD": os.getenv('REDSHIFT_PASSWORD'),
        "REDSHIFT_HOST": os.getenv('REDSHIFT_HOST'),
        "REDSHIFT_PORT": os.getenv('REDSHIFT_PORT', '5439'),
        "REDSHIFT_DBNAME": os.getenv('REDSHIFT_DBNAME')
    }

    schema = "jkacosta91_coderhouse"
    table = "Marvel_Characters"

    data_conn = DataConn(user_credentials, schema)
    data_retriever = DataRetriever(
        public_key=os.getenv('MARVEL_PUBLIC_KEY'),
        private_key=os.getenv('MARVEL_PRIVATE_KEY')
    )

    try:
        data = data_retriever.get_data()
        data_conn.upload_data(data, table)
        logging.info(f"Data uploaded to -> {schema}.{table}")

    except Exception as e:
        logging.error(f"Not able to upload data\n{e}")

    finally:
        data_conn.close_conn()

if __name__ == "__main__":
    main()