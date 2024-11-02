import io
import streamlit as st
import pandas as pd

from library.normalise_data import normalise_all_tables

@st.cache_data
def generate_dataframes(data) -> "dict[str, pd.DataFrame]":

    print("Generating case-specific dataframes")

    file_obj = io.BytesIO(data)
    df_dicts = pd.read_excel(file_obj, sheet_name=None)

    tab_contents = {}
    for sheetname, df in df_dicts.items():
        case_type = sheetname.replace("LOGBOOK_", "").replace("_", " ").title()
        tab_contents[case_type] = df

    return tab_contents


@st.cache_data
def get_normalised_data():

    print("Generating normalised dataframe")

    frames = generate_dataframes(st.session_state.export_filedata)
    return normalise_all_tables(frames)

def recalculate_normalisation():
    get_normalised_data.clear()
