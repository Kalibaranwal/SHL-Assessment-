import streamlit as st
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("🧠 SHL Assessment Recommendation Engine")


# SHL Data

data = [
    {
        "Assessment_name": "Global Skills Development Report",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/global-skills-development-report/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "Not Given",
        "Test_type": "Ability & Aptitude, Biodata & Situational Judgement, Competencies, Development & 360, Assessment Exercises, Personality & Behavior"
    },
    {
        "Assessment_name": ".NET Framework 4.5",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/net-framework-4-5/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "30 minutes",
        "Test_type": "Knowledge & Skills"
    },
    {
        "Assessment_name": ".NET MVC(New)",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/net-mvc-new/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "17 minutes",
        "Test_type": "Knowledge & Skills"
    },
    {
        "Assessment_name": ".NET MVVM(New)",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/net-mvvm-new/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "5 minutes",
        "Test_type": "Knowledge & Skills"
    },
    {
        "Assessment_name": ".NET WCF(New)",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/net-wcf-new/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "11 minutes",
        "Test_type": "Knowledge & Skills"
    },
    {
        "Assessment_name": ".NET WPF(New)",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/net-wpf-new/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "9 minutes",
        "Test_type": "Knowledge & Skills"
    },
    {
        "Assessment_name": ".NET XAML(New)",
        "URL": "https://www.shl.com/solutions/products/product-catalog/view/net-xaml-new/",
        "Remote_testing": "Yes",
        "Adaptive_Support": "No",
        "Duration": "5 minutes",
        "Test_type": "Knowledge & Skills"
    },
]

df = pd.DataFrame(data)


# Helper functions


def parse_duration(duration):
    match = re.search(r"(\d+)", duration)
    return int(match.group(1)) if match else None

def extract_info(query):
    skills = re.findall(r'\b(Python|JavaScript|SQL|Java|C#|.NET|React|Cognitive|Personality)\b', query, re.IGNORECASE)
    skills = list(set([skill.lower() for skill in skills]))  # normalize
    duration_match = re.search(r'(\d+)\s*minutes', query)
    max_duration = int(duration_match.group(1)) if duration_match else None
    return skills, max_duration

def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        st.error(f"Error reading URL: {e}")
        return ""

def recommend_assessments(df, skills, max_duration):
    recommendations = []
    for _, row in df.iterrows():
        test_skills = row["Assessment_name"].lower() + " " + row["Test_type"].lower()
        duration = parse_duration(row["Duration"])
        if skills and not any(skill in test_skills for skill in skills):
            continue
        if max_duration is not None and duration is not None and duration > max_duration:
            continue
        recommendations.append(row)
    return pd.DataFrame(recommendations[:10])  # Max 10 results


# Streamlit Interface

user_input = st.text_area("Enter a job description (or paste a URL to one):", height=200)

if st.button("🔍 Recommend Assessments"):
    if user_input:
        if user_input.startswith("http"):
            user_query = get_text_from_url(user_input)
        else:
            user_query = user_input

        skills_needed, time_limit = extract_info(user_query)

        st.success(f"✅ Extracted Skills: {', '.join(skills_needed) if skills_needed else 'None'}")
        st.info(f"⏱️ Max Duration: {time_limit if time_limit else 'Not specified'} minutes")

        recommended_df = recommend_assessments(df, skills_needed, time_limit)

        if not recommended_df.empty:
            st.subheader("🔎 Recommended SHL Assessments")
            for _, row in recommended_df.iterrows():
                st.markdown(f"### [{row['Assessment_name']}]({row['URL']})")
                st.markdown(f"**Remote Testing:** {row['Remote_testing']} | **Adaptive Support:** {row['Adaptive_Support']}")
                st.markdown(f"**Duration:** {row['Duration']}  \n**Test Type:** {row['Test_type']}")
                st.markdown("---")
        else:
            st.warning("❌ No relevant assessments found based on your input.")
    else:
        st.warning("⚠️ Please enter a job description or URL.")
