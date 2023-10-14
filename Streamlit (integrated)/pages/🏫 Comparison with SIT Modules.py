
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


    ## graph moved to linkedin page
    # st.header(f"LinkedIn's Top {courseSelected} Skills")
    # fig1 = px.bar(sorted_filtered_df.head(num_skills_to_display), x= selected_seniorities, y= dfSkills[:num_skills_to_display], labels ={'y': 'Top Skills from LinkedIn Job Postings', 'variable': 'Seniority Level', 'value': 'count'})
    # st.plotly_chart(fig1, use_container_width=True)

    #panda series to dataframe
    countJobs = jobDF['Seniority'].value_counts().reset_index()
    result = ""
    for index, row in countJobs.iterrows():
        seniority_level = row['Seniority']
        count = row['count']
        if result:  # Add a comma and space if result is not empty
            result += ", "
        result += f"{seniority_level} -{count} Jobs"

    # st.caption(f"Disclaimer: {result}")
        
    schoolSkills = schoolDf["Skills"].to_list()
    
    schDf = sorted_filtered_df[sorted_filtered_df.index.isin(schoolSkills)]
    schDfSkills = schDf.index
    fig = px.bar(schDf.head(num_skills_to_display), x= selected_seniorities, y= schDfSkills[:num_skills_to_display], height= 500, labels ={'y': f'Top Skills from \nLinkedIn taught in SIT {courseSelected}', 'variable': 'Seniority Level', 'value': 'Number of Occurrences'})
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Disclaimer: {result}")

    st.write('#')
    # st.header("What are some other skills I can develop outside of SIT?")
    # suggestPlot(sorted_filtered_df,schDf)

    return sorted_df

def suggestPlot(data1, data2):
    linkedinDf = data1
    sitDf = data2
    # combine both dataframe
    diffDf = pd.concat([linkedinDf,sitDf])
    # remove duplicates , keeping only the uncommon skills
    diffDf = diffDf.drop_duplicates(keep=False)
    all_seniorities = diffDf.columns.to_list()
    # create a new Column for sum of all senority levels
    diffDf['Total'] = diffDf[all_seniorities].sum(axis=1)
    # remove individual seniority levels
    diffDf = diffDf.drop(columns=all_seniorities)
    # create Skills column , referencing value from index
    diffDf['Skills']=diffDf.index
    diffDf = diffDf.reset_index(drop=True) #reset index
    # Sidebar slider to select the number of skills to display
    num_skills_to_display = st.slider("Pie Chart Slider", 1, 50, 20)

    filtered_df = diffDf.head(num_skills_to_display)
    
    # Create a pie chart
    fig = px.pie(filtered_df, names='Skills', values='Total', title='Skills to Explore', height=500, width=800)

    # Display the pie chart
    # st.plotly_chart(fig)
    st.write('#')
    # skills in text format
    st.subheader('Top Skills to develop outside of SIT curriculum', divider='rainbow')
    for num in range(num_skills_to_display):
    #iloc is to search by column
        st.write(f"Skill {num+1} : {diffDf.iloc[num]['Skills']}")





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
