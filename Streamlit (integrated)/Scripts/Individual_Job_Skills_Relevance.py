import streamlit as st
import base64
import pandas as pd
from collections import OrderedDict 

# Zhuo En's function
def search(LinkedInData, df2):

    # obtain all jobs from LinkedIn, then remove NaN
    jobs = LinkedInData['Job Title'].dropna(axis=0)

    # to remove duplicated from list 
    jobs = sorted(list(OrderedDict.fromkeys(jobs))) 
    job_search = st.multiselect('Jobs', jobs)

    # Filter the DataFrame based on the job and skill search
    if job_search:

        filtered_df = pd.DataFrame()
        if len(job_search) != 0:
            for i in job_search:
                fil_df = pd.DataFrame()
                fil_df = LinkedInData[LinkedInData['Job Title'].str.contains(i, case=False)]
                filtered_df = pd.concat([filtered_df, fil_df], ignore_index=1)
        
    else:
        filtered_df = LinkedInData

    return filtered_df

def comparison2(df1_part2, df2):
    # PART 2 Compare each job to the sit skills
    st.header("Individual Job Skills Relevance")

    # Split skills in df1_part2 into a list of skills
    df1_part2['Skills Extracted'] = df1_part2['Extracted Skills'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
    # print(df1_part2['Extracted Skills'])

    # Create a set of skills from df2 for faster lookup
    available_skills = set(df2['Skills'])

    # Function to calculate skill percentage for a job and find unmatched skills
    def calculate_skill_percentage(job_skills):
        matched_skills = [skill for skill in job_skills if skill in available_skills]
        unmatched_skills = [skill for skill in job_skills if skill not in available_skills]
        total_skills = len(job_skills)
        total_matched_skills = len(matched_skills)

        # Calculate the skill percentage with 2 decimal places
        skill_percentage = round((total_matched_skills / total_skills) * 100, 2) if total_skills > 0 else 0

        return skill_percentage, unmatched_skills

    # Calculate skill percentage and find unmatched skills for each job
    df1_part2['skill_percentage'], df1_part2['unmatched_skills'] = zip(
        *df1_part2['Skills Extracted'].apply(calculate_skill_percentage))

    # Sort the DataFrame by 'Matching_Skills_Percentage' in descending order
    df1_part2 = df1_part2.sort_values(by='skill_percentage', ascending=False)

    # Change the default index column to start from 1
    df1_part2.index = range(1, len(df1_part2) + 1)

    filtered_df = search(df1_part2, df2)

    # Job Title search input
    # search_title = st.text_input("Search for a Job Title:")

    # Display the results in a table with skill_percentage formatted to 2 decimal places
    st.dataframe(filtered_df[['Job Title', 'skill_percentage',  'unmatched_skills', 'Skills Extracted']].rename(columns={'skill_percentage': 'Skill Percentage', 'unmatched_skills': 'Unmatched Skills'}), hide_index= True, height=300, use_container_width= True)

    # Export the updated job CSV
    def export_csv():
        csv = df1_part2[['Job Title', 'skill_percentage',  'unmatched_skills', 'Skills Extracted']].rename(columns={'skill_percentage': 'Skill Percentage', 'unmatched_skills': 'Unmatched Skills'}).to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="updated_job_skills.csv" style="padding: 8px 16px; background-color: #008CBA; color: white; text-decoration: none; border-radius: 5px;">Download CSV</a>'
        return href

    st.markdown(export_csv(), unsafe_allow_html=True)
