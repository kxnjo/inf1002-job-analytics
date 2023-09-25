import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC

#TODO: Create a class for driver instead

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def main():
    # Enter SIT website
    try:
        driver.get("https://www.singaporetech.edu.sg/undergraduate-programmes")
    except:
        print(f"Unable to enter SIT Undergraduate Programmes page")
        driver.quit()
        return
    
    # Get all courses available, end program if no courses found
    all_courses = get_all_courses()
    if len(all_courses) == 0:
        print("No courses available.")
        driver.quit()
        return

    # Show courses that are available and request user input (choose courses)
    for index, course_name in all_courses.items():
        print(f"{index}: {course_name}")
    chosen_courses = request_user_input(all_courses)


    # Click into each course and extract the modules, write into CSV format
    for c in chosen_courses:
        try:
            click_course(all_courses[c])
        except Exception as e:
            print(f"Unable to enter course page of {c}:{all_courses[c]}, Error:{e}")
            return
        
        try:
            all_mods = get_modules()
        except Exception as e:
            print(f"Unable to get modules of {c}:{all_courses[c]}, Error:{e}")

        with open(f"data/{all_courses[c]}.csv", "w") as f:
            f.write("Module Name" + "\n")
            for mod in all_mods:
                f.write(mod + "\n")

        driver.back()
    

    driver.quit()


def get_all_courses():
    courses = driver.find_elements(By.CLASS_NAME, 'course-card__title')
    all_courses = {}
    for index, course in enumerate(courses, start=1):
        all_courses[index] = course.text
    return all_courses


def click_course(course):
    loaded_courses = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'grid-cards'))
    )
    xpath = f"//div[@class='course-card' and .//text()='{course}']/a"
    course_element = loaded_courses.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click()", course_element)


def request_user_input(all_courses):
    print("\nPlease enter the indexes of your chosen courses separated by commas (e.g. '1,4,7'). Alternatively, you can also enter only one course.")
    user_input = input("Choose courses:")
    while not clean_user_input(user_input, len(all_courses)):
        user_input = input("Invalid input. Format is comma separated values e.g. '1,4,7' or '1'. Choose courses:")

    chosen_courses = [int(i) for i in user_input.split(",")]
    return chosen_courses


def clean_user_input(user_input, max_number):
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
        data_text = data[0].get_attribute("textContent").strip()
        clean_modules.append(data_text)
    return clean_modules


start_time = time.time()
main()
#print("--- %s seconds ---" % (time.time() - start_time))