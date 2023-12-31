from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import os
import string

def main():
    # Read csv files containing extracted data
    path = "data/"
    filepaths = os.listdir(path)

    for filepath in filepaths:
        if filepath.endswith(".csv"):
            print(f"Reading {filepath}")
            module_title = []
            module_desc = []

            with open(f"data/{filepath}", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader) # skip header line
                for row in reader:
                    if row[1]: # if link exists
                        title, desc = get_description(row[1])

                        # Stores data of module description
                        if module_match(row[0], title):
                            module_title.append(title)
                            module_desc.append(desc)
                            print(f"Added description for {title}")
                            continue

                    # If link doesn't exist or module name doesn't match, set value to None
                    module_title.append(None)
                    module_desc.append(None)

            # Add module Title and Description extracted from the module page
            data = pd.read_csv(f"data/{filepath}")
            data["Title"] = module_title
            data["Description"] = module_desc
            data.to_csv(f"data/{filepath}", index=False, encoding="utf-8")


# Collect data from module description
def get_description(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Look for module description in the page
    module = soup.find("div", class_="group-left")

    # Search for text
    try:
        desc_elements = module.findChildren("p")
        # Handle exception cases that are styled differently on SIT website
        if not desc_elements:
            desc_elements = module.findAll("div", class_="row--top-md")

        # Save descriptions into 1 paragraph.
        desc_text = []
        for text in desc_elements:
            desc = text.getText().strip()
            desc_text.append(desc)
        desc = " ".join(desc_text)

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


# Check if module description page matches module name stated in course page
def module_match(mod_name, description_page_name):
    # Removing whitespaces and punctuation
    removal = string.punctuation + string.whitespace
    mod_name1 = mod_name.translate(str.maketrans('', '', removal))
    mod_name2 = description_page_name.translate(str.maketrans('', '', removal))

    # Replacing some common US-UK English differences
    clean_mod_name1 = mod_name1.replace("ization", "isation").replace("ze", "se")
    clean_mod_name2 = mod_name2.replace("ization", "isation").replace("ize", "ise")

    if clean_mod_name1.lower() == clean_mod_name2.lower():
        return True
    return False


main()