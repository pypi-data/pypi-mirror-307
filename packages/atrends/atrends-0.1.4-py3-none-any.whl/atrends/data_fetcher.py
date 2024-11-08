from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
import requests
import logging
import time

class GoogleTrendsFetcher:
    def __init__(self, hl='en_US', tz=360):
        self.pytrends = TrendReq(hl=hl, tz=tz, timeout=(10, 25))  # adding connect and read timeout

    def fetch_interest_over_time(self, keywords, timeframe, geo='', category=0, max_retries=3):
        try:
            self.pytrends.build_payload(keywords, timeframe=timeframe, geo=geo, cat=category)
            return self.pytrends.interest_over_time()
        except ResponseError as e:
            logging.error(f"Pytrends response error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error during Pytrends request: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def fetch_with_retries(self, keywords, timeframe, geo='', category=0, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            data = self.fetch_interest_over_time(keywords, timeframe, geo, category)
            if data is not None and not data.empty:
                return data
            logging.warning(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        
        logging.error("Max retries reached. Failed to fetch data from Pytrends.")
        return None
