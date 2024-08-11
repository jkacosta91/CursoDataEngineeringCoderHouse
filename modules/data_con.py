import requests
import pandas as pd
import logging
import hashlib
import time
from io import StringIO

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s :: GetDataModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

class DataRetriever:
    def __init__(self, public_key: str, private_key: str) -> None:
        self.endpoint: str = "https://gateway.marvel.com/v1/public/characters"
        self.public_key: str = public_key
        self.private_key: str = private_key

    def get_data(self):
        ts = str(time.time())
        hash_string = ts + self.private_key + self.public_key
        hash_md5 = hashlib.md5(hash_string.encode('utf-8')).hexdigest()

        params = {
            'ts': ts,
            'apikey': self.public_key,
            'hash': hash_md5,
            'limit': 100
        }

        try:
            response = requests.get(self.endpoint, params=params)
            response.raise_for_status()
            response_json = response.json()

            if 'data' in response_json and 'results' in response_json['data']:
                data_by_list_api = pd.DataFrame(response_json['data']['results'])
                # columnas necesarias para la ingestión en las tablas
                cols = ["id", "name", "description", "modified", "resourceURI"]
                logging.info(f"{cols} -> to be inserted")
                data = data_by_list_api[cols]

                # Procesar y registrar la información de los datos
                buffer = StringIO()
                data.info(buf=buffer)
                s = buffer.getvalue()
                logging.info(s)
                logging.info("Data created")
                return data

            else:
                logging.error("Invalid response structure from API")
                return pd.DataFrame()

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise

        except Exception as e:
            logging.error(f"Not able to process the data from the API\n{e}")
            raise
