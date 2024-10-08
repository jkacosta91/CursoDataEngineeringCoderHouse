import os
import logging
from modules.data_con import DataConn
from modules.get_data_from_api import DataRetriever
from dotenv import load_dotenv

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

    schema:str = "jkacosta91_coderhouse"
    table:str = "anime"

    data_con = DataConn(user_credentials, schema)
    data_retriever = DataRetriever()  

    try:
        data = data_retriever.get_data(page=1, limit=10)  
        data_con.upload_data(data, table)
        logging.info(f"Data uploaded to -> {schema}.{table}")

    except Exception as e:
        logging.error(f"Not able to upload data\n{e}")

    finally:
        data_con.close_conn()

if __name__ == "__main__":
    main()