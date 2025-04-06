#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""

import streamlit as st
from src.core.utils import set_page_state, handle_file_upload, read_file

# Load Components
set_page_state("pages/report_generator.py")

df_exception = None
df_missed = None
col1, col2 = st.columns(2)

# --- Exception File Upload ---
with col1:
    st.markdown("#### 1. Exception CSV")
    exception_file = st.file_uploader("Upload Exception CSV or Excel", type=["csv", "xls", "xlsx"], key="exception")

    if exception_file is None and "df_exception_file" in st.session_state:
        exception_file = st.session_state["df_exception_file"]

    # Read and handle the file (with skiprows=24)
    read_exception_data = read_file(exception_file, skip_rows=24) if exception_file else None
    df_exception = handle_file_upload(dataframe=read_exception_data, filename=exception_file, session_key="df_exception", label="Exception File")

# --- Missed Meals File Upload ---
with col2:
    st.markdown("#### 2. Missed Meals CSV")
    missed_meals_file = st.file_uploader("Choose the Missed Meals file", type=["csv", "xls", "xlsx"],
                                         key="missed_meals")

    if missed_meals_file is None and "df_missed_file" in st.session_state:
        missed_meals_file = st.session_state["df_missed_file"]

    read_missed_meals_data = read_file(missed_meals_file) if missed_meals_file else None
    df_missed = handle_file_upload(read_missed_meals_data, missed_meals_file, session_key="df_missed",
                                   label="Missed Meals File")
# --- Display Data and Submit ---
if df_exception is not None and df_missed is not None:
    data_tabs = st.tabs([
        st.session_state.get('exception_filename', 'Exception Data'),
        st.session_state.get('missed_filename', 'Missed Meals Data')
    ])

    with data_tabs[0]:
        st.subheader("Exception Data")
        st.dataframe(df_exception, use_container_width=True)

    with data_tabs[1]:
        st.subheader("Missed Meals Data")
        st.dataframe(df_missed, use_container_width=True)

    st.divider()

    if st.button("🚀 Submit and Generate Report", use_container_width=True):
        set_page_state("pages/report.py")
        st.switch_page("pages/report.py")
else:
    st.warning("⚠️ Please upload both files to continue.")
