import pandas as pd
import streamlit as st
import streamlit_wordcloud as wordcloud

allSkills = pd.read_csv("../skills-classifier/data/allSkill.csv")

hSkill_IS = allSkills[(allSkills["category"] == "IS") & (allSkills["type"] == "hard_skill")].sort_values(by = 'count', ascending = False)
sSkill_IS = allSkills[(allSkills["category"] == "IS") & (allSkills["type"] == "soft_skill")].sort_values(by = 'count', ascending = False)

hSkill_SE = allSkills[(allSkills["category"] == "SE") & (allSkills["type"] == "hard_skill")].sort_values(by = 'count', ascending = False)
sSkill_SE = allSkills[(allSkills["category"] == "SE") & (allSkills["type"] == "soft_skill")].sort_values(by = 'count', ascending = False)

# overallOption
overallOption = "SE"

def construct_words(df):
    curr_words = []
    for index, values in df.iterrows():
        print(values["skill"])
        curr_words.append(dict(text = values["skill"], value = values["count"], skill = values["skill"], count = values["count"], category = values["category"]))
    return curr_words

# multi select
options = st.multiselect('Select your category and skill type', ['Hard Skills', 'Soft Skills'], default=['Hard Skills', 'Soft Skills'])
words = []

if len(options) != 0:
    for i in options:
        if overallOption == "IS":
            if i == "Hard Skills":
                words += construct_words(hSkill_IS)
            elif i == "Soft Skills":
                words += construct_words(sSkill_IS)
        elif overallOption == "SE":
            if i == "Hard Skills":
                words += construct_words(hSkill_SE)
            elif i == "Soft Skills":
                words += construct_words(sSkill_SE)

words = sorted(words, key=lambda x: x['count'], reverse=True)
# word cloud
return_obj = wordcloud.visualize(words, tooltip_data_fields={
    'text': 'Skill', 'value':'Total skill count'
}, padding=2, max_words = 50, palette='Dark2', per_word_coloring=False)