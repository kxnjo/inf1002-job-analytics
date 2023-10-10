import requests
import json
import pandas as pd
from datetime import datetime
import dotenv
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


# Read the crawled csv file containing the job description
def main():
    # Get the list of all files crawled using directory
    path = "cleaned_data/non_extracted/"
    non_extracted_file = os.listdir(path)

    # printing the list using loop
    for x in range(len(non_extracted_file)):
        # To read csv file crawled
        df = pd.read_csv(path+non_extracted_file[x])

        # To extract Skills for each job crawled
        df["Extracted Skills"] = df.apply(lambda row: extract_api(row["Job description"]), axis=1)

        # Append skills extracted from description
        df.to_csv("cleaned_data/extracted/title_skill/appended_skill_" + non_extracted_file[x])

        # Separate all skill into single row
        df["Skills"] = df["Skills"].str.split(',')
        data = df["Skills"].explode('Skills')

        # Count Repeated Skills & Remove Duplicates
        df = pd.DataFrame(data, columns=['Skills'])
        unique_skills = df.pivot_table(columns=['Skills'], aggfunc='size')

        # Csv file of Skills & Count without duplicates
        unique_skills.to_csv("cleaned_data/extracted/skills/skills_" + non_extracted_file[x])

        print(non_extracted_file[x])


# Access environment variables ti access the skills api
def get_access_token():
    url = "https://auth.emsicloud.com/connect/token"
    payload = f"client_id={os.getenv('Client_ID')}&client_secret={os.getenv('Secret')}&grant_type=client_credentials&scope=emsi_open"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)["access_token"]


# To ensure token is not expired and valid to use (Authorization)
def verify_token_validity():
    if not os.getenv("Timestamp"):
        time_diff = 3600
    else:
        format_data = "%Y-%m-%d %H:%M:%S.%f"
        time_diff = (datetime.now() - datetime.strptime(os.getenv("timestamp"), format_data)).total_seconds()

    # auto-refresh: get new token if >3600
    if time_diff > 3600:
        token = get_access_token()
        dotenv.set_key('.env', "Timestamp", str(datetime.now()))
        dotenv.set_key('.env', "Token", token)
        return token

    return os.getenv("Token")


# Extract the api from the descriptions in csv using the api
def extract_api(raw_text):
    # configs (https://docs.lightcast.dev/apis/skills#versions-version-extract)
    access_token = verify_token_validity()
    querystring = {"language":"en"}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Extract data from API
    payload = json.dumps({"text":raw_text})
    url = "https://emsiservices.com/skills/versions/latest/extract"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    data = json.loads(response.text)["data"]

    # Extract skill names from data
    skill_names = []
    for i in data:
        skill_names.append(i["skill"]["name"])
    skill_string = ",".join(skill_names)

    return skill_string


main()
