<h1 align="center">Hi 👋, this is Linkedout</h1>
<h3 align="center">A web application tool for data analytics and visualisation. The project aims to study the current demands of the job market and perform analysis in comparison to the skills provided in respective undergraduate degrees in SIT.</h3>

## Packages required
Run the following code in your terminal
`pip install -r requirements.txt`

## File Directories
- 🧑‍🔧 LinkedIn Job Extraction
    - [Data extractions of for LinkedIn Jobs](./crawler/extract_linkedin_jobs.py)
    - [Data cleaning for LinkedIn](./data-cleaner/clean_linkedin_jobs.py)
        - When prompted to enter a folder name, enter "IS" or "SE" to use our sample data
    - [Skills Extraction for LinkedIn](./extract_linkedIn_skills/extract_linkedIn_skills.py)
- 🔭 Data Extraction for SIT's Website
    - [Extraction of courses and modules](./sit_crawler/sit_get_modules.py)
    - [Extraction of module descriptions](./sit_crawler/get_module_description.py)
    - [Skills Extraction for SIT](./extract_SIT_skills/extract_SIT_skills.py)
- 📝 Skills classifier
    - [Dataset skills preprocessing + Creation of model](./skills-classifier/skills_classifier_model.ipynb)
    - [Classify LinkedIn Skills](./skills-classifier/classify_linkedin_skills.py)
    - [Classify Skill Function File](./skills-classifier/classify_skills.py)
- 📊 Data Visualisation Web Application
    - [Web Application](https://github.com/kxnjo/inf1002-job-analytics/blob/main/Streamlit%20(integrated)/%F0%9F%94%8D%20SIT%20Skills%20and%20Job%20Analysis.py)