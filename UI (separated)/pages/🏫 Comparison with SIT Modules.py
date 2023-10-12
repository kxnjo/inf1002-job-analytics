
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title='Comparison', 
    page_icon='🏫', 
    layout='wide'
    )

st.title('🏫 Comparison')
st.sidebar.selectbox(label='Choose a Degree for LinkedIn Jobs', options=('ICT(IS)', 'ICT(SE)'), placeholder='Choose a Degree')
st.sidebar.selectbox(label='Choose a Degree for SIT', options=('ICT(IS)', 'ICT(SE)'), placeholder='Choose a Degree')
st.sidebar.write('Chart 2[link](http://localhost:8501/Comparison_with_SIT_Modules#chart-2)', disabled=True, type='Primary')


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

try:
    # text_search = st.text_input("Search Skills or Degree", value="")
    st.subheader('Chart 1')
    fig = px.pie(sit_all, values='Count', names='Skills')
        # results_df = results_df.groupby(['Skills'])['Skills'].count().reset_index(name='Count')

    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Chart 2')
    fig = px.pie(sit_all, values='Count', names='Skills')
        # results_df = results_df.groupby(['Skills'])['Skills'].count().reset_index(name='Count')

    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Chart 3')
    fig = px.pie(sit_all, values='Count', names='Skills')
        # results_df = results_df.groupby(['Skills'])['Skills'].count().reset_index(name='Count')

    st.plotly_chart(fig, use_container_width=True)
    
except Exception:
    st.write('Oops, no match found')
