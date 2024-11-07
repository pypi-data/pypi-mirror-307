from gemnify_sdk.scripts.logging import getLogger
import requests

class HTTP:
    def __init__(self, config) -> None:
        self.url = config.url
        self.logger = getLogger(config)

    def post(self, function, payload):
        response = requests.post(self.url + function, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["resp"]
        else:
            self.logger.error(f"Request failed with status code {response.status_code}, {response.text}")