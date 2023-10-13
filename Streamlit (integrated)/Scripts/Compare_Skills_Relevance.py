import streamlit as st
import plotly.express as px


def comparison1(df1, df2):
    # PART 1 TO COMPARE SKILLS
    st.header("Compare Skills Relevance at a Glance")

    df1 = df1.rename(columns={'0': 'Count'})

    # Allow the user to select the number of top skills from dataset 1 to compare
    n_top_skills = st.slider("Select the number of top N skills from LinkedIn list to compare", min_value=50, max_value=len(df1), step=50)

    # Calculate the top n skills in dataset 1
    top_skills_df1 = df1.nlargest(n_top_skills, 'Count')

    # Find skills in both datasets
    common_skills = set(top_skills_df1['Skills']).intersection(set(df2['Skills']))
    print(common_skills)

    num_common = len(common_skills)
    num_uncommon = len(top_skills_df1) - num_common

    # Calculate percentages
    percentage_common = (len(common_skills) / n_top_skills) * 100
    percentage_not_in_df2 = 100 - percentage_common

    # Create a pie chart to visualize the percentages
    fig = px.pie(
        values=[num_common, num_uncommon],
        names=["Matching Skills", "Skills not taught in SIT"],
        title=f"Comparison for Top {n_top_skills} Demanded Skills",
        labels={"Matching Skills": "Common Skills", "Skills not taught in SIT": "Uncommon Skills"},
        color_discrete_sequence=['#C3B1E1', '#A7C7E7'],  # Custom color palette
    )

    # Adjust the height and width of the pie chart
    fig.update_layout(
        height=600,  # Set the height
        width=700,  # Set the width
        legend=dict(orientation="v", x=1.05, y=0.5)  # Move the legend to the right side
    )

    fig.update_traces(textinfo='percent+label', pull=[0.1, 0], hoverinfo='label+percent')

    st.plotly_chart(fig)

    df2.sort_values('Count', ascending = False, inplace = True)
    matched_skills_df2 = df2[df2['Skills'].isin(common_skills)]

    # Add a numbered column for matched skills
    matched_skills_df2.reset_index(drop=True, inplace=True)
    matched_skills_df2.index = matched_skills_df2.index + 1
    
    st.subheader('Demanded skills found in SIT curriculum', divider='rainbow')
    with st.expander('See all Skills'):
        for num in range(len(matched_skills_df2)):
        #iloc is to search by column
            st.write(f"Skill {num+1} : {matched_skills_df2.iloc[num]['Skills']}")


    # Create a filter to display unmatched skills from dataset 1
    unmatched_skills_df1 = top_skills_df1[~top_skills_df1['Skills'].isin(common_skills)]

    # Add a numbered column for unmatched skills
    unmatched_skills_df1.reset_index(drop=True, inplace=True)
    unmatched_skills_df1.index = unmatched_skills_df1.index + 1

    st.subheader('Demanded skills to develop outside of SIT curriculum', divider='rainbow')
    with st.expander('See all Skills'):
        for num in range(len(unmatched_skills_df1)):
        #iloc is to search by column
            st.write(f"Skill {num+1} : {unmatched_skills_df1.iloc[num]['Skills']}")
