#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""

import streamlit as st
from src.core import utils
from src.components import sidebar

st.markdown(utils.load_css("assets/css/styles.css"), unsafe_allow_html=True)

pages = [
    # st.Page("pages/home.py", title="Home", icon=":material/show_chart:"),
    st.Page("pages/report_generator.py", title="Create Report", icon=":material/summarize:", url_path="/generate_report"),
    st.Page("pages/report.py", title="View Report", icon=":material/summarize:", url_path="report")
]



pg = st.navigation(pages, expanded=True)
sidebar.sidebar()

try:
    pg.run()
except Exception as e:
    st.header("Error")
    st.error(f"An unexpected error occurred. Redirecting to error page... \n\n {e.__str__()}")
