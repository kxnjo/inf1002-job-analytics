import json
import requests
from datetime import datetime
import time
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import gc
import os


class APIRetryCountException(Exception):
    """API retry count limit reached"""
    pass


def iterate_and_join(input_list):
    return ':'.join(str(x) for x in input_list)

def extract_cookies_and_header(browser):
    # get necessary authentication cookies from selenium and pass to requests
    cookies = browser.get_cookies()
    header = {}
    cookies_list = {}
    for c in cookies:
        cookies_list[c['name']] = c['value']
        # send the JSESSIONID cookie value in the Csrf-Token header for API authentication
        if c['name'] == 'JSESSIONID':
            header['Csrf-Token'] = c['value'].strip('"')

    return {
        'cookies': cookies_list,
        'header': header
    }
def get_skills(job_urn, requests_cookies, header):
    tries = 0

    while True:
        tries += 1
        # exception if 3 tries all result in error
        if tries <= 3:
            # get job skills using API
            skills_req = requests.get(f'https://www.linkedin.com/voyager/api/voyagerAssessmentsDashJobSkillMatchInsight'
                                      f'/urn%3Ali%3Afsd_jobSkillMatchInsight%3A{job_urn}?'
                                      f'decorationId=com.linkedin.voyager.dash.deco.assessments.FullJobSkillMatchInsight-16'
                                      , cookies=requests_cookies, headers=header)

            if skills_req.status_code == 200:
                # get skills from API
                skills_req_json = json.loads(skills_req.text)
                skill_list = []

                for skill in skills_req_json['skillMatchStatuses']:
                    skill_list.append(skill['localizedSkillDisplayName'])

                # iterate and join skill names as colon-delimited (:) values
                skills = iterate_and_join(skill_list)
                return skills
            elif skills_req.status_code == 429:
                # if too many requests, back off for 3 seconds then retry
                print('Skills API rate limited, retrying in 3 seconds...')
            else:
                print(f'Skills API HTTP {skills_req.status_code} error with {job_urn}')

            sleep(3)
        else:
            raise APIRetryCountException

def get_job_info(job_urn, requests_cookies, header):
    # for debug
    print(f'Current job urn: {job_urn}')
    tries = 0
    while True:
        # exception if 3 tries all result in error
        tries += 1
        if tries <= 3:
            # get additional info such as employment type
            info_req = requests.get(f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_urn}'
                                     f'?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1'
                                     f'&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,'
                                     f'SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)'
                                     , cookies=requests_cookies, headers=header)

            if info_req.status_code == 200:
                industries_list = []
                job_func_list = []

                job_page_json = json.loads(info_req.text)

                # get all industries
                for industry in job_page_json['formattedIndustries']:
                    industries_list.append(industry)

                # get all job functions
                for job_func in job_page_json['formattedJobFunctions']:
                    job_func_list.append(job_func)

                applicants = job_page_json['applies']
                seniority = job_page_json['formattedExperienceLevel']
                employment_type = job_page_json['formattedEmploymentStatus']
                job_function = iterate_and_join(job_func_list)
                industries = iterate_and_join(industries_list)
                job_desc = job_page_json['description']['text']
                posted_on = time.strftime('%d-%b-%Y', time.localtime(job_page_json['listedAt'] / 1000.0))

                return {
                    'posted_on': posted_on,
                    'applicants': applicants,
                    'seniority': seniority,
                    'emp_type': employment_type,
                    'job_func': job_function,
                    'industries': industries,
                    'job_desc': job_desc
                }
            elif info_req.status_code == 429:
                print('Job info API rate limited, retrying in 3 seconds...')
            else:
                print(f'Job info API HTTP {info_req.status_code} error with {job_urn}')

            # back off for 3 seconds then retry
            sleep(3)
        else:
            raise APIRetryCountException


def crawl_job_listings():
    data = []

    i = 0
    crawled_count = 0
    options = Options()
    options.binary_location = r"C:\Users\denny\Downloads\chrome-win64\chrome-win64\chrome.exe"

    # if user doesn't want to see the browser load pages
    # if userOptions.upper() == "H":
    #     print("Headless mode selected")
    #     options.add_argument("--headless=new")  # don't show browser screen

    browser = webdriver.Chrome(options=options)
    browser.get("https://linkedin.com/login")
    browser.set_window_size(1280, 800)
    sleep(3)

    username = browser.find_element(By.ID, "username")
    username.send_keys("yiteriv870@recutv.com")

    pword = browser.find_element(By.ID, "password")
    pword.send_keys("INF_1002")

    browser.find_element(By.XPATH, "//button[@type='submit']").click()

    login_page = browser.find_element(by=By.TAG_NAME, value='body').text.strip()
    if 'security check' in login_page.lower():
        print('Complete the security challenge, you have 15 seconds to do so.')
        sleep(15)

    query = 'Penetration Tester'
    job_search_location = 'Singapore'

    url = f'https://www.linkedin.com/jobs/search/?keywords={query}&location={job_search_location}'

    # navigate to job search page
    browser.get(url)
    sleep(3)

    # get necessary authentication cookies from selenium and pass to requests
    credentials = extract_cookies_and_header(browser)
    requests_cookies = credentials['cookies']
    header = credentials['header']

    # name of csv file
    filename = f'({query}_{job_search_location})_crawl_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv'

    # change 2nd param of range to select how many jobs to crawl. basically (range - 1) * 25 = max no. of results
    for page_num in range(1, 41):
        # find individual job cards
        job_card_list = browser.find_elements(by=By.CLASS_NAME, value='jobs-search-results__list-item')

        # manually scroll through the job cards to the bottom so all contents are loaded
        for item in job_card_list:
            browser.execute_script("arguments[0].scrollIntoView();", item)
            sleep(0.3)

        # Wait for 3 seconds in case job cards haven't fully loaded, then update beautifulsoup
        sleep(2)
        soup = bs(browser.page_source, 'html.parser')

        job_postings = soup.find_all('li', {'class': 'jobs-search-results__list-item'})

        # total job postings processed
        i += len(job_postings)

        # Extract relevant information from each job posting card and store it in a list of dictionaries
        for job_posting in job_postings:
            crawled_count += 1
            try:
                job_title = job_posting.find('a', class_='job-card-list__title').get_text().strip()
            except AttributeError:
                print('missing job title')
                job_title = None

            try:
                company_name = job_posting.find('span',
                                                class_='job-card-container__primary-description').get_text().strip()
            except AttributeError:
                print('missing company name')
                company_name = None

            try:
                location = job_posting.find('li', class_='job-card-container__metadata-item').get_text().strip()
            except AttributeError:
                print('missing location')
                location = None

            # get job urn
            job_urn = job_posting.get('data-occludable-job-id')

            # get job skills using API
            try:
                skills = get_skills(job_urn, requests_cookies, header)
            except APIRetryCountException:
                print(f'Skills API retry limit reached for job {job_urn}')
                continue
            except Exception as err:
                print(f'Skills API exception "{str(err)}" for job {job_urn}')
                continue

            # get additional info such as employment type
            try:
                job_info = get_job_info(job_urn, requests_cookies, header)
            except APIRetryCountException:
                print(f'job info API retry limit reached for job {job_urn}')
                continue
            except Exception as err:
                print(f'job info API exception "{str(err)}" for job {job_urn}')
                continue

            # for debug
            print(f'job page {crawled_count}')

            data.append({
                'Job Title': job_title,
                'Job URN': job_urn,
                'Company Name': company_name,
                'Location': location,
                'Applicants': job_info['applicants'],
                'Seniority': job_info['seniority'],
                'Employment type': job_info['emp_type'],
                'Job function': job_info['job_func'],
                'Industries': job_info['industries'],
                'Job description': job_info['job_desc'],
                'Posted on': job_info['posted_on'],
                'Skills': skills
            })
            # for debug
            print({
                'Job Title': job_title,
                'Job URN': job_urn,
                'Company Name': company_name,
                'Location': location,
                'Applicants': job_info['applicants'],
                'Seniority': job_info['seniority'],
                'Employment type': job_info['emp_type'],
                'Job function': job_info['job_func'],
                'Industries': job_info['industries'],
                'Job description': job_info['job_desc'],
                'Posted on': job_info['posted_on'],
                'Skills': skills
            })

            # force garbage collection to reduce memory usage
            gc.collect()

        # append results to csv for every page, creates file if not exists
        # in case of crash, at most 1 page of results lost
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', index=False, header=not os.path.exists(filename))

        # find button to access next page and click it
        try:
            browser.find_element(by=By.XPATH, value=f'//button[@aria-label="Page {page_num + 1}"]').click()
        except common.NoSuchElementException:
            print('End of job listings')
            break

        # reset data list
        data = []

        sleep(0.4)

    print(f'Crawled a total of {i} job listings')
    print(f'Results saved to {filename}')


if __name__ == '__main__':
    # crawl_job_listings(
    #     input('Enter H to run in headless mode, or any other key to see the crawler working in the browser.'))
    crawl_job_listings()
