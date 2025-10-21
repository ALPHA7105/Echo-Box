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
if st.sidebar.button("Submit Suggestion"):
    page = "submit"
elif st.sidebar.button("Dashboard"):
    page = "dashboard"
else:
    page = "submit"  # default page

# --- Main Title ---
st.title("📝 EchoBox: Submit Your Suggestion")
st.markdown("Got an idea to make our school better? Share it here! Every suggestion counts and could spark real change — anonymously and safely.")

# --- CSV File Setup ---
CSV_FILE = "suggestions.csv"
if not os.path.exists(CSV_FILE):
    # create empty CSV with headers
    pd.DataFrame(columns=["Time", "Category", "Suggestion"]).to_csv(CSV_FILE, index=False)

st.markdown("---")

# --- Suggestion Form ---
if page == "submit":
    st.header("Submit a Suggestion")
    st.markdown(
        "Got an idea to make our school better? Share it here! "
        "Every suggestion counts and could spark real change — anonymously and safely."
    )

    with st.form("suggestion_form"):
        category = st.selectbox("Category", ["Academics", "Facilities", "Events", "Teachers", "Other"])
        suggestion = st.text_area("Your Suggestion")
        submitted = st.form_submit_button("Submit")

    if submitted:
        if suggestion.strip() != "":
            df = pd.DataFrame([[datetime.now(), category, suggestion]],
                              columns=["Time", "Category", "Suggestion"])
            df.to_csv(CSV_FILE, mode='a', header=False, index=False)
            st.success("✅ Suggestion submitted successfully!")
        else:
            st.error("❌ Please enter a suggestion before submitting.")
st.mardown("---")

# --- Dashboard Section ---
if page == "dashboard":
    st.header("📊 Dashboard - View Suggestions")
    st.markdown("Below you can view all submitted suggestions, filter by category, and delete any if needed.")

    # Load CSV
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
                if st.button(f"Delete row {row.name}"):
                    data = data.drop(row.name)
                    data.to_csv(CSV_FILE, mode='w', header=False, index=False)
                    st.rerun()

            st.subheader("Suggestions by Category")
            if not data.empty:
                category_counts = data['Category'].value_counts()
                st.bar_chart(category_counts)

    except FileNotFoundError:
        st.info("No suggestions submitted yet.")
