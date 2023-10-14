
import pandas as pd
from collections import OrderedDict 
import streamlit as st
import plotly.express as px
import sys
sys.path.append('Scripts')
import Individual_Job_Skills_Relevance as script


st.set_page_config(
    page_title='SIT Skills and Job Analysis', 
    page_icon='🔍', 
    layout='wide'
    )

st.title('🔍 Skill Search')

try:

    col1, col2 = st.columns(2)

    # LinkedIn Cleaned Dataset With Skills Appended for Every Job
    dataset1_Part2_names = {
            "LinkedIn Information Security": "data/Appended_Skills_IS.csv",
            "LinkedIn Software Engineering": "data/Appended_Skills_SE.csv",
        }

    # SIT Dataset
    dataset2_names = {
            "ICT(IS)": "data/ICT(IS)_Module_Description_Skills.csv",
            "ICT(SE)": "data/ICT(SE)_Module_Description_Skills.csv",
        }

    # Display content based on the selected navigation option
    
    selected_dataset1_Part2_name = st.sidebar.selectbox("Select LinkedIn Job Category",
                                                        list(dataset1_Part2_names.keys()))
    dataset1_Part2_file_path = dataset1_Part2_names[selected_dataset1_Part2_name]
    df1_part2 = pd.read_csv(dataset1_Part2_file_path)

    selected_dataset2_name = st.sidebar.selectbox("Select SIT Degree", list(dataset2_names.keys()))
    dataset2_file_path = dataset2_names[selected_dataset2_name]
    df2 = pd.read_csv(dataset2_file_path)

    script.comparison2(df1_part2, df2)

except Exception:
    st.write('Oops, no match found')
