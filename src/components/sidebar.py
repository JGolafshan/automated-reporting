#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""

import streamlit as st


def sidebar():
    st.sidebar.title("📊 Report Generator")
    # Show the navigation
    # st.sidebar.page_link("pages/home.py", label="Home", icon=":material/home_filled:")
    st.sidebar.page_link("pages/report_generator.py", label="Create Report", icon=":material/create:")
    st.sidebar.page_link("pages/report.py", label="View Report", icon=":material/dashboard:")
