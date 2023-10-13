import streamlit as st
import plotly.express as px


def comparison1(df1, df2):
    # PART 1 TO COMPARE SKILLS
    st.title("Compare Skills Relevance")

    df1 = df1.rename(columns={'0': 'Count'})

    # Allow the user to select the number of top skills from dataset 1 to compare
    n_top_skills_options = list(range(50, len(df1) + 1, 50))
    n_top_skills = st.selectbox("Select the number of top N skills from linkedIn list to compare", n_top_skills_options)

    # Calculate the top n skills in dataset 1
    top_skills_df1 = df1.nlargest(n_top_skills, 'Count')

    # Find skills in both datasets
    common_skills = set(top_skills_df1['Skills']).intersection(set(df2['Skills']))

    # Calculate percentages
    percentage_common = (len(common_skills) / n_top_skills) * 100
    percentage_not_in_df2 = 100 - percentage_common

    # Create a pie chart to visualize the percentages
    fig = px.pie(
        values=[percentage_common, percentage_not_in_df2],
        names=["Matching Skills", "Skills not taught in SIT"],
        title=f"Comparison for Top {n_top_skills} Demanded Skills",
        labels={"Matching Skills": "Common Skills", "Skills not taught in SIT": "Uncommon Skills"},
        color_discrete_sequence=['#C3B1E1', '#A7C7E7'],  # Custom color palette
    )

    # Adjust the height and width of the pie chart
    fig.update_layout(
        height=500,  # Set the height
        width=700,  # Set the width
        legend=dict(orientation="v", x=1.05, y=0.5)  # Move the legend to the right side
    )

    fig.update_traces(textinfo='percent+label', pull=[0.1, 0], hoverinfo='label+percent')

    st.plotly_chart(fig)

    # Create a filter to display matched skills from dataset 2
    show_matched_skills = st.checkbox("Show skills taught in SIT", value=False)

    if show_matched_skills:
        matched_skills_df2 = df2[df2['Skills'].isin(common_skills)]
        st.subheader("Skills Taught in SIT")

        # Add a numbered column for matched skills
        matched_skills_df2.reset_index(drop=True, inplace=True)
        matched_skills_df2.index = matched_skills_df2.index + 1

        # Pagination for matched skills
        matched_page = st.number_input("Page:", min_value=1,
                                       max_value=(len(matched_skills_df2) // 5) + 1, step=1, value=1)
        matched_start_idx = (matched_page - 1) * 5
        matched_end_idx = matched_start_idx + 5

        # Display the table of matched skills for the current page
        st.table(matched_skills_df2[['Skills', 'Count']].iloc[matched_start_idx:matched_end_idx])

        # Indicate the number of pages for matched skills
        st.write(f"Page {matched_page} of {((len(matched_skills_df2) - 1) // 5) + 1} pages")

    # Create a filter to display unmatched skills from dataset 1
    show_unmatched_skills_df1 = st.checkbox("Show skills not taught in SIT", value=False)

    if show_unmatched_skills_df1:
        unmatched_skills_df1 = top_skills_df1[~top_skills_df1['Skills'].isin(common_skills)]
        st.subheader("Relevant Skills Not Taught in SIT")

        # Add a numbered column for unmatched skills
        unmatched_skills_df1.reset_index(drop=True, inplace=True)
        unmatched_skills_df1.index = unmatched_skills_df1.index + 1

        # Pagination for unmatched skills
        unmatched_page = st.number_input("Page:", min_value=1,
                                         max_value=(len(unmatched_skills_df1) // 5) + 1, step=1, value=1)
        unmatched_start_idx = (unmatched_page - 1) * 5
        unmatched_end_idx = unmatched_start_idx + 5

        # Display the table of unmatched skills for the current page
        st.table(unmatched_skills_df1[['Skills', 'Count']].iloc[unmatched_start_idx:unmatched_end_idx])

        # Indicate the number of pages for unmatched skills
        st.write(f"Page {unmatched_page} of {((len(unmatched_skills_df1) - 1) // 5) + 1} pages")

