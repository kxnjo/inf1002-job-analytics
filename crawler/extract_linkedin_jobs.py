from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium import common
from selenium.webdriver.common.by import By
from gc import collect as collect_garbage
from os import path
import helperLibrary
from helperLibrary import APIRetryCountException


def crawl_job_listings(query):
    data = []
    crawled_count = 0
    relevant = 0
    browser = webdriver.Chrome()

    # log in to linkedin
    try:
        helperLibrary.login(browser)
    except:
        print("An error occurred while logging in to LinkedIn")
        return

    job_search_location = 'Singapore'
    url = f'https://www.linkedin.com/jobs/search/?keywords={query}&location={job_search_location}'

    # navigate to job search page
    browser.get(url)
    sleep(3)

    # check if no search results for the search term
    if browser.find_elements(by=By.CLASS_NAME, value="jobs-search-no-results-banner"):
        print("There were no matching results on LinkedIn for your search term")
        return

    # get necessary authentication cookies from selenium and pass to requests
    credentials = helperLibrary.extract_cookies_and_header(browser)
    requests_cookies = credentials['cookies']
    header = credentials['header']

    # name of csv file
    filename = f'({query}_{job_search_location})_crawl_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv'

    # crawl up to 1000 jobs per search term (25 per page)
    for page_num in range(1, 41):
        # find individual job cards
        job_card_list = browser.find_elements(by=By.CLASS_NAME, value='jobs-search-results__list-item')

        # manually scroll through the job cards to the bottom so all contents are loaded
        for item in job_card_list:
            browser.execute_script("arguments[0].scrollIntoView();", item)
            sleep(0.3)

        # Wait for 2 seconds in case job cards haven't fully loaded, then update beautifulsoup
        sleep(2)
        soup = bs(browser.page_source, 'html.parser')

        job_postings = soup.find_all('li', {'class': 'jobs-search-results__list-item'})

        # Extract relevant information from each job posting card and store it in a list of dictionaries
        for job_posting in job_postings:
            job_card = helperLibrary.extract_card_info(job_posting)

            # if job card is missing info for any reason, skip
            if job_card is not None:
                # if job title doesn't contain any words of the search query, consider it irrelevant
                words_to_match = query.lower().split(" ")
                if not any(word in job_card.job_title.lower() for word in words_to_match):
                    print(f'Skipped potentially irrelevant job: {job_card.job_title}')
                    continue

                relevant += 1
            else:
                print('Skipping job card with missing information')
                continue

            job_urn = job_card.job_urn

            # get job skills using API
            try:
                skills = helperLibrary.get_skills(job_urn, requests_cookies, header)
            except APIRetryCountException:
                print(f'Skills API retry limit reached for job {job_urn}')
                continue
            except Exception as err:
                print(f'Skills API exception "{str(err)}" for job {job_urn}')
                continue

            # get additional info such as employment type
            try:
                job_info = helperLibrary.get_job_info(job_urn, requests_cookies, header)
            except APIRetryCountException:
                print(f'Job info API retry limit reached for job {job_urn}')
                continue
            except Exception as err:
                print(f'Job info API exception "{str(err)}" for job {job_urn}')
                continue

            job = {
                'Job Title': job_card.job_title,
                'Job URN': job_card.job_urn,
                'Company Name': job_card.company_name,
                'Location': job_card.location,
                'Applicants': job_info.applicants,
                'Seniority': job_info.seniority,
                'Employment type': job_info.employment_type,
                'Job function': job_info.job_function,
                'Industries': job_info.industries,
                'Job description': job_info.job_desc,
                'Posted on': job_info.posted_on,
                'Skills': skills
            }

            data.append(job)
            # for debug
            print(job)

            # force garbage collection to reduce memory usage
            collect_garbage()

        # append results to csv for every page, creates file if not exists
        # in case of crash, at most 1 page of results lost
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', index=False, header=not path.exists(filename))

        # find button to access next page and click it
        try:
            browser.find_element(by=By.XPATH, value=f'//button[@aria-label="Page {page_num + 1}"]').click()
        except common.NoSuchElementException:
            # cannot find button for next page means we have reached the last page
            print('End of job listings')
            break

        # reset data list
        data = []

        # wait between API calls to avoid getting rate-limited
        sleep(0.4)

    print(f'Crawled a total of {crawled_count} job listings, found {relevant} results that should be relevant')
    print(f'Results saved to {filename}')


crawl_job_listings(input('Enter your search term: '))
