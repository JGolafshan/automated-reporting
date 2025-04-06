#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Date: 06/04/2024
    Author: Joshua David Golafshan
"""

import pandas as pd
import streamlit as st


def read_file(file, skip_rows=0):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file, skiprows=skip_rows)
        elif file.name.endswith((".xls", ".xlsx")):
            return pd.read_excel(file, skiprows=skip_rows)
        else:
            st.warning("Unsupported file format. Please upload CSV or Excel.")
            return None
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None


def handle_file_upload(dataframe, filename, session_key: str, label: str):
    """
    Handles file upload with session caching and feedback display.

    Parameters:
    - dataframe: DataFrame loaded from the uploaded file
    - filename: the uploaded file object
    - session_key: base key for session_state (e.g., 'df_exception')
    - label: display name (e.g., "Exception File")

    Returns:
    - DataFrame or None
    """

    name_key = f"{session_key}_filename"
    file_key = f"{session_key}_file"

    if dataframe is not None and filename is not None:
        # Save file and dataframe to session
        st.session_state[session_key] = dataframe
        st.session_state[file_key] = filename
        st.session_state[name_key] = filename.name
        st.success(f"✅ Loaded: {filename.name}")
        return dataframe

    elif session_key in st.session_state:
        # Recover previously stored data
        st.success(f"✅ Previously loaded: {st.session_state.get(name_key, label)}")
        return st.session_state[session_key]

    return None

def set_page_state(page: str):
    """Set the current page in session state and navigate if needed."""
    if st.session_state.get("current_page") != page:
        st.session_state.current_page = page


def load_css(file_path: str) -> str:
    """
    Load and apply a custom CSS file to the Streamlit app.

    This function abstracts the CSS from the Streamlit app by reading
    a CSS file and injecting it into the app using `st.markdown()`.

    :param file_path: Path to the CSS file.
    :raises FileNotFoundError: If the specified file does not exist.
    :raises Exception: If the file cannot be read.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            css = f.read()
        return f"<style>{css}</style>"
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_path}")
    except Exception as e:
        st.error(f"Error loading CSS file: {e}")
