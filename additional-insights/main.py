import pandas
import streamlit as st
import pandas as pd
import altair as alt
import os
import glob

# uses 2 csv files - the cleaned jobs csv files (IS and SE) with the lightcast skills appended
# currently reads these 2 files from the same directory as the script
# most popular industries can put in the main app, additional insights can be separate

# most popular industries
def industries_stats(jobs):
    # remove duplicates, exclude jobs where industries empty and then split values
    df = jobs.dropna(subset=['Industries'])
    df['Industries'] = df['Industries'].str.split(':')
    industry_list = df.explode('Industries')['Industries']

    st.header('Most popular industries')
    # get top 30 industries by count
    st.write(f'Total number of industries is {len(industry_list.unique())}, showing top 30')
    industries_display = industry_list.value_counts().to_frame().head(30)

    # display as bar chart
    st.write(alt.Chart(industries_display.reset_index()).properties(width=700).mark_bar().encode(
        y=alt.Y('Industries', sort=None, type='nominal', axis=alt.Axis(labelLimit=190)),
        x=alt.X('count:Q', title='Number of job listings')
    ))

# average skills identified per job (lightcast vs linkedin)
def skills_stats(jobs):
    # drop skill rows that are duplicates across IS and SE or do not have any skills identified by linkedin
    job_skills = jobs.dropna(subset=['Skills'])

    lightcast_skill_count = 0
    linkedin_skill_count = 0

    # add up total number of linkedin and lightcast skills respectively
    for item in job_skills.loc[:, ['Skills', 'Extracted Skills']].iterrows():
        linkedin_skill_count += len(str(item[1]['Skills']).split(':'))
        lightcast_skill_count += len(str(item[1]['Extracted Skills']).split(','))

    # average out and display in bar chart
    avg_linkedin_skill = round(linkedin_skill_count/len(job_skills), 2)
    avg_lightcast_skill = round(lightcast_skill_count/len(job_skills), 2)

    st.header('Average number of skills identified per job by each platform')

    data = pd.DataFrame({
        'Platform': ['Lightcast', 'LinkedIn'],
        'Count': [avg_lightcast_skill, avg_linkedin_skill]
    })

    st.write(alt.Chart(data).properties(width=700).mark_bar().encode(
        x='Platform:N',
        y='Count:Q'
    ))

# most popular companies
def company_stats(jobs):
    company_list = jobs['Company Name'].value_counts()
    st.header('Most popular companies')
    st.write(f'Total number of companies is {len(company_list)}, showing top 30')
    # display as bar chart
    st.write(alt.Chart(company_list.head(30).reset_index()).properties(width=700).mark_bar().encode(
        y=alt.Y('Company Name', sort=None, type='nominal', axis=alt.Axis(labelLimit=190)),
        x=alt.X('count:Q', title='Number of job listings')
    ))


# read files for job listings
job_df_list = []
job_data = glob.glob(os.path.join(os.getcwd(), '*.csv'))
# read all csv in folder
for file in job_data:
    job_df_list.append(pd.read_csv(file))

jobs_df = pandas.concat(job_df_list).drop_duplicates(subset=['Job URN'])

industries_stats(jobs_df)
company_stats(jobs_df)
skills_stats(jobs_df)



