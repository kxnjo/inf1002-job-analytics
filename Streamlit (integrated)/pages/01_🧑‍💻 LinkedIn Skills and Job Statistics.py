
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
# import streamlit_wordcloud as wordcloud

st.set_page_config(
    page_title='SIT Skills and Job Analysis', 
    page_icon='🔍', 
    layout='wide'
    )

st.title('🧑‍💻 LinkedIn Skills and Job Statistics')
deg = st.sidebar.selectbox(label='Select LinkedIn Category', options=('LinkedIn Information Systems', 'LinkedIn Software Engineering'), placeholder='Choose a Degree')

def main(deg):
         
    newDF, csvName = userChoices(deg)
    createPlot(newDF,csvName)


def userChoices(deg):
    if deg == "LinkedIn Information Systems":
        csv_name = 'data/Appended_Skills_IS.csv'
        newDF= pd.read_csv(csv_name)
    else:
        csv_name = 'data/Appended_Skills_SE.csv'
        newDF= pd.read_csv(csv_name)

    return newDF, csv_name
    
def createPlot(data1, data2):
    # LinkedIn Skills ONLY
    jobDF = data1
    # remove NaN values in Seniority and Extracted Skills column
    jobDF = jobDF.dropna(subset=['Seniority'])
    jobDF = jobDF.dropna(subset=['Extracted Skills'])
    columns_to_extract = ['Seniority', 'Extracted Skills']
    # create new dataframe with only seniority and extracted skills
    new_df = jobDF[columns_to_extract]
    
    # Split the "Extracted Skills" column by comma
    skills_split = new_df['Extracted Skills'].str.split(',')

    # Create a new DataFrame with the split skills
    skills_df = pd.DataFrame(skills_split.tolist(), index=new_df.index)

    # Merge the "Seniority" column with the skills DataFrame
    merged_df = pd.concat([new_df['Seniority'], skills_df], axis=1)

    # .melt is a transform func, id_vars -> x axis , value_name-> y axis column name
    stacked_df = merged_df.melt(id_vars=['Seniority'], value_name= "Skills")
    stacked_df = stacked_df.drop(columns="variable")
    stacked_df = stacked_df.dropna(subset="Skills")

    testDf = pd.DataFrame(stacked_df, columns = ["Seniority", "Skills"])
    # sum count of each skill
    pivot_df = testDf.pivot_table(index='Skills', columns='Seniority', aggfunc='size', fill_value=0)

    # sort by the sum of all seniority levels
    sorted_df = pivot_df.sum(axis=1).sort_values(ascending=False)

    # # Use the sorted index to rearrange the rows in the df
    sorted_df = pivot_df.loc[sorted_df.index]
    # print(sorted_df)

    col1, space, col2 = st.columns([6,1,9])
   
    with col1: 
    # df skills
        dfSkills = sorted_df.index
        num_skills_to_display = st.slider("Number of Skills to Display", 1, 50 , 25) # 1 - lowest , 50 - max , 5 - default
        # Create a list of all seniority levels for default selection
        all_seniorities = sorted_df.columns.to_list()

    with col2:
        # Add a sidebar multi-select with default selection of all seniority levels
        selected_seniorities = st.multiselect("Select Seniority Levels", all_seniorities, all_seniorities)

    # Filter the DataFrame based on selected seniority levels
    filtered_df = sorted_df[selected_seniorities]

    # Sort the DataFrame in descending order by the sum of selected seniority levels
    sorted_filtered_df = filtered_df.loc[filtered_df.sum(axis=1).sort_values(ascending=False).index]

    # SIT SKILLS
    if data2 == "data/Appended_Skills_IS.csv":
        schoolDf = pd.read_csv("data/ICT(IS)_Module_Description_Skills.csv")
        courseSelected = "Information Security"
    else:
        schoolDf = pd.read_csv("data/ICT(SE)_Module_Description_Skills.csv")
        courseSelected = "Software Engineering"
    
    schoolSkills = schoolDf["Skills"].to_list()

    schDf = sorted_filtered_df[sorted_filtered_df.index.isin(schoolSkills)]
    schDfSkills = schDf.index

    st.header(f"LinkedIn's Top {courseSelected} Skills")
    fig1 = px.bar(sorted_filtered_df.head(num_skills_to_display), x= selected_seniorities, y= dfSkills[:num_skills_to_display], width=720, labels ={'x': 'Top Skills from LinkedIn Job Postings', 'variable': 'Seniority Level', 'value': 'Number of Occurrences', 'y': 'Skills'})    
    
    st.plotly_chart(fig1)
    #panda series to dataframe
    countJobs = jobDF['Seniority'].value_counts().reset_index()
    result = ""
    for index, row in countJobs.iterrows():
        seniority_level = row['Seniority']
        count = row['count']
        if result:  # Add a comma and space if result is not empty
            result += ", "
        result += f"{seniority_level} -{count} Jobs"

    st.caption(f"Disclaimer: {result}")

    return sorted_df















## Denny's code
# most popular industries
def industries_stats(jobs):
    # remove duplicates, exclude jobs where industries empty and then split values
    df = jobs.dropna(subset=['Industries']).drop_duplicates(subset=['Job URN'])
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
    st.write(alt.Chart(industries_display.reset_index()).properties(width=1000).mark_bar().encode(
        y=alt.Y('Industries', sort=None, type='nominal', axis=alt.Axis(labelLimit=190)),
        x=alt.X('count:Q', title='Number of job listings')
    ))

# average skills identified per job (lightcast vs linkedin)
def skills_stats(jobs):
    # drop skill rows that are duplicates across IS and SE or do not have any skills identified by linkedin
    job_skills = jobs.drop_duplicates(subset=['Job URN']).dropna(subset=['Skills'])

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

    st.write(alt.Chart(data).properties(width=1000).mark_bar().encode(
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

try:

    st.selectbox(label='Choose Type of Skill', options=('Soft Skills', 'Hard Skills', 'Both'), placeholder='Type of Skill')

    job_df_list = []
    job_data = ['data/Appended_Skills_IS.csv','data/Appended_Skills_SE.csv']

    #read csv based on degree chosen
    if deg == 'LinkedIn Information Systems':
        job_df_list.append(pd.read_csv(job_data[0]))

    elif deg == 'LinkedIn Software Engineering':
        job_df_list.append(pd.read_csv(job_data[1]))

    st.write('#')

    main(deg)
    
    jobs_df = pd.concat(job_df_list)

    st.write('#')

    industries_stats(jobs_df)
    st.write('#')
    company_stats(jobs_df)
    st.write('#')
    skills_stats(jobs_df)

except Exception:
    st.write('Oops, no match found')

