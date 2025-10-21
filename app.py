# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Page Config ---
st.set_page_config(
    page_title="EchoBox",
    layout="centered",
    page_icon="📝"
)

# --- Sidebar ---
st.sidebar.title("EchoBox")
st.sidebar.caption("Anonymous Student Suggestion Box")
if "page" not in st.session_state:
    st.session_state.page = "submit"  # default page

# --- Sidebar Buttons ---
if st.sidebar.button("Submit Suggestion"):
    st.session_state.page = "submit"
if st.sidebar.button("Dashboard"):
    st.session_state.page = "dashboard"

page = st.session_state.page
# --- Main Title ---
st.markdown(
    """
    <h1 style='text-align: center; font-size: 48px;'>📝 EchoBox</h1>
    <br>
    """,
    unsafe_allow_html=True
)
st.markdown("Got an idea to make our school better? Share it here! Every suggestion counts and could spark real change — anonymously and safely.")
st.markdown("---")

# --- CSV File Setup ---
CSV_FILE = "suggestions.csv"
if not os.path.exists(CSV_FILE):
    # create empty CSV with headers
    pd.DataFrame(columns=["Time", "Category", "Suggestion"]).to_csv(CSV_FILE, index=False)

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
            st.markdown("---")
            for i, row in display_data.iterrows():
                st.markdown(f"**[{row['Category']}]** {row['Suggestion']}")
                if st.button(f"Delete response"):
                    data = data.drop(row.name)
                    data.to_csv(CSV_FILE, mode='w', header=False, index=False)
                    st.rerun()
                st.markdown("---")

            st.subheader("Suggestions by Category")
            if not data.empty:
                category_counts = data['Category'].value_counts()
                st.bar_chart(category_counts)

    except FileNotFoundError:
        st.info("No suggestions submitted yet.")


st.markdown("---")

st.markdown(
    """
    <p style="text-align:center; font-size:14px; color:gray;">
    🛠️ EchoBox - Student Suggestion Box <br>
    Developed by: <strong>Sarvesh Kore</strong> <br>
    For: Dunes Interschool Hackathon 3.0 <br>
    &copy; 2025
    </p>
    """, 
    unsafe_allow_html=True
)
