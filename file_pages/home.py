
import streamlit as st

from file_pages.upload import upload_dialog
from file_pages.download import download_dialog
from file_pages.login import login_dialog


st.title("Welcome to the RCoA Logbook Analyser")
st.write(f"Current export file: {st.session_state.export_filename}")

filesize = len(st.session_state.export_filedata)
kb = round(filesize / 1_024, 1)
mb = round(filesize // 1_024_000, 1)
if kb < 1:
    st.write(f"File size: {filesize}B")
elif mb < 1:
    st.write(f"File size: {kb}KB")
else:
    st.write(f"File size: {mb}MB")


col1, col2, col3 = st.columns(3)
col1.button("Upload local file", on_click=upload_dialog)

if st.session_state.logged_in:
    col2.button("Fetch from RCoA", on_click=download_dialog)
else:
    col2.button("Fetch from RCoA", on_click=login_dialog)

if st.session_state.export_filedata:
    col3.download_button(
        "Download to local device",
        data=st.session_state.export_filedata,
        file_name=st.session_state.export_filename,
    )
