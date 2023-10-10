import streamlit as st
import pandas as pd
from Compare_Skills_Relevance import comparison1
from Individual_Job_Skills_Relevance import comparison2

# Add navigation options to the sidebar
selected_page = st.sidebar.radio("Navigation", ["Compare Skills", "Individual Job Skills Relevance"])

# LinkedIn Dataset
dataset1_names = {
        "LinkedIn Information Systems": "extracted/skills/skills_IS_cleaned_03-10-2023_14-53-44.csv",
        "LinkedIn Software Engineering": "extracted/skills/skills_SE_cleaned_03-10-2023_14-53-53.csv",
    }

# LinkedIn Cleaned Dataset With Skills Appended for Every Job
dataset1_Part2_names = {
        "LinkedIn Information Systems": "extracted/title_skill/appended_skill_IS_cleaned_03-10-2023_14-53-44.csv",
        "LinkedIn Software Engineering": "extracted/title_skill/appended_skill_SE_cleaned_03-10-2023_14-53-53.csv",
    }

# SIT Dataset
dataset2_names = {
        "SIT Information Systems": "sit_extracted/Information and Communications Technology (Information Security)_Module_Description_Skills.csv",
        "SIT Software Engineering": "sit_extracted/Information and Communications Technology (Software Engineering)_Module_Description_Skills.csv",
    }

selected_dataset2_name = st.sidebar.selectbox("Select SIT Degree", list(dataset2_names.keys()))
dataset2_file_path = dataset2_names[selected_dataset2_name]
df2 = pd.read_csv(dataset2_file_path)

# Display content based on the selected navigation option
if selected_page == "Compare Skills":
    selected_dataset1_name = st.sidebar.selectbox("Select linkedIn Category", list(dataset1_names.keys()))
    dataset1_file_path = dataset1_names[selected_dataset1_name]
    df1 = pd.read_csv(dataset1_file_path)

    comparison1(df1, df2)

elif selected_page == "Individual Job Skills Relevance":
    selected_dataset1_Part2_name = st.sidebar.selectbox("Select linkedIn Job Category",
                                                        list(dataset1_Part2_names.keys()))
    dataset1_Part2_file_path = dataset1_Part2_names[selected_dataset1_Part2_name]
    df1_part2 = pd.read_csv(dataset1_Part2_file_path)

    comparison2(df1_part2, df2)