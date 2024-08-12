import requests
import pandas as pd
import logging
import time
from io import StringIO

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s :: GetDataModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

class DataRetriever:
    def __init__(self, user:str = "jkacosta91", repos:str = "repos" ) -> None:
        self.endpoint: str = "https://api.jikan.moe/v4/anime"

    def get_data(self, page: int = 1, limit: int = 25):
        params = {
            'page': page,
            'limit': limit
        }

        try:
            response = requests.get(self.endpoint, params=params)
            response.raise_for_status()
            response_json = response.json()

            if 'data' in response_json:
                data_by_list_api = pd.DataFrame(response_json['data'])

                # columnas necesarias para la ingestión en las tablas
                cols = ["mal_id", "url", "approved", "title","title_english", 
                        "title_japanese", "type", "source", "episodes","status", "airing", 
                        "duration", "rating", "score", "scored_by", "rank", "popularity", "members", "favorites", 
                        "synopsis", "background", "season", "year"]
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