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
    # get top n industries by count selected using slider, default is 10, max 50
    to_show = st.slider('Select top n results to display', 10, 50, 10, key='industries-slider')
    st.write(f'Total number of industries is {len(industry_list.unique())}, showing top {to_show}')

    # update chart on slider change
    if to_show:
        industries_display = industry_list.value_counts().to_frame().head(to_show)

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
    # count job listings grouped by company name
    company_list = jobs['Company Name'].value_counts()
    st.header('Most popular companies')

    company_list_display = company_list
    # get top n companies by count selected using slider, default is 10, max 50
    to_show = st.slider('Select top n results to display', 10, 50, 10, key='companies-slider')
    st.write(f'Total number of companies is {len(company_list)}, showing top {to_show}')

    # update chart on slider change
    if to_show:
        company_list_display = company_list.to_frame().head(to_show)

    # display as bar chart
    st.write(alt.Chart(company_list_display.reset_index()).properties(width=700).mark_bar().encode(
        y=alt.Y('Company Name', sort=None, type='nominal', axis=alt.Axis(labelLimit=190)),
        x=alt.X('count:Q', title='Number of job listings')
    ))

    st.header('Companies sorted by number of job listings')
    # dataframe for display in table
    company_list_search = company_list.to_frame()
    # allow user to search for a company and see how many job listings they have
    search = st.text_input('Search for a company')
    if search:
        company_list_search = company_list[company_list.index.str.contains(search, case=False)].to_frame()

    st.dataframe(company_list_search.rename(columns={'count': 'Number of job listings'}), width=700
                 , column_config={
                    'Company Name': st.column_config.TextColumn(width='large'),
                    'Number of job listings': st.column_config.TextColumn(width='small')
                })

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
