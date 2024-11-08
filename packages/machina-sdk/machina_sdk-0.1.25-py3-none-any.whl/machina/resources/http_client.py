import requests
import json


class HttpClient:

    def __init__(self, api_key: str):

        self.api = "http://127.0.0.1:5000"

        self.headers = {
            "X-Api-Token": api_key,
            "Content-Type": "application/json"
        }


    def __parse_response(self, content):
        # Decode and parse the JSON content
        return json.loads(content.decode('utf-8'))


    def get(self, url):

        try:
            response = requests.get(f"{self.api}/{url}", headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses

            # Debug information
            print(f"Connection: {response.connection}")
            print(f"Headers: {response.headers}")
            print(f"Status Code: {response.status_code}")
            print(f"Content: {response.content}")

            return self.__parse_response(response.content)  # Decode and parse

        except requests.RequestException as e:
            print(f"HTTP error occurred: {e}")
            return {}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def post(self, url, data):
        try:
            response = requests.post(f"{self.api}/{url}", data, headers=self.headers)
            print(response)
            return self.__parse_response(response.content)
        except Exception as e:
            print("Exception", e)
            return {}


    def put(self, url, data):
        try:
            response = requests.put(f"{self.api}/{url}", data, headers=self.headers)
            print(response)
            return self.__parse_response(response.content)
        except Exception as e:
            print("Exception", e)
            return {}


    def delete(self, url):
        try:
            response = requests.delete(f"{self.api}/{url}", headers=self.headers)
            print(response)
            return self.__parse_response(response.content)
        except Exception as e:
            print("Exception", e)
            return {}
