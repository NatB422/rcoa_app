import streamlit as st
import time


@st.dialog("Upload")
def upload_dialog():

    def run_upload():
        if not uploaded_file:
            return

        filedata = uploaded_file.read()

        st.session_state.export_filename = uploaded_file.name
        st.session_state.export_filedata = filedata

        st.success("File uploaded")
        time.sleep(1)
        st.rerun()


    uploaded_file = st.file_uploader(
        "Upload logbook export",
        accept_multiple_files=False,
    )

    if uploaded_file:
        run_upload()
