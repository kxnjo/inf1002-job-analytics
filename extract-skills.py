import requests
import json
import os
import dotenv
import pandas as pd
from datetime import datetime

# get environment variables (to store API credentials & token)
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def main():
    df = pd.read_csv("crawl.csv")
    df["Skills"] = df.apply(lambda row: extract_API(row["job-desc"]), axis=1)
    df.to_csv("out.csv")


def get_access_token():
    url = "https://auth.emsicloud.com/connect/token"
    payload = f"client_id={os.getenv('client_id')}&client_secret={os.getenv('client_secret')}&grant_type=client_credentials&scope=emsi_open"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)["access_token"]


def verify_token_validity():
    if not os.getenv("timestamp"):
        time_diff = 3600
    else:
        format_data = "%Y-%m-%d %H:%M:%S.%f"
        time_diff = (datetime.now() - datetime.strptime(os.getenv("timestamp"), format_data)).total_seconds()

    # auto-refresh: get new token if >3600
    if time_diff > 3600:
        token = get_access_token()
        dotenv.set_key(dotenv_file, "timestamp", str(datetime.now()))
        dotenv.set_key(dotenv_file, "token", token)
        return token
    
    return os.getenv("token")


def extract_API(raw_text):
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
    # print(response.headers) # to check rate limit

    # Extract skill names from data
    skill_names = []
    for i in data:
        skill_names.append(i["skill"]["name"])
    skill_string = ",".join(skill_names)
    print(skill_string)
    return skill_string
    

main()