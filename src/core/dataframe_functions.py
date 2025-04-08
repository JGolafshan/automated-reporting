#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Date: 07/04/2024
    Author: Joshua David Golafshan
"""

import datetime
import numpy as np
import pandas as pd
import streamlit as st


# ---------------------------
# Utility Functions
# ---------------------------

def safe_rename(df, rename_map):
    return df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})


def safe_int_column(df, col):
    df = df[pd.to_numeric(df[col], errors='coerce').notna()]
    df[col] = df[col].astype(int)
    return df


def format_timedelta_as_str(td):
    if pd.isna(td):
        return ""
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"{hours:02}:{minutes:02}"


# ---------------------------
# Data Cleaning Functions
# ---------------------------

def clean_roster_dataframe(df):
    df = safe_rename(df, {'Emp ID': 'Employee ID'})
    df = safe_int_column(df, "Employee ID")
    return df


def clean_exception_dataframe(df):
    df = safe_rename(df, {
        'PERSONFULLNAME': 'Employee Name',
        'PERSONNUM': 'Employee ID'
    })
    df = df.dropna(how='all')
    if len(df) > 2:
        df = df.iloc[:-2]
    df = safe_int_column(df, "Employee ID")
    df["Amount Exceptions"] = df["Scheduled"] - df["Actual"]
    return df


def clean_missing_meal_dataframe(df):
    df = safe_rename(df, {
        'PERSONFULLNAME': 'Employee Name',
        'Empl ID': 'Employee ID',
        'Manager': 'Supervisor Name'
    })
    conditions = [
        df["Shift Code"].str.startswith("N", na=False),
        df["Shift Code"].str.startswith("D", na=False)
    ]
    choices = ["Night Shift", "Day Shift"]
    df["Shift Type"] = np.select(conditions, choices, default="Other")
    return df


# ---------------------------
# Filtering Functions
# ---------------------------

def filter_exception_dataframe(df, exception_type="EARLY", session_key="filter_min_exception_amount"):
    df = df[df["EXCEPTIONTYPE"] == exception_type].copy()
    df["Amount Exceptions"] = pd.to_timedelta(df["Amount Exceptions"], errors="coerce")
    df = df[df["Amount Exceptions"].notna()]
    df["total_minutes"] = df["Amount Exceptions"].dt.total_seconds() / 60

    cutoff = st.session_state.get(session_key, 0)
    if cutoff:
        df = df[df["total_minutes"] > cutoff]

    df["Amount Exceptions"] = df["Amount Exceptions"].apply(format_timedelta_as_str)
    return df


def filter_missing_meal_dataframe(df):
    if df is not None and "Missed" in df.columns:
        return df[df["Missed"] > 0]
    return df


# ---------------------------
# Final Output Selection
# ---------------------------

def finalised_exception_dataframe(df):
    if "include" not in df.columns:
        return pd.DataFrame()
    df = df[df["include"] == True]
    cols = [
        "include", "Employee ID", "Employee Name", "Supervisor Name",
        "Job Title", "Job Level", "Actual", "Scheduled", "Amount Exceptions"
    ]
    return df[cols].copy()


def finalised_mm_dataframe(df):
    if "include" not in df.columns:
        return pd.DataFrame()
    df = df[df["include"] == True]
    cols = ["include", "Employee ID", "Employee Name", "Supervisor Name", "Shift Type"]
    return df[cols].copy()


# ---------------------------
# Join Helper
# ---------------------------

def join_roster_df(left, roster):
    return left.merge(
        roster[["Employee ID", "Supervisor Name", "Job Title", "Job Level"]],
        on="Employee ID",
        how="left"
    )
