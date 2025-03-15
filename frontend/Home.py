import streamlit as st

st.set_page_config(page_title="Home", page_icon=":house:")

st.title("Welcome to the Cloud Service Provide Log Analyzer")

st.markdown("""
This application allows you to:
- **Upload JSON log files** from your cloud service provider.
- **Monitors metrics** such as network performance, CPU utilization, Memory Usage and Disk Usage per second.
""")

st.sidebar.success("Select a page above.")
