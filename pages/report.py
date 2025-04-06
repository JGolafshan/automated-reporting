#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""

import streamlit as st
from src.core.data_export import HTMLReportGenerator
from src.core.utils import set_page_state, create_temp_html
from subprocess import check_output


def filter_exception_dataframe():
    pass


def filter_missing_meal_dataframe(dataframe):
    if dataframe is not None:
        df_filtered = dataframe[dataframe["Missed"] > 0]
        return df_filtered


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
        st.dataframe(raw_df_exception, use_container_width=True)

    with data_tabs[1]:
        st.subheader("Missed Meals Data")
        filtered_missed_df = filter_missing_meal_dataframe(raw_df_missed)
        filtered_missed_df["include"] = True
        edited_df = st.data_editor(filtered_missed_df, num_rows="dynamic", use_container_width=True)

    st.divider()

    html_output = HTMLReportGenerator()
    mm_table = html_output.create_table(edited_df, "Missed Mails")
    html_output.add_component(mm_table)

    # Output
    html_content = html_output.generate_html_report()

    with st.expander("Preview HTML", expanded=False):
        st.subheader("Expected Output")
        st.warning("⚠️ Please note that the appearance may differ in the downloaded HTML file due to potential conflicts with existing styles.")

        # Render in Streamlit
        st.html(html_content)

    st.divider()

    # Optionally let user download it
    cols = st.columns([0.12, 0.10, 0.10, 0.68])
    with cols[0]:
        st.download_button("Download HTML", data=html_content, file_name="report.html", mime="text/html")

    with cols[1]:
        if st.button('Open HTML'):
            check_output("start " + create_temp_html(html_content), shell=True)

    with cols[2]:
        st.download_button("Download PDF", data=html_content, file_name="report.pdf", mime="application/pdf")

else:
    st.warning("❗ Please upload both files on the Report Generator page first.")
