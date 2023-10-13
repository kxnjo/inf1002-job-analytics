
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
# st.sidebar.selectbox(label='Choose a Degree', options=('ICT(IS)', 'ICT(SE)', 'All'), placeholder='Choose a Degree')



# li_IS = pd.read_csv('LinkedIn/ICT(IS)_LinkedIn_Skills.csv').assign(Degree = 'ICT(IS)')
# li_SE = pd.read_csv('LinkedIn/ICT(SE)_LinkedIn_Skills.csv').assign(Degree = 'ICT(SE)')

# li_IS = li_IS[['Degree','Job Title','Skills']]
# li_SE = li_SE[['Degree','Job Title','Skills']]

# li_all = pd.concat([li_IS, li_SE], ignore_index=1)

# sit_IS = pd.read_csv('SIT/ICT(IS)_Module_Description_Skills.csv').assign(Degree = 'ICT(IS)')
# sit_SE = pd.read_csv('SIT/ICT(SE)_Module_Description_Skills.csv').assign(Degree = 'ICT(SE)')

# sit_IS = sit_IS[['Degree','Skills','Count']]
# sit_SE = sit_SE[['Degree','Skills','Count']]   

# sit_all = pd.concat([sit_IS, sit_SE], ignore_index=1)

try:

    col1, col2 = st.columns(2)

    # LinkedIn Cleaned Dataset With Skills Appended for Every Job
    dataset1_Part2_names = {
            "LinkedIn Information Systems": "data/Appended_Skills_IS.csv",
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

    # if text_search == '':
    #     with col1:
    #         st.write('#')
    #         st.subheader('LinkedIn Job Descriptions and Skills')
    #         st.dataframe(li_all, width=850, hide_index=True)

    #     with col2:
    #         st.write('#')
    #         st.subheader('SIT Modules Descriptions and Skills')
    #         st.dataframe(sit_all, width=850, hide_index=True)            

    # else: 
    #     with col1:
    #         st.write('#')
    #         st.subheader('LinkedIn Job Descriptions and Skills')
    #         li_1 = li_all["Skills"].str.contains(text_search)
    #         li_2 = li_all["Degree"].str.contains(text_search)
    #         li_3 = li_all["Job Title"].str.contains(text_search)
    #         li_search = li_all[li_1 | li_2 | li_3]

    #         # Show the results, if you have a text_search
    #         if text_search:
    #             st.dataframe(li_search, width=850, hide_index=True)

    #     with col2:
    #         st.write('#')
    #         st.subheader('SIT Modules Descriptions and Skills')
    #         sit_1 = sit_all["Skills"].str.contains(text_search)
    #         sit_2 = sit_all["Degree"].str.contains(text_search)
    #         sit_search = sit_all[sit_1 | sit_2]

    #         # Show the results, if you have a text_search
    #         if text_search:
    #             st.dataframe(sit_search, width=850, hide_index=True)

except Exception:
    st.write('Oops, no match found')
