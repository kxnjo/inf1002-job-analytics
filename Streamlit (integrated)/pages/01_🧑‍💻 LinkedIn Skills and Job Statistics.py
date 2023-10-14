
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import streamlit_wordcloud as wordcloud

st.set_page_config(
    page_title='SIT Skills and Job Analysis', 
    page_icon='🔍', 
    layout='wide'
    )

st.title('🧑‍💻 LinkedIn Skills and Job Statistics')
deg = st.sidebar.selectbox(label='Select LinkedIn Category', options=('LinkedIn Information Security', 'LinkedIn Software Engineering'), placeholder='Choose a Degree')

def main(deg):
         
    newDF, csvName = userChoices(deg)
    createWordcloud(csvName)
    createPlot(newDF,csvName)


def userChoices(deg):
    if deg == "LinkedIn Information Security":
        csv_name = 'data/Appended_Skills_IS.csv'
        newDF= pd.read_csv(csv_name)
    else:
        csv_name = 'data/Appended_Skills_SE.csv'
        newDF= pd.read_csv(csv_name)

    return newDF, csv_name

# = = = WORD CLOUD = = =
def construct_words(df):
    curr_words = []
    for index, values in df.iterrows():
        curr_words.append(dict(text = values["skill"], value = values["count"], type = values["type"], count = values["count"], category = values["category"]))
    return curr_words

def createWordcloud(csvName):
    allSkills = pd.read_csv('../skills-classifier/data/allSkill.csv')
    if 'IS' in csvName:
        hSkill = allSkills[(allSkills["category"] == "IS") & (allSkills["type"] == "hard_skill")].sort_values(by = 'count', ascending = False)
        sSkill = allSkills[(allSkills["category"] == "IS") & (allSkills["type"] == "soft_skill")].sort_values(by = 'count', ascending = False)
    elif 'SE' in csvName:
        hSkill = allSkills[(allSkills["category"] == "SE") & (allSkills["type"] == "hard_skill")].sort_values(by = 'count', ascending = False)
        sSkill = allSkills[(allSkills["category"] == "SE") & (allSkills["type"] == "soft_skill")].sort_values(by = 'count', ascending = False)

    # display option bar
    option = st.selectbox(label='Choose Type of Skill', options=('Hard Skills', 'Soft Skills', 'Both'), placeholder='Type of Skill')
    words = []

    # filter by option
    if option == "Hard Skills":
        words += construct_words(hSkill)
    elif option == "Soft Skills":
        words += construct_words(sSkill)
    elif option == "Both":
        words += construct_words(hSkill)
        words += construct_words(sSkill)

    words = sorted(words, key=lambda x: x['count'], reverse=True)
    # word cloud
    return_obj = wordcloud.visualize(words, tooltip_data_fields={
        'text': 'Skill', 'value':'Total skill count',  'type': "Skill type"
    }, padding=2, max_words = 70, palette='Dark2', per_word_coloring=False, height='25em')
    
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
    result_df = new_df.copy()  # Create a copy of the original DataFrame
    result_df['Extracted Skills'] = skills_split  # Add the split skills as a new column
        
    new_skills = result_df.explode('Extracted Skills') 
    
    # Group using Extracted Skills column, count occurence of each Seniority, unstack - set Extracted Skills as index, each unique seniority as column. fill null value with 0
    finalDF = new_skills.groupby('Extracted Skills')['Seniority'].value_counts().unstack(fill_value=0)

    # Reset the index to make "Extracted Skills" a regular column
    finalDF = finalDF.reset_index()
    finalDF.columns.name = None # remove index column name

        # Create a new column to sum
    finalDF['Total'] = finalDF[finalDF.columns[1:]].sum(axis=1)
    # sort by Highest > Lowest sum
    finalDF = finalDF.sort_values(by='Total', ascending=False)
    finalDF = finalDF.drop(columns='Total')
    finalDF = finalDF.reset_index(drop=True)
    # print(sorted_df)

    col1, space, col2 = st.columns([6,1,9])
   
    with col1: 
    # df skills
        dfSkills = finalDF['Extracted Skills']
        num_skills_to_display = st.slider("Number of Skills to Display", 1, 50 , 25) # 1 - lowest , 50 - max , 5 - default
        # Create a list of all seniority levels for default selection
        all_seniorities = finalDF.columns.to_list()
        all_seniorities = all_seniorities[1:]
        # Custom order for sorting
        custom_order = {'Internship': 0, 'Entry level': 1, 'Associate': 2, 'Mid-Senior level': 3, 'Director': 4, 'Executive': 5}
    # Sort the list based on the custom order
        all_seniorities = sorted(all_seniorities, key=lambda x: custom_order.get(x, len(custom_order)))
        
    with col2:
        # Add a sidebar multi-select with default selection of all seniority levels
        selected_seniorities = st.multiselect("Select Seniority Levels", all_seniorities, all_seniorities)

    # SIT SKILLS
    if data2 == "data/Appended_Skills_IS.csv":
        schoolDf = pd.read_csv("data/ICT(IS)_Module_Description_Skills.csv")
        courseSelected = "Information Security"
    else:
        schoolDf = pd.read_csv("data/ICT(SE)_Module_Description_Skills.csv")
        courseSelected = "Software Engineering"
    
    schoolSkills = schoolDf["Skills"].to_list()
       
    schDf = finalDF[finalDF['Extracted Skills'].isin(schoolSkills)]

    st.header(f"LinkedIn's Top {courseSelected} Skills")
    fig1 = px.bar(finalDF.head(num_skills_to_display), x= selected_seniorities, y= dfSkills[:num_skills_to_display], width=720, height = 500, labels ={'x': 'Top Skills from LinkedIn Job Postings', 'variable': 'Seniority Level', 'value': 'Number of Occurrences', 'y': 'Skills'})    
    
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

    return finalDF















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
    job_df_list = []
    job_data = ['data/Appended_Skills_IS.csv','data/Appended_Skills_SE.csv']

    #read csv based on degree chosen
    if deg == 'LinkedIn Information Security':
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

