import streamlit as st

from library.rcoa import get_account_details

@st.cache_data
def account_details():
    return get_account_details(st.session_state.rcoa_session)

st.header(f"RCoA Account details of {st.session_state.displayname}")
st.markdown(account_details(), unsafe_allow_html=True)
