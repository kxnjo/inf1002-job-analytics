import re # regular expression library
import requests # requests library to make API code
import pandas as pd

API_KEY = 'AIzaSyDH6gfB_UlGeEtqXt7ZiHK7TdYydSTQWac'
SEARCH_ENGINE_ID = '718bdbf89bb93481f'

def build_payload(query, date_restrict = 'm1', **params):
    """
    :param query = Search term
    :date_restrict = Restricts results based on recency (default is 1 month, 'm1')

    :return = dictionary containing API request params
    """

    payload = {
        'key': API_KEY,
        'q': query,
        'cx': SEARCH_ENGINE_ID, 
        'date_restrict': date_restrict
    }

    payload.update(params)
    return payload

def make_request(payload):
    """
    function makes request to Google Search API and handle potential errors.

    :payload = dictionary containing request parameters
    :return = JSON response from Google Search API
    """

    response = requests.get("https://www.googleapis.com/customsearch/v1", params = payload)
    # check if there is any errors
    if response.status_code != 200:
        raise Exception('Request Failed')

    return response.json()

# example prints
response = make_request(build_payload('SIT Software Engineering'))
print(response["items"][0]["link"])