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
