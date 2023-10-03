import string
import nltk
from nltk.corpus import stopwords
import pandas
import pandas as pd
import os
import glob
from datetime import datetime
import re


def save_data(df, filename):
    os.makedirs(f'{os.path.join(os.getcwd(), "processed")}', exist_ok=True)
    file_path = f'{os.path.join(os.getcwd(), "processed", filename)}'

    df.to_csv(file_path, index=False)


def clean_data(df):
    original_size = len(df)

    # drop duplicates based on job urn, and drop rows where mandatory attributes are empty
    df_for_cleaning = (df.drop_duplicates(subset=['Job URN'])
                       .dropna(subset=['Job Title', 'Job URN', 'Company Name', 'Location', 'Applicants',
                                       'Employment type', 'Job description', 'Posted on']))

    # number of rows after deduplication and dropping those with missing data
    initial_cleaned_size = len(df_for_cleaning)

    # save deduplicated data while job desc is still human-readable
    save_data(df_for_cleaning, f'{folder_name}_deduplicated_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv')

    # remove links from description
    df_for_cleaning['Job description'] = (df_for_cleaning['Job description']
                                          .apply(lambda x: " ".join(re.sub("(http\S+)",
                                                                           "", x) for x in x.split())))
    # remove email addresses
    df_for_cleaning['Job description'] = (df_for_cleaning['Job description']
                                          .apply(lambda x: " ".join(re.sub("([\w\.\-\_]+@[\w\.\-\_]+)",
                                                                           "", x) for x in x.split())))
    # lowercase all text
    df_for_cleaning['Job description'] = (df_for_cleaning['Job description']
                                          .apply(lambda x: " ".join(x.lower() for x in x.split())))

    # remove punctuation and numbers
    numbers_and_punctuation = set(string.punctuation + string.digits)
    df_for_cleaning['Job description'] = (df_for_cleaning['Job description']
                                          .apply(lambda x: ''.join(char for char in x
                                                                   if char not in numbers_and_punctuation)))

    # check if list of stopwords is downloaded and up to date
    nltk.download('stopwords')
    # remove stopwords
    stopwords_to_remove = stopwords.words('english')
    df_for_cleaning['Job description'] = (df_for_cleaning['Job description']
                                          .apply(lambda x: " ".join(x for x in x.split() if x not in stopwords_to_remove)))

    # save final cleaned version
    save_data(df_for_cleaning, f'{folder_name}_cleaned_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv')

    print(f'{original_size} rows imported, {initial_cleaned_size} rows left after initial cleaning '
          f'({original_size - initial_cleaned_size} duplicate or corrupt rows removed)')


if __name__ == '__main__':
    file_load_df_list = []
    folder_name = input('Enter name of folder to load data from: ')
    # generate folder path to read files from
    path = os.path.join(os.getcwd(), folder_name, '*.csv')
    data = glob.glob(path)

    # read all csv in folder
    for file in data:
        print(f'Reading {file}')
        file_load_df_list.append(pd.read_csv(file))

    raw_data = pandas.concat(file_load_df_list)
    clean_data(raw_data)
