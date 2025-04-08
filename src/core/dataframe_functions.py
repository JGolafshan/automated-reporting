#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 07/04/2024
    Author: Joshua David Golafshan
"""
import datetime

import numpy as np
import pandas as pd


def join_roster_df(join, joinee):
    df_merged = join.merge(
        joinee[["Employee ID", "Supervisor Name", "Job Title", "Job Level"]],
        on="Employee ID",
        how="left"  # or "inner" depending on your use case
    )
    return df_merged


def clean_roster_dataframe(dataframe):
    dataframe.rename(
        columns={'Emp ID': 'Employee ID'},
        inplace=True)

    dataframe["Employee ID"] = dataframe["Employee ID"].astype(int)
    return dataframe


def clean_exception_dataframe(dataframe):
    dataframe.rename(
        columns={'PERSONFULLNAME': 'Employee Name', 'PERSONNUM': 'Employee ID'},
        inplace=True)
    dataframe = dataframe.dropna(how='all')
    dataframe = dataframe[:-2]

    dataframe["Employee ID"] = dataframe["Employee ID"].astype(int)
    dataframe["Amount Exceptions"] = dataframe["Scheduled"] - dataframe["Actual"]
    return dataframe


def filter_exception_dataframe(dataframe):
    dataframe = dataframe[dataframe["EXCEPTIONTYPE"] == "EARLY"]

    dataframe["Amount Exceptions"] = pd.to_timedelta(dataframe["Amount Exceptions"])
    dataframe["total_minutes"] = dataframe["Amount Exceptions"].dt.total_seconds() / 60
    cutoff_minutes = 5

    dataframe = dataframe[dataframe["total_minutes"] > cutoff_minutes]
    dataframe["Amount Exceptions"] = dataframe["Amount Exceptions"].apply(lambda x: str(x).split(' ')[2][:5])

    return dataframe


def finalised_exception_dataframe(filtered_df):
    selected_columns = filtered_df[
        ["Employee ID", "Employee Name", "Supervisor Name", "Job Title", "Job Level", "Actual", "Scheduled",
         "Amount Exceptions"]]
    return selected_columns


def clean_missing_meal_dataframe(dataframe):
    dataframe.rename(
        columns={'PERSONFULLNAME': 'Employee Name', 'Empl ID': 'Employee ID', "Manager": "Supervisor Name"},
        inplace=True)

    conditions = [
        dataframe["Shift Code"].str.startswith("N", na=False),
        dataframe["Shift Code"].str.startswith("D", na=False)
    ]

    choices = ["Night Shift", "Day Shift"]

    dataframe["Shift Type"] = np.select(conditions, choices, default="Other")
    return dataframe


def filter_missing_meal_dataframe(dataframe):
    if dataframe is not None:
        df_filtered = dataframe[dataframe["Missed"] > 0]
        return df_filtered


def finalised_mm_dataframe(filtered_df):
    # Filter rows where include is True
    included_rows = filtered_df[filtered_df["include"] == True]

    # Then select the specific columns you want
    selected_columns = included_rows[["include", "Employee ID", "Employee Name", "Supervisor Name", "Shift Type"]]
    return selected_columns
