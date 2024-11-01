import io
import streamlit as st
import pandas

@st.cache_data
def generate_dataframes(data):
    file_obj = io.BytesIO(data)
    df_dicts = pandas.read_excel(file_obj, sheet_name=None)

    tab_contents = {}
    for sheetname, df in df_dicts.items():
        case_type = sheetname.replace("LOGBOOK_", "").replace("_", " ").title()
        tab_contents[case_type] = df

    return tab_contents

def show_excel_file_contents():

    tab_contents = generate_dataframes(st.session_state.export_filedata)
    for index, tab_obj in enumerate(st.tabs(tab_contents)):
        tab_name = list(tab_contents)[index]
        tab_obj.dataframe(tab_contents[tab_name])



st.write(f"Current export file: {st.session_state.export_filename}")

filesize = len(st.session_state.export_filedata)
if filesize < 1_024:
    # Probably not an Excel file...
    st.write("Error processing file - contents shown below")
    st.write(st.session_state.export_filedata)
else:
    show_excel_file_contents()
