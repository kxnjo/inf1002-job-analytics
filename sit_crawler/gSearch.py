import re # regular expression library
import requests # requests library to make API code
import pandas as pd

API_KEY = 'AIzaSyDH6gfB_UlGeEtqXt7ZiHK7TdYydSTQWac'
SEARCH_ENGINE_ID = '718bdbf89bb93481f'

def build_payload(query, **params):
    """
    :param query = Search term
    :date_restrict = Restricts results based on recency (default is 1 month, 'm1')

    :return = dictionary containing API request params
    """

    payload = {
        'key': API_KEY,
        'q': query,
        'cx': SEARCH_ENGINE_ID
    }

    payload.update(params)
    return payload

def make_request(search, school):
    """
    function makes request to Google Search API and handle potential errors.

    :payload = dictionary containing request parameters
    :return = JSON response from Google Search API
    """
    payload = build_payload(f'{search} {school}')

    response = requests.get("https://www.googleapis.com/customsearch/v1", params = payload)
    # check if there is any errors
    if response.status_code != 200:
        raise Exception('Request Failed')

    return response.json()

def find_course(courseName, school = "Singapore Institute of Technology"):
    """
    function searches and URL for COURSE result that's of most relevance to use case (SIT students)

    :response = search listing object in JSON
    :return = URL for specified search
    """
    
     # build the payload
    response = make_request(courseName, school) # get list of google search responses in JSON

    # check if the response is working well
    if response["items"]:
        itemsResponse = response["items"].copy()
    else:
        return "search not found"

    # filter for school search (make sure that it is the right school)
    for item in itemsResponse:
        resultList = [item["title"], item["displayLink"], item["snippet"]]
        print("\n\n this is result list")
        print(resultList)
        for x in resultList:
            # find school name (likely that link is related to the school)
            if school in x or courseName in x:
                return item["link"]

    
    return "link not found"

def find_module(moduleName, school = "Singapore Institute of Technology"):
    """
    function searches and URL for MODULE result that's of most relevance to use case (SIT students)

    :response = search listing object in JSON
    :return = URL for specified search
    """
    moduleURL = "https://www.singaporetech.edu.sg/modules/"

     # build the payload
    response = make_request(f'{moduleName} module', school) # get dictionary of google search responses in JSON

    # check if the response is working well
    if response["items"]:
        itemsResponse = response["items"].copy()
    else:
        return "search not found"

    # filter for school search (make sure that it is the right school)
    for item in itemsResponse:
        if moduleURL in item["link"]:
            return item["link"]
    return "module link not found"


# example search
# print(find_course("software engineering"))
print(find_module("programming fundamentals"))