import streamlit as st

st.set_page_config(page_title="Home", page_icon=":house:")

st.title("Welcome to the Network Performance Monitoring App")

st.markdown("""
This application allows you to:
- **Upload JSON log files** from your cloud service provider.
- **Monitor real-time metrics** such as network performance, CPU utilization, and API calls per second.
""")

st.sidebar.success("Select a page above.")
