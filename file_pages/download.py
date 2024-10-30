import streamlit as st

from library.rcoa import download_logbook, refresh_logbook


@st.dialog("Download")
def download_dialog():

    if st.button("Download latest logbook export"):
        filename, filedata = download_logbook(st.session_state.rcoa_session)
        st.session_state.export_filedata = filedata
        st.session_state.export_filename = filename # f"logbook_export_{datetime.date.today():%Y-%m-%d}.xlsx2"
        st.rerun()

    if st.button("Refresh logbook export", disabled=True):
        # Not yet working it seems - 2024-10-30
        refresh_logbook(st.session_state.rcoa_session)
