import streamlit as st
import time

from library.file_properties import get_excel_file_creation_time
from utils.data_frame import get_normalised_data


@st.dialog("Upload")
def upload_dialog():

    def run_upload():
        if not uploaded_file:
            return

        filedata = uploaded_file.read()

        st.session_state.export_filename = uploaded_file.name
        st.session_state.export_filedata = filedata

        try:
            created_time = get_excel_file_creation_time(filedata)
            st.session_state.file_created = created_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            st.session_state.file_created = ""

        st.success("File uploaded")
        time.sleep(1)

        get_normalised_data.clear()
        st.rerun()


    uploaded_file = st.file_uploader(
        "Upload logbook export",
        accept_multiple_files=False,
    )

    if uploaded_file:
        run_upload()
