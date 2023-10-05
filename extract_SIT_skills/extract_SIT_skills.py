import os
import json
import pandas as pd
import requests
from datetime import datetime

print('Start time is', datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

directory = 'sit_crawler\data'
for file in os.listdir(directory):
    print(file)
    with open(os.path.join(directory, file), encoding="utf8") as f:

        skill_names = []
        
        #reading module desciptions from csv
        dataDesc = pd.read_csv(f)

        #extracting description only, removing empty rows
        descList = dataDesc.dropna(axis=0)['Description'].tolist()

        #connecting to lightcast API
        url = "https://auth.emsicloud.com/connect/token"
        payload = "client_id=yzksqh2fhcdas5d3&client_secret=1Ol9MEkB&grant_type=client_credentials&scope=emsi_open"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, data=payload, headers=headers)
        access_token = json.loads(response.text)['access_token']

        url = "https://emsiservices.com/skills/status"
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.request("GET", url, headers=headers)

        # using skillsapi to extract skills
        url = "https://emsiservices.com/skills/versions/latest/extract"
        querystring = {"language":"en"}
        headers = {
            'Authorization': "Bearer " + access_token,
            'Content-Type': "text/plain"
            }

        # going through description list to extract skills
        for desc in descList:
            payload = '{ \"text\": \"' + desc + '\", \"confidenceThreshold\": 1.0 }'
            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

            result = json.loads(response.text)["data"]
            
            # stores skills extracted into list
            for i in result:
                skill_names.append(i["skill"]["name"])

        # storing skills in dataframe
        results_df = pd.DataFrame(skill_names, columns = ['Skills'])

        #counting skills in dataframe
        results_df = results_df.groupby(['Skills'])['Skills'].count().reset_index(name='Count')

        #output skills and count as csv
        isExist = os.path.exists('extract_SIT_skills\data')
        if not isExist:
            os.makedirs('extract_SIT_skills\data')
            
        results_df.to_csv('extract_SIT_skills/data/'+(file.split('.')[0])+'_Module_Description_Skills.csv', index = False)

print('End time is', datetime.now().strftime("%d-%m-%Y %H:%M:%S"))