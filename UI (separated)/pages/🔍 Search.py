
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title='Skill Search', 
    page_icon='🔍', 
    layout='wide'
    )

st.title('🔍 Skill Search')
st.sidebar.selectbox(label='Choose a Degree', options=('ICT(IS)', 'ICT(SE)'), placeholder='Choose a Degree')

try:

    text_search = st.text_input("Search Skills or Degree", value="")
    col1, col2 = st.columns(2)

    li_IS = pd.read_csv('LinkedIn/ICT(IS)_LinkedIn_Skills.csv').assign(Degree = 'ICT(IS)')
    li_SE = pd.read_csv('LinkedIn/ICT(SE)_LinkedIn_Skills.csv').assign(Degree = 'ICT(SE)')

    li_IS = li_IS[['Degree','Job Title','Skills']]
    li_SE = li_SE[['Degree','Job Title','Skills']]
    
    li_all = pd.concat([li_IS, li_SE], ignore_index=1)

    sit_IS = pd.read_csv('SIT/ICT(IS)_Module_Description_Skills.csv').assign(Degree = 'ICT(IS)')
    sit_SE = pd.read_csv('SIT/ICT(SE)_Module_Description_Skills.csv').assign(Degree = 'ICT(SE)')

    sit_IS = sit_IS[['Degree','Skills','Count']]
    sit_SE = sit_SE[['Degree','Skills','Count']]   

    sit_all = pd.concat([sit_IS, sit_SE], ignore_index=1)

    if text_search == '':
        with col1:
            st.write('#')
            st.subheader('LinkedIn Job Descriptions and Skills')
            st.dataframe(li_all, width=850, hide_index=True)

        with col2:
            st.write('#')
            st.subheader('SIT Modules Descriptions and Skills')
            st.dataframe(sit_all, width=850, hide_index=True)            

    else: 
        with col1:
            st.write('#')
            st.subheader('LinkedIn Job Descriptions and Skills')
            li_1 = li_all["Skills"].str.contains(text_search)
            li_2 = li_all["Degree"].str.contains(text_search)
            li_3 = li_all["Job Title"].str.contains(text_search)
            li_search = li_all[li_1 | li_2 | li_3]

            # Show the results, if you have a text_search
            if text_search:
                st.dataframe(li_search, width=850, hide_index=True)

        with col2:
            st.write('#')
            st.subheader('SIT Modules Descriptions and Skills')
            sit_1 = sit_all["Skills"].str.contains(text_search)
            sit_2 = sit_all["Degree"].str.contains(text_search)
            sit_search = sit_all[sit_1 | sit_2]

            # Show the results, if you have a text_search
            if text_search:
                st.dataframe(sit_search, width=850, hide_index=True)

except Exception:
    st.write('Oops, no match found')
