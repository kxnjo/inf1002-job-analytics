import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from copy import deepcopy
import pandas as pd
import sys


# Our own modules
import gSearch

# Create an instance of Chrome Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("log-level=1")
driver = webdriver.Chrome(options=options)


def main():
    # Enter SIT website
    print(f"\nAttempting to retrieve SIT undergraduate degree programmes...")
    try:
        driver.get("https://www.singaporetech.edu.sg/undergraduate-programmes")
    except Exception as e:
        end_program(f"Unable to navigate into SIT Undergraduate Programmes. Error:{e}")
    
    # Get all courses available, end program if no courses found
    all_courses = get_all_courses()
    if len(all_courses) == 0:
        end_program("No courses available.")


    # Show courses that are available and request user input (choose courses)
    for index, course_name in all_courses.items():
        print(f"{index}: {course_name}")
    user_chosen_courses = request_user_input(all_courses)


    # Storing and formatting course information
    courses = {}
    data = {
        "Module Name": [],
        "Link": []
    }
    
    # Click into each course from the programmes page
    for c in user_chosen_courses:
        course_name = all_courses[c]
        print(f"\nAttempting to retrieve all modules from {course_name}...")
        try:
            click_course(course_name)
        except Exception as e:
            end_program(f"Unable to enter course page of {c}:{all_courses[c]}, Error:{e}")

        # Retrieve all modules listed in the degree programme
        try:
            all_mods = get_modules()
            courses[course_name] = deepcopy(data)
            courses[course_name]["Module Name"].extend(all_mods)
        except Exception as e:
            end_program(f"Unable to get modules of {c}:{all_courses[c]}, Error:{e}")

        driver.back()

    # For each module, use Google Search API to search for the top relevant module link and write into csv
    for course_name, course_data in courses.items():
        print(f"Attempting to retrieve module descriptions from {course_name}...")
        for mod in course_data["Module Name"]:
            try:
                link = gSearch.find_module(mod)
            except:
                end_program("Unable to search for module via Google Search API")
            course_data["Link"].append(link)
        data_out = pd.DataFrame(course_data)
        data_out.to_csv(f"data/{course_name}.csv", index=False)

    driver.quit()


# Retrieve all course names available on the webpage
def get_all_courses():
    courses = driver.find_elements(By.CLASS_NAME, 'course-card__title')
    all_courses = {}
    for index, course in enumerate(courses, start=1):
        all_courses[index] = course.text
    return all_courses


# Click into course page based on course name
def click_course(course):
    loaded_courses = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'grid-cards'))
    )
    xpath = f"//div[@class='course-card' and .//text()='{course}']/a"
    course_element = loaded_courses.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click()", course_element)


# Request user input on the choice of courses
def request_user_input(all_courses):
    print("\nPlease enter the indexes of chosen courses separated by commas (e.g. '26,27'). Alternatively, you can also enter only one course.")
    user_input = input("Choose courses:")

    # Re-prompt user until we get a valid input
    while not check_input_validity(user_input, len(all_courses)):
        user_input = input("Invalid input. Format is comma separated values e.g. '26,27' or '26'. Choose courses:")

    chosen_courses = [int(i) for i in user_input.split(",")]
    return chosen_courses


def check_input_validity(user_input, max_number):
    # Check if input are all integers
    try:
        course_numbers = [int(i) for i in user_input.split(",")]
    except:
        return False
    
    # Check if any of the inputs is out of range
    for course in course_numbers:
        if course <= 0 or course > max_number:
            return False
    return True


def get_modules():
    programme_structure = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'programme-structure'))
    )

    core_modules = programme_structure.find_elements(By.CLASS_NAME, 'Core')
    core_modules_text = get_text(core_modules)

    university_modules = programme_structure.find_elements(By.CLASS_NAME, 'University')
    university_modules_text = get_text(university_modules)

    all_mods = core_modules_text + university_modules_text
    return all_mods


def get_text(modules):
    clean_modules = []
    for module in modules:
        data = module.find_elements(By.TAG_NAME, 'td')
        data_text = data[0].get_attribute("textContent").strip().replace("\xa0", " ")
        clean_modules.append(data_text)
    return clean_modules


# display error, quit driver and quit program
def end_program(error):
    print(error)
    driver.quit()
    sys.exit(error)

#start_time = time.time()
main()
#print("--- %s seconds ---" % (time.time() - start_time))