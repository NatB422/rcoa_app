
import streamlit as st

from library.rcoa import create_rcoa_session


def perform_login():

    session = create_rcoa_session(
        st.session_state.username,
        st.session_state.password,
    )

    st.session_state.rcoa_session = session
    st.session_state.displayname = session.cookies.get("name").replace("_", " ")


@st.dialog("Login")
def login_dialog():
    # Concept: store credentials somwhere to be loaded as secrets and pre-loaded here?
    # default_username = st.session_state.username or st.secrets["rcoa"].username
    # default_password = st.secrets["rcoa"].password if st.session_state.username == st.secrets["rcoa"].username else ""

    default_username = st.session_state.username
    default_password = ""

    username = st.text_input("Username", value=default_username)
    password = st.text_input("Password", value=default_password)

    if st.button("Log in"):
        if not username:
            st.toast("Please specify a username")
            return

        st.session_state.username = username
        st.session_state.password = password

        perform_login()
        st.session_state.logged_in = True

        st.rerun()
