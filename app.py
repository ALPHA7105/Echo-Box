# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Page Config ---
st.set_page_config(
    page_title="EchoBox - Student Suggestion Box",
    layout="centered",
    page_icon="📝"
)

# --- Sidebar ---
st.sidebar.title("EchoBox")
st.sidebar.caption("Anonymous Student Suggestion Box")
# Optional: add school logo if you have one
# st.sidebar.image("logo.png", width=150)

# --- Main Title ---
st.title("📝 EchoBox: Submit Your Suggestion")
st.markdown("Help improve our school! Your suggestions are **anonymous** and valued.")

# --- CSV File Setup ---
CSV_FILE = "suggestions.csv"
if not os.path.exists(CSV_FILE):
    # create empty CSV with headers
    pd.DataFrame(columns=["Time", "Category", "Suggestion"]).to_csv(CSV_FILE, index=False)

# --- Suggestion Form ---
st.header("Submit a Suggestion")
with st.form("suggestion_form"):
    category = st.selectbox("Category", ["Academics", "Facilities", "Events", "Teachers", "Other"])
    suggestion = st.text_area("Your Suggestion")
    submitted = st.form_submit_button("Submit")

if submitted:
    if suggestion.strip() != "":
        # Append submission to CSV
        df = pd.DataFrame([[datetime.now(), category, suggestion]],
                          columns=["Time", "Category", "Suggestion"])
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
        st.success("✅ Suggestion submitted successfully!")
    else:
        st.error("❌ Please enter a suggestion before submitting.")

# --- Dashboard Section ---
st.header("📊 Dashboard - View Suggestions")
try:
    data = pd.read_csv(CSV_FILE, names=["Time", "Category", "Suggestion"])

    if data.empty:
        st.info("No suggestions submitted yet.")
    else:
        # Filter by category
        filter_cat = st.selectbox("Filter by Category", ["All"] + list(data['Category'].unique()))
        if filter_cat != "All":
            display_data = data[data['Category'] == filter_cat]
        else:
            display_data = data

        st.subheader("All Suggestions")
            for i, row in display_data.iterrows():
        st.markdown(f"**[{row['Category']}]** {row['Suggestion']}")
            if st.button(f"Delete row {i}"):
                # Remove the row from the main DataFrame
                data = data.drop(row.name)
                # Overwrite CSV
                data.to_csv(CSV_FILE, mode='w', header=False, index=False)
                st.experimental_rerun()  # refresh the page

        st.subheader("Suggestions by Category")
        category_counts = data['Category'].value_counts()
    st.bar_chart(category_counts)
    
except Exception as e:
    st.info("No suggestions submitted yet.")
