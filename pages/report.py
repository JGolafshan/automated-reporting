#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""
import datetime

import streamlit as st
from src.core.data_export import HTMLReportGenerator
from src.core.dataframe_functions import *
from src.core.utils import set_page_state, create_temp_html
from subprocess import check_output

# Load Components
set_page_state("pages/report.py")
st.title("Generated Report")

if "df_exception" in st.session_state and "df_missed" in st.session_state and "df_roster" in st.session_state:
    st.info("Review the filter data")

    # Load datasets
    raw_df_roster = st.session_state.df_roster
    raw_df_exception = st.session_state.df_exception
    raw_df_missed = st.session_state.df_missed

    cleaned_df_roster = clean_roster_dataframe(raw_df_roster)

    data_tabs = st.tabs([
        st.session_state.get('exception_filename', 'Exception Data'),
        st.session_state.get('missed_filename', 'Missed Meals Data')
    ])

    with data_tabs[0]:
        table_data, filter_data = st.columns([9,2])
        with table_data:
            st.subheader("Exception Data")
            cleaned_exception_df = clean_exception_dataframe(raw_df_exception)

            joined_exception_df = join_roster_df(cleaned_exception_df, cleaned_df_roster)
            filter_exception_df = filter_exception_dataframe(joined_exception_df)
            filter_exception_df = filter_exception_df.sort_values(by="Supervisor Name")

            complete_exception_df = finalised_exception_dataframe(filter_exception_df)
            exception_data_editor = st.data_editor(complete_exception_df, num_rows="dynamic", use_container_width=True)
        with filter_data:
            st.write("ss")

    with data_tabs[1]:
        st.subheader("Missed Meals Data")
        cleaned_mm_df = clean_missing_meal_dataframe(raw_df_missed)

        filtered_missed_df = filter_missing_meal_dataframe(cleaned_mm_df)
        filtered_missed_df["include"] = True
        filtered_missed_df = filtered_missed_df.sort_values(by="Supervisor Name")
        complete_mm_df = finalised_mm_dataframe(filtered_missed_df)

        mm_data_editor = st.data_editor(complete_mm_df, num_rows="dynamic", use_container_width=True)

    st.divider()

    html_output = HTMLReportGenerator()

    final_df = mm_data_editor[mm_data_editor["include"] == True]
    final_df = final_df[["Employee ID", "Employee Name", "Supervisor Name", "Shift Type"]]

    mm_table = html_output.create_table(final_df, "Missed Mails")

    html_output.add_component(mm_table)

    counts = finalised_mm_dataframe(mm_data_editor)["Shift Type"].value_counts()
    summary_str = f"Day - {counts.get('Day Shift', 0)}, Night - {counts.get('Night Shift', 0)}, Other - {counts.get('Other', 0)}"
    html_output.add_component(html_output.create_tag(
        tag_name="h4",
        classname="summary_stats",
        id_name="",
        style="",
        contents=summary_str)
    )

    html_output.add_component(html_output.create_tag("hr", "", "", "", ""))

    exception_table = html_output.create_table(exception_data_editor, "Early In")
    html_output.add_component(exception_table)
    final_exeception_df = finalised_exception_dataframe(exception_data_editor)


    copy = final_exeception_df.copy()
    copy["Amount Exceptions"] = final_exeception_df["Amount Exceptions"] + ":00"
    copy["Amount Exceptions"] = pd.to_timedelta(copy["Amount Exceptions"])
    total_time = copy["Amount Exceptions"].sum()
    total_minutes = total_time.total_seconds() // 60



    total_time_contents = f"Total Time: {total_minutes} Minutes"
    html_output.add_component(html_output.create_tag(
        tag_name="h4",
        classname="summary_stats",
        id_name="",
        style="",
        contents=total_time_contents)
    )
    html_output.add_component(html_output.create_tag("hr", "", "", "", ""))

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
        st.download_button("Download HTML", data=html_content,
                           file_name=f"report - {datetime.datetime.now().date()}.html", mime="text/html")

    with cols[1]:
        if st.button('Open HTML'):
            check_output("start " + create_temp_html(html_content), shell=True)

else:
    st.warning("❗ Please upload both files on the Report Generator page first.")
