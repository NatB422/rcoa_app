
import streamlit as st


SESSION_STATE_DEFAULTS = {
    # User details
    "logged_in": False,
    "username": None,
    "displayname": None,
    # File to analyse
    "export_filename": "",
    "export_filedata": b"",
    "rcoa_session": None,
}

def main():

    for key, value in SESSION_STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # if not st.session_state.logged_in:
    #     pg = st.navigation([st.Page("login.py", title="Log in", icon=":material/login:")])
    #     pg.run()
    #     return

    st.set_page_config(
        layout="wide",
        page_title="RCoA Logbook Analyser",
        page_icon=":book:",

    )

    def logout():
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.rcoa_session = None
            st.session_state.password = None
            st.rerun()

    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

    nav_dict = {
        "Logbook File": [
            st.Page("file_pages/home.py", title="Home"),
            st.Page("file_pages/view.py", title="View"),
        ],
    }
    if st.session_state.logged_in:
        nav_dict[f"{st.session_state.displayname}'s Account"] = [logout_page]

    pg = st.navigation(nav_dict)
    pg.run()



if __name__ == "__main__":
    main()
