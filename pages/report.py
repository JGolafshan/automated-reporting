#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""

import pandas as pd
import streamlit as st
from src.core.data_export import HTMLReportGenerator
from src.core.utils import set_page_state, create_temp_html
from subprocess import check_output

file_name_roster = r"C:\Users\JGola\Desktop\Active_Roster_Detail_1743549472356"


def clean_exception_dataframe(dataframe):
    dataframe.rename(
        columns={'PERSONFULLNAME': 'Full Name', 'EMPLOYEEID': 'Employee ID'},
        inplace=True)
    dataframe = dataframe.dropna(how='all')
    dataframe = dataframe[:-2]

    dataframe["Employee ID"] = dataframe["Employee ID"].astype(int)
    dataframe["Amount Exceptions"] = dataframe["Scheduled"] - dataframe["Actual"]
    dataframe["Amount Exceptions"] = dataframe["Amount Exceptions"].dt.total_seconds() // 60
    return dataframe


def filter_exception_dataframe(dataframe):
    dataframe = dataframe[dataframe["EXCEPTIONTYPE"] == "EARLY"]
    dataframe = dataframe[dataframe["Amount Exceptions"] > 5]
    return dataframe


def finalised_exception_dataframe(filtered_df):
    selected_columns = filtered_df[["Employee ID", "Full Name", "Actual", "Scheduled", "Amount Exceptions"]]
    return selected_columns


def clean_missing_meal_dataframe(dataframe):
    pass


def filter_missing_meal_dataframe(dataframe):
    if dataframe is not None:
        df_filtered = dataframe[dataframe["Missed"] > 0]
        return df_filtered


def finalised_mm_dataframe(filtered_df):
    # Filter rows where include is True
    included_rows = filtered_df[filtered_df["include"] == True]

    # Then select the specific columns you want
    selected_columns = included_rows[["Empl ID", "Employee Name", "Shift Code", "Manager"]]
    return selected_columns


# Load Components
set_page_state("pages/report.py")
st.title("Generated Report")

if "df_exception" in st.session_state and "df_missed" in st.session_state:
    st.info("Review the filter data")

    # Load datasets
    raw_df_exception = st.session_state.df_exception
    raw_df_missed = st.session_state.df_missed

    data_tabs = st.tabs([
        st.session_state.get('exception_filename', 'Exception Data'),
        st.session_state.get('missed_filename', 'Missed Meals Data')
    ])

    with data_tabs[0]:
        st.subheader("Exception Data")
        cleaned_exception_df = clean_exception_dataframe(raw_df_exception)
        filter_exception_df = filter_exception_dataframe(cleaned_exception_df)
        st.dataframe(filter_exception_df, use_container_width=True)

    with data_tabs[1]:
        st.subheader("Missed Meals Data")
        filtered_missed_df = filter_missing_meal_dataframe(raw_df_missed)
        filtered_missed_df["include"] = True
        edited_df = st.data_editor(filtered_missed_df, num_rows="dynamic", use_container_width=True)

    st.divider()

    html_output = HTMLReportGenerator()
    mm_table = html_output.create_table(finalised_mm_dataframe(edited_df), "Missed Mails")
    html_output.add_component(mm_table)

    exception_table = html_output.create_table(finalised_exception_dataframe(filter_exception_df), "Early In")
    html_output.add_component(exception_table)

    # Output
    html_content = html_output.generate_html_report()

    with st.expander("Preview HTML", expanded=False):
        st.subheader("Expected Output")
        st.warning(
            "⚠️ Please note that the appearance may differ in the downloaded HTML file due to potential conflicts with existing styles.")

        # Render in Streamlit
        st.html(html_content)

    st.divider()

    # Optionally let user download it
    cols = st.columns([0.12, 0.10, 0.78])
    with cols[0]:
        st.download_button("Download HTML", data=html_content, file_name="report.html", mime="text/html")

    with cols[1]:
        if st.button('Open HTML'):
            check_output("start " + create_temp_html(html_content), shell=True)

else:
    st.warning("❗ Please upload both files on the Report Generator page first.")
