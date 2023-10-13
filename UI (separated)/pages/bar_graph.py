import pandas as pd
import streamlit as st
import plotly.express as px

def main():
    
    choice = st.radio( "**Choose SE/IS**", #radio button to toggle between SE/IS
        ["**Software Engineering**", "**Information Security**"], 
        captions = ["View the top skills for Software Engineering", "View the top skills for Information Security"])     
    newDF, csvName = userChoices(choice)

    createPlot(newDF,csvName)

def userChoices(choice):
    if choice == "**Software Engineering**":
        csv_name = 'extract_linkedIn_skills/cleaned_data/extracted/title_skill/appended_skill_SE_cleaned_03-10-2023_14-53-53.csv'
        newDF= pd.read_csv(csv_name)
    else:
        csv_name = 'extract_linkedIn_skills/cleaned_data/extracted/title_skill/appended_skill_IS_cleaned_03-10-2023_14-53-44.csv'
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
  
    # df skills
    dfSkills = sorted_df.index

    num_skills_to_display = st.sidebar.slider("Number of Skills to Display", 1, 50 , 25) # 1 - lowest , 50 - max , 5 - default
    # Create a list of all seniority levels for default selection
    all_seniorities = sorted_df.columns.to_list() #['Associate', 'Director', 'Entry level', 'Executive', 'Internship', 'Mid-Senior level']
    # re-arrange seniority from junior to senior
    all_seniorities = ['Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']


    # Add a sidebar multi-select with default selection of all seniority levels
    selected_seniorities = st.sidebar.multiselect("Select Seniority Levels", all_seniorities, all_seniorities)

    # Filter the DataFrame based on selected seniority levels
    filtered_df = sorted_df[selected_seniorities]

    # Sort the DataFrame in descending order by the sum of selected seniority levels
    sorted_filtered_df = filtered_df.loc[filtered_df.sum(axis=1).sort_values(ascending=False).index]

    # SIT SKILLS
    if data2 == "extract_linkedIn_skills/cleaned_data/extracted/title_skill/appended_skill_SE_cleaned_03-10-2023_14-53-53.csv":
        courseSelected = "Software Engineering"
    else:
        courseSelected = "Information Security"
    
    st.header(f"LinkedIn's Top {courseSelected} Skills")
    # fig1 = px.bar(sorted_filtered_df.head(num_skills_to_display), x= dfSkills[:num_skills_to_display], y= selected_seniorities, labels ={'x': 'Top Skills from LinkedIn Job Postings', 'variable': 'Seniority Level', 'value': 'count'})
    fig1 = px.bar(sorted_filtered_df.head(num_skills_to_display), x= selected_seniorities, y= dfSkills[:num_skills_to_display], labels ={'y': 'Top Skills from LinkedIn Job Postings', 'variable': 'Seniority Level', 'value': 'count'})
    
    st.plotly_chart(fig1, use_container_width=True)
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

    # checkbox to show/hide 2nd graph
    show_graph = st.checkbox("Show Comparison with SIT skills")
    
    if show_graph:
        # SIT SKILLS
        SITselected = st.selectbox("Choose SIT Course", options= ['Software Engineering', 'Information Security'])
        
        if courseSelected == "Software Engineering" and SITselected == "Software Engineering":
            schoolDf = pd.read_csv("extract_SIT_skills/data/Information and Communications Technology (Software Engineering)_Module_Description_Skills.csv")
        elif courseSelected == "Software Engineering" and SITselected == "Information Security":
            schoolDf = pd.read_csv("extract_SIT_skills/data/Information and Communications Technology (Information Security)_Module_Description_Skills.csv")
        elif courseSelected == "Information Security" and SITselected == "Information Security":
            schoolDf = pd.read_csv("extract_SIT_skills/data/Information and Communications Technology (Information Security)_Module_Description_Skills.csv")
        elif courseSelected == "Information Security" and SITselected == "Software Engineering":
            schoolDf = pd.read_csv("extract_SIT_skills/data/Information and Communications Technology (Software Engineering)_Module_Description_Skills.csv")
        
        schoolSkills = schoolDf["Skills"].to_list()
       
        schDf = sorted_filtered_df[sorted_filtered_df.index.isin(schoolSkills)]
        schDfSkills = schDf.index
        fig = px.bar(schDf.head(num_skills_to_display), x= selected_seniorities, y= schDfSkills[:num_skills_to_display], labels ={'y': f'Top Skills from \nLinkedIn Job Postings taught in SIT {courseSelected}', 'variable': 'Seniority Level', 'value': 'Count'})
    
        st.subheader(f"Comparison between {courseSelected} LinkedIn Skills and SIT {SITselected}")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Disclaimer: {result}")

        show_More = st.checkbox("What are some other skills I can develop outside of SIT?")
        if show_More:
            suggestPlot(sorted_filtered_df,schDf)

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
    num_skills_to_display = st.sidebar.slider("Pie Chart Slider", 1, 50, 20)

    filtered_df = diffDf.head(num_skills_to_display)

    # Create a pie chart
    fig = px.pie(filtered_df, names='Skills', values='Total', title='Skills to Explore')

    # Display the pie chart
    st.plotly_chart(fig)
    # skills in text format
    st.subheader('Top Skills to develop outside of SIT curriculum', divider='rainbow')
    for num in range(num_skills_to_display):
    #iloc is to search by column
        st.write(f"The Top {num+1} Skill : {diffDf.iloc[num]['Skills']}")

main()