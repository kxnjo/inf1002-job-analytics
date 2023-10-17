
import sys
sys.path.append('Scripts')
import streamlit as st
import pandas as pd
import plotly.express as px
from Compare_Skills_Relevance import comparison1


st.set_page_config(
    page_title='SIT Skills and Job Analysis', 
    page_icon='🔍', 
    layout='wide'
    )

st.title('🏫 Comparison')

def main(LinkedInchoice, SITchoice):

    newDF, csvName = userChoices(LinkedInchoice)
    createPlot(newDF,csvName, SITchoice)

def userChoices(choice):
    if choice == "LinkedIn Software Engineering":
        csv_name = 'data/Appended_Skills_SE.csv'
        newDF= pd.read_csv(csv_name)
    else:
        csv_name = 'data/Appended_Skills_IS.csv'
        newDF= pd.read_csv(csv_name)
    return newDF, csv_name
    
def createPlot(data1, data2, selected_dataset2_name):



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
    finalDF = finalDF.set_index('Extracted Skills')

    # SIT SKILLS
    if data2 == "data/Appended_Skills_SE.csv":
        courseSelected = "Software Engineering"
    else:
        courseSelected = "Information Security"

    # SIT SKILLS
    
    #selected_dataset2_name is the SIT Degree selection on the sidebar
    if courseSelected == "Software Engineering" and selected_dataset2_name == "ICT(SE)":
        schoolDf = pd.read_csv("data/ICT(SE)_Module_Description_Skills.csv")
    elif courseSelected == "Software Engineering" and selected_dataset2_name == "ICT(IS)":
        schoolDf = pd.read_csv("data/ICT(IS)_Module_Description_Skills.csv")
    elif courseSelected == "Information Security" and selected_dataset2_name == "ICT(IS)":
        schoolDf = pd.read_csv("data/ICT(IS)_Module_Description_Skills.csv")
    elif courseSelected == "Information Security" and selected_dataset2_name == "ICT(SE)":
        schoolDf = pd.read_csv("data/ICT(SE)_Module_Description_Skills.csv")        

    st.header(f"Comparison between {courseSelected} LinkedIn Skills and {selected_dataset2_name}")
  
    col1, space, col2 = st.columns([6,1,9])
   
    with col1: 
    # df skills
        dfSkills = finalDF.index
        num_skills_to_display = st.slider("Number of Skills to Display", 1, 50 , 25) # 1 - lowest , 50 - max , 5 - default
        # Create a list of all seniority levels for default selection
        all_seniorities = finalDF.columns.to_list()
        # Custom order for sorting
        custom_order = {'Internship': 0, 'Entry level': 1, 'Associate': 2, 'Mid-Senior level': 3, 'Director': 4, 'Executive': 5}
    # Sort the list based on the custom order
        all_seniorities = sorted(all_seniorities, key=lambda x: custom_order.get(x, len(custom_order)))
    with col2:
        # Add a sidebar multi-select with default selection of all seniority levels
        selected_seniorities = st.multiselect("Select Seniority Levels", all_seniorities, all_seniorities)

    # Filter the DataFrame based on selected seniority levels
    filtered_df = finalDF[selected_seniorities]

    # Sort the DataFrame in descending order by the sum of selected seniority levels
    sorted_filtered_df = filtered_df.loc[filtered_df.sum(axis=1).sort_values(ascending=False).index]

    #panda series to dataframe
    countJobs = jobDF['Seniority'].value_counts().reset_index()
    result = ""
    for index, row in countJobs.iterrows():
        seniority_level = row['Seniority']
        count = row['count']
        if result:  # Add a comma and space if result is not empty
            result += ", "
        result += f"{seniority_level} -{count} Jobs"

        
    schoolSkills = schoolDf["Skills"].to_list()
    
    schDf = sorted_filtered_df[sorted_filtered_df.index.isin(schoolSkills)]
    schDfSkills = schDf.index
    fig = px.bar(schDf.head(num_skills_to_display), x= selected_seniorities, y= schDfSkills[:num_skills_to_display], height= 500, labels ={'y': 'Top Skills from LinkedIn taught in SIT ', 'variable': 'Seniority Level', 'value': 'Number of Occurrences'})
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Disclaimer: {result}")

    st.write('#')


    return finalDF


try:
    # selected_page = st.sidebar.radio("Navigation", ["Compare Skills", "Individual Job Skills Relevance"])

    # LinkedIn Dataset
    dataset1_names = {
            "LinkedIn Information Security": "data/LinkedIn_Skills_IS.csv",
            "LinkedIn Software Engineering": "data/LinkedIn_Skills_SE.csv",
        }

    # SIT Dataset
    dataset2_names = {
            "ICT(IS)": "data/ICT(IS)_Module_Description_Skills.csv",
            "ICT(SE)": "data/ICT(SE)_Module_Description_Skills.csv",
        }

    # Display content based on the selected navigation option

    selected_dataset1_name = st.sidebar.selectbox("Select LinkedIn Category", list(dataset1_names.keys()))
    dataset1_file_path = dataset1_names[selected_dataset1_name]
    df1 = pd.read_csv(dataset1_file_path)

    selected_dataset2_name = st.sidebar.selectbox("Select SIT Degree", list(dataset2_names.keys()))
    dataset2_file_path = dataset2_names[selected_dataset2_name]
    df2 = pd.read_csv(dataset2_file_path)

    comparison1(df1, df2)

    # Johnathan's functions
    main(selected_dataset1_name, selected_dataset2_name)
    
except Exception:
    st.write('Oops, no match found')
