# INF1002 Python Project
A web application tool for data analytics and visualisation.
The project aims to study the current demands of the job market and perform analysis in comparison to the skills provided in respective undergraduate degrees in SIT.

## Packages to install
Run the following code in your terminal
`pip install -r requirements.txt`

## Files to run
### `./crawler` - Data Extraction for LinkedIn
Extraction of LinkedIn jobs: `extract_linkedin_jobs.py`

### `./data-cleaner` - Data Cleaning for LinkedIn
Cleaning of LinkedIn data: `clean_linkedin_jobs.py`

When prompted to enter a folder name, enter "IS" or "SE" to use our sample data

### - Skills Extraction for LinkedIn



### `./sit_crawler` - Data Extraction for SIT's Website 
Extraction of courses and modules: `sit_get_modules.py`  
Extraction of module descriptions: `get_module_description.py`


### `./extract_SIT_skills` - Skills Extraction for SIT
Extract skills: `extract_SIT_skills.py`


### `./skills-classifier` - Classifies skills: Hard skills, Soft skills
Dataset skills preprocessing + Creation of model: `skills_classifier_model.ipynb`
Classifying Linkedin Skills: `classify_linkedin_skills.py`
Classify Skill Function File: `classify_skills.py`


### `./Streamlit (integrated)` - Web Application
Web Application: `SIT Skills and Job Analysis.py`



<h1 align="center">Hi 👋, this is Linkedout</h1>
<h3 align="center">A web application tool for data analytics and visualisation. The project aims to study the current demands of the job market and perform analysis in comparison to the skills provided in respective undergraduate degrees in SIT.</h3>

## Packages required
Run the following code in your terminal
`pip install -r requirements.txt`

## File Directories
- 🧑‍🔧 LinkedIn Job Extraction
    - [Data extractions of for LinkedIn Jobs](./crawler/extract_linkedin_jobs.py)
    - [Data cleaning for LinkedIn](./data-cleaner/clean_linkedin_jobs.py)
    When prompted to enter a folder name, enter "IS" or "SE" to use our sample data
    - [Skills Extraction for LinkedIn](./*)
- 🔭 Data Extraction for SIT's Website
    - [Extraction of courses and modules](./sit_crawler/sit_get_modules.py)
    - [Extraction of module descriptions](./sit_crawler/get_module_descriptions.py)
    - [Skills Extraction for SIT](./extract_SIT_skills/extract_SIT_skills.py)
- 📝 Skills classifier
    - [Dataset skills preprocessing + Creation of model](./skills-classifier/skills_classifier_model.ipynb)
    - [Classify LinkedIn Skills](./skills-classifier/classify_linkedin_skills.py)
    - [Classify Skill Function File](./skills-classifier/classify_skills.py)
- 📊 Data Visualisation Web Application
    - [Web Application](./Streamlit(integrated)/SIT Skills and Job Analysis.py)