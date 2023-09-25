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

def find_module(search, school = "SIT"):
    """
    function searches and URL for result that's of most relevance to use case (SIT students)

    :response = search listing object in JSON
    :return = URL for specified search
    """
    
    payload = build_payload(f'{search} {school}') # build the payload
    response = make_request(payload) # get list of google search responses in JSON

    # check if the response is working well
    if response["items"]:
        itemsResponse = response["items"].copy()
    else:
        return "search not found"

    # filter for school search (make sure that it is the right school)
    for item in itemsResponse:
        resultList = [item["title"], item["displayLink"], item["snippet"]]
        for x in resultList:
            if school in x:
                return item["link"]
    
    return "link not found"


# example search
print(find_module("software engineering"))