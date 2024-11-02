import streamlit as st

from utils.data_frame import generate_dataframes


st.write(f"Current export file: {st.session_state.export_filename}")

filesize = len(st.session_state.export_filedata)
if filesize < 1_024:
    # Probably not an Excel file...
    st.write("Error processing file - contents shown below")
    st.write(st.session_state.export_filedata)
else:
    tab_contents = generate_dataframes(st.session_state.export_filedata)
    for index, tab_obj in enumerate(st.tabs(tab_contents)):
        tab_name = list(tab_contents)[index]
        tab_obj.dataframe(tab_contents[tab_name])
