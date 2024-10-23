import requests
import logging

logger = logging.getLogger(__name__)

class Api:
    def noResponse(self, url):
        try:
            r = requests.get(url, timeout=5)
            return False
        except requests.exceptions.RequestException as e:
            logger.debug(f"API not responding at {url}: {e}")
            return True