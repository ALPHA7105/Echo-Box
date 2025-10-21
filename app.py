import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Student Suggestion Box", layout="centered")
st.title("📝 Student Suggestion Box")

# --- Form ---
st.header("Submit Your Suggestion")
with st.form("suggestion_form"):
    category = st.selectbox("Category", ["Academics", "Facilities", "Events", "Teachers", "Other"])
    suggestion = st.text_area("Your Suggestion")
    submitted = st.form_submit_button("Submit")

if submitted and suggestion.strip() != "":
    # Append to CSV
    df = pd.DataFrame([[datetime.now(), category, suggestion]],
                      columns=["Time", "Category", "Suggestion"])
    df.to_csv("suggestions.csv", mode='a', header=False, index=False)
    st.success("✅ Suggestion submitted successfully!")

st.header("📊 Dashboard - View Suggestions")
# Load CSV
try:
    data = pd.read_csv("suggestions.csv", names=["Time", "Category", "Suggestion"])
    st.dataframe(data)

    # Category counts
    category_counts = data['Category'].value_counts()
    st.subheader("Suggestions by Category")
    st.bar_chart(category_counts)

except FileNotFoundError:
    st.info("No suggestions yet!")
