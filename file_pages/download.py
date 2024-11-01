import datetime
import time
import streamlit as st

from library.rcoa import download_logbook, refresh_logbook


@st.dialog("Download")
def download_dialog():

    st.write(f"Fetch logbook from RCoA for {st.session_state.displayname}")

    if st.button("Download latest logbook export"):
        download_placeholder = st.empty()
        download_placeholder.success(f"Download started at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")

        filename, filedata = download_logbook(st.session_state.rcoa_session)
        st.session_state.export_filedata = filedata
        st.session_state.export_filename = filename
        download_placeholder.success("Download completed")

        time.sleep(1)
        st.rerun()

    if st.button("Refresh logbook export", disabled=False):
        # Not yet working it seems - 2024-10-30
        refresh_placeholder = st.empty()
        refresh_placeholder.success(f"Refresh requested at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")

        error_message = refresh_logbook(st.session_state.rcoa_session)
        if error_message:
            refresh_placeholder.warning("Something went wrong requesting a refresh")
        else:
            refresh_placeholder.success(
                f"RCoA refresh successfully started at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}.\n"
                "Download should be available after about 1-2 minutes."
            )

        time.sleep(3)
        refresh_placeholder.empty()
