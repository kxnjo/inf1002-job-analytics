from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

#TODO: change this hardcoded value to use all data files in certain filepath instead
filepaths = ["Information and Communications Technology (Information Security).csv", "Information and Communications Technology (Software Engineering).csv"]

def main():
    for filepath in filepaths:
        module_title = []
        module_desc = []

        with open(f"data/{filepath}", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader) # skip header line
            for row in reader:
                if row[1]: # if link exists
                    title, desc = get_description(row[1])
                    module_title.append(title)
                    module_desc.append(desc)
                else:
                    module_title.append(None)
                    module_desc.append(None)

        # Add module Title and Description extracted from the module page
        data = pd.read_csv(f"data/{filepath}")
        data["Title"] = module_title
        data["Description"] = module_desc
        data.to_csv(f"data/{filepath}", index=False)


def get_description(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # print(url) # for debug

    module = soup.find("div", class_="group-left")

    # Search for module description
    try:
        desc_element = module.findChild("p")

        # Exception cases that are styled differently on SIT website
        if not desc_element:
            desc_element = module.find("div", class_="row--top-md")

        desc = desc_element.getText().strip()

    except Exception as e:
        print(f"Error getting description from {url}, {e}")
        desc = None
    
    # Search for module title
    try:
        title = module.findChild("h1").getText().strip()

    except Exception as e:
        print(f"Error getting title from {url}, {e}")
        title = None

    return [title, desc]

main()