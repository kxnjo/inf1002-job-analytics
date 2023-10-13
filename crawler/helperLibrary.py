import json
import requests
import time
from selenium.webdriver.common.by import By


class JobCard:
    """Class to represent info extracted from the job cards on the search page."""

    def __init__(self, job_title, company_name, location, job_urn):
        self.job_title = job_title
        self.company_name = company_name
        self.location = location
        self.job_urn = job_urn


class JobInfo:
    """Class to represent info extracted from the job listing (excluding skills).
    Optional attributes: seniority, job function, industries"""

    def __init__(self, posted_on, applicants, job_desc, employment_type, seniority="", job_function="", industries=""):
        self.posted_on = posted_on
        self.applicants = applicants
        self.seniority = seniority
        self.employment_type = employment_type
        self.job_function = job_function
        self.industries = industries
        self.job_desc = job_desc


class APIRetryCountException(Exception):
    """Raised when API retry count limit is reached"""
    pass


# convert a list into a string of colon-delimited values
def iterate_and_join(input_list):
    return ':'.join(str(x) for x in input_list)


# get necessary authentication cookies from selenium and pass to requests
def extract_cookies_and_header(browser):
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


# get linkedin-identified skills from API
def get_skills(job_urn, requests_cookies, header):
    tries = 0

    while True:
        tries += 1
        # raise exception if 3 tries all result in error
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

                # add skills to a list
                if skills_req_json['skillMatchStatuses'] is not None:
                    for skill in skills_req_json['skillMatchStatuses']:
                        skill_list.append(skill['localizedSkillDisplayName'])

                    # iterate and join skill names as colon-delimited (:) values
                    skills = iterate_and_join(skill_list)
                return skills
            elif skills_req.status_code == 429:
                # if too many requests
                print('Skills API rate limited, retrying in 3 seconds...')
            else:
                # if any other HTTP error occurs, log to console output and try again
                print(f'Skills API HTTP {skills_req.status_code} error with {job_urn}')

            # back off for 3 seconds then retry after an error
            time.sleep(3)
        else:
            raise APIRetryCountException


# get additional job info from API
def get_job_info(job_urn, requests_cookies, header):
    # for debug
    print(f'Current job urn: {job_urn}')
    tries = 0
    while True:
        # raise exception if 3 tries all result in error
        tries += 1
        if tries <= 3:
            # get additional info such as employment type
            info_req = requests.get(f'https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_urn}'
                                    f'?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65'
                                    f'&topN=1&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,'
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
                # posted on is a unix timestamp, so we have to convert it to human-readable date format
                posted_on = time.strftime('%d-%b-%Y', time.localtime(job_page_json['listedAt'] / 1000.0))

                return JobInfo(posted_on, applicants, job_desc, employment_type, seniority, job_function, industries)
            elif info_req.status_code == 429:
                # if too many requests
                print('Job info API rate limited, retrying in 3 seconds...')
            else:
                # if any other HTTP error occurs, log to console output and try again
                print(f'Job info API HTTP {info_req.status_code} error with {job_urn}')

            # back off for 3 seconds then retry after an error
            time.sleep(3)
        else:
            raise APIRetryCountException


# get info from job listing cards
def extract_card_info(card):
    # extract job title
    try:
        job_title = card.find('a', class_='job-card-list__title').get_text().strip()
    except AttributeError:
        print('Missing job title')
        return None

    # extract company name
    try:
        company_name = card.find('span', class_='job-card-container__primary-description').get_text().strip()
    except AttributeError:
        print('Missing company name')
        return None

    # extract job location
    try:
        location = card.find('li', class_='job-card-container__metadata-item').get_text().strip()
    except AttributeError:
        print('Missing location')
        return None

    # get job urn
    job_urn = card.get('data-occludable-job-id')

    return JobCard(job_title, company_name, location, job_urn)


def login(browser):
    browser.get("https://linkedin.com/login")
    browser.set_window_size(1280, 800)
    time.sleep(3)

    # enter user credentials into fields, then submit
    username = browser.find_element(By.ID, "username")
    username.send_keys("pwcudulv@pokemail.net")

    pword = browser.find_element(By.ID, "password")
    pword.send_keys("INF_1002")

    browser.find_element(By.XPATH, "//button[@type='submit']").click()

    # if linkedin asks to complete a security check, alert user and wait for confirmation that it is done
    login_page = browser.find_element(by=By.TAG_NAME, value='body').text.strip()
    if 'security check' in login_page.lower():
        # create a popup in the browser to tell the user to complete the security challenge
        browser.execute_script(
            "alert('Message from crawler: Please complete security check, then return to the console.');")
        input('Security challenge detected, complete it and then input anything to continue.')
