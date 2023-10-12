import pandas as pd
import matplotlib.pyplot as plt
import difflib
from classify_skills.py import classify_skill

# = = = IMPORT DATASETS = = =
# linkedin data
linkedin_IS_appended = pd.read_csv(
    "../extract_linkedIn_skills/cleaned_data/extracted/title_skill/appended_skill_IS_cleaned_03-10-2023_14-53-44.csv"
)
linkedin_SE_appended = pd.read_csv(
    "../extract_linkedIn_skills/cleaned_data/extracted/title_skill/appended_skill_SE_cleaned_03-10-2023_14-53-53.csv"
)

# SIT modules
# ictIS_modules = pd.read_csv("../sit_crawler/data/ICT(IS)_Module_Description_Skills.csv")
# ictSE_modules = pd.read_csv("../sit_crawler/data/ICT(SE)_Module_Description_Skills.csv")


# = = = CLEANING DATASETS (drop NA values) = = =
# remove NA values in seniority
linkedin_IS_appended = linkedin_IS_appended.dropna()
linkedin_SE_appended = linkedin_SE_appended.dropna()


# = = = CATEGORISE SKILL TYPE = = =
def categorize_skill_linkedin(df):
    overall_hard_skill = {}
    overall_soft_skill = {}
    for index, row in df.iterrows():
        curr_hSkill = []
        curr_sSkill = []
        # print(row['Extracted Skills'])
        skills_list = row["Extracted Skills"].split(",")

        for skill in skills_list:
            predict_skill_type = classify_skill(skill)
            if predict_skill_type == 1:
                curr_hSkill.append(skill)
                overall_hard_skill[skill] = (
                    overall_hard_skill[skill] + 1 if skill in overall_hard_skill else 1
                )
            else:  # predict_skill_type = 0
                curr_sSkill.append(skill)
                overall_soft_skill[skill] = (
                    overall_soft_skill[skill] + 1 if skill in overall_soft_skill else 1
                )

        df.at[index, "Hard Skill"] = ",".join(curr_hSkill)
        df.at[index, "Soft Skill"] = ",".join(curr_sSkill)

    return [df, overall_hard_skill, overall_soft_skill]


(
    categorised_IS,
    overall_hard_skill_IS,
    overall_soft_skill_IS,
) = categorize_skill_linkedin(linkedin_IS_appended)
(
    categorised_SE,
    overall_hard_skill_SE,
    overall_soft_skill_SE,
) = categorize_skill_linkedin(linkedin_SE_appended)

# = = = save into CSV for each type = = =
categorised_IS.to_csv("./data/categorised_IS.csv", encoding="utf-8")
categorised_SE.to_csv("./data/categorised_SE.csv", encoding="utf-8")

# = = = COMBINE ALL SKILLS INTO 1 DF = = =
df = pd.DataFrame(columns=["category", "skill", "type", "count"])
for skill, count in overall_hard_skill_IS.items():
    df = df.append(
        {"category": "IS", "skill": skill, "type": "hard_skill", "count": int(count)},
        ignore_index=True,
    )

for skill, count in overall_soft_skill_IS.items():
    df = df.append(
        {"category": "IS", "skill": skill, "type": "soft_skill", "count": int(count)},
        ignore_index=True,
    )

for skill, count in overall_hard_skill_SE.items():
    df = df.append(
        {"category": "SE", "skill": skill, "type": "hard_skill", "count": int(count)},
        ignore_index=True,
    )

for skill, count in overall_soft_skill_SE.items():
    df = df.append(
        {"category": "SE", "skill": skill, "type": "soft_skill", "count": int(count)},
        ignore_index=True,
    )

df.to_csv("./data/allSkill.csv")
