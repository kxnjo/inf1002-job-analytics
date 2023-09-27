from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

filepaths = ["Information and Communications Technology (Information Security).csv", "Information and Communications Technology (Software Engineering).csv"]

def main():
    for filepath in filepaths:
        module_title = []
        module_desc = []
        with open(f"data/{filepath}", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[1]:
                    title, desc = get_description(row[1])
                    module_title.append(title)
                    module_desc.append(desc)
                    """
                    if title == row[1]:
                        module_desc.append(desc)
                    else:
                        module_desc.append("incorrect module")
                    """
                else:
                    module_title.append(None)
                    module_desc.append(None)

        data = pd.read_csv(f"data/{filepath}")
        data["Title"] = module_title
        data["Description"] = module_desc
        data.to_csv(f"data/{filepath}", index=False)

def get_description(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    print(url)

    module = soup.find("div", class_="group-left")

    # Search for module description
    try:
        module_desc = module.findChild("p")
        # Exception cases that are styled differently on SIT website
        if not module_desc:
            module_desc = module.find("div", class_="row--top-md")

        module_desc = module_desc.getText().strip()

    except Exception as e:
        print(f"Error getting description from {url}, {e}")
        module_desc = None
    
    # Search for module title
    try:
        module_title = module.findChild("h1").getText().strip()

    except Exception as e:
        print(f"Error getting title from {url}, {e}")
        module_title = None

    return [module_title, module_desc]

main()