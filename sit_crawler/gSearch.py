import re  # regular expression library
import requests  # requests library to make API code
import pandas as pd
import json
from datetime import date


# = = = CUSTOM ERROR = = =
class GoogleSearchLimit(Exception):
    "You have hit the limit for the day. Try again tomorrow."
    pass


# = = = LOAD REQUEST COUNTER = = =
today = date.today()
data = {
    "api_key": "AIzaSyDH6gfB_UlGeEtqXt7ZiHK7TdYydSTQWac",
    "search_engine": "718bdbf89bb93481f",
    "date": {str(today): 0},
}
file_path = "./data/gSearch_counter.json"

try:
    with open(file_path, "r") as credentials:
        data = json.load(credentials)
        if data["date"][str(today)] is None:
            print(f"today's count does not exist!")
            update_count(0)

except FileNotFoundError:
    print("JSON file not found. Creating a new one.")
    # Writing to sample.json
    with open(file_path, "w") as credentials:
        credentials.write(json.dumps(data, indent=4))


def update_count(newCount):
    data["date"][str(today)] = newCount
    with open(file_path, "w") as credentials:
        credentials.write(json.dumps(data, indent=4))


# = = = GOOGLE SEARCHES REQUEST = = =
def build_payload(query, **params):
    """
    :param query = Search term
    :date_restrict = Restricts results based on recency (default is 1 month, 'm1')

    :return = dictionary containing API request params
    """

    payload = {"key": data["api_key"], "q": query, "cx": data["search_engine"]}

    payload.update(params)
    return payload


def make_request(search, school):
    """
    function makes request to Google Search API and handle potential errors.

    :payload = dictionary containing request parameters
    :return = JSON response from Google Search API
    """
    try:
        curr_counter = int(data["date"][str(today)])
        if curr_counter == 100:
            raise GoogleSearchLimit
        elif curr_counter == 50:
            print(
                f"\n WARNING = = = You have reached 50% of search limit for today. \n"
            )
        elif curr_counter >= 90:
            print(
                f"\n WARNING = = = You have reached {curr_counter}% of search limit for today. \n"
            )

        # add request count
        update_count(int(data["date"][str(today)]) + 1)

        payload = build_payload(f"{search} {school}")
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1", params=payload
        )
        # check if there is any errors
        if response.status_code != 200:
            raise Exception("Request Failed")

        return response.json()
    except GoogleSearchLimit:
        print("\nYou have hit the limit for the day. Try again tomorrow.\n\n")


def find_course(courseName, school="Singapore Institute of Technology"):
    """
    function searches and URL for COURSE result that's of most relevance to use case (SIT students)

    :response = search listing object in JSON
    :return = URL for specified search
    """

    # build the payload
    response = make_request(
        courseName, school
    )  # get list of google search responses in JSON

    # check if the response is working well
    if response["items"]:
        itemsResponse = response["items"].copy()
    else:
        return "search not found"

    # filter for school search (make sure that it is the right school)
    for item in itemsResponse:
        resultList = [item["title"], item["displayLink"], item["snippet"]]
        # print("\n\n this is result list")
        # print(resultList)
        for x in resultList:
            # find school name (likely that link is related to the school)
            if school in x or courseName in x:
                return item["link"]

    return "link not found"


def find_module(moduleName, school="Singapore Institute of Technology"):
    """
    function searches and URL for MODULE result that's of most relevance to use case (SIT students)

    :response = search listing object in JSON
    :return = URL for specified search
    """
    moduleURL = "https://www.singaporetech.edu.sg/modules/"

    # build the payload
    response = make_request(
        f"{moduleName} module", school
    )  # get dictionary of google search responses in JSON

    # check if the response is working well
    if response["items"]:
        itemsResponse = response["items"].copy()
    else:
        return None

    # filter for school search (make sure that it is the right school)
    for item in itemsResponse:
        if moduleURL in item["link"]:
            return item["link"]
    return None


# example search
print(find_course("software engineering"))
# print(find_module("programming fundamentals"))
