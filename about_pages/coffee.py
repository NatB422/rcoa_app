import streamlit as st
from streamlit.components.v1 import iframe

KOFI_URL = "https://ko-fi.com/"
KOFI_ACCOUNT = "natb422"

col1, col2 = st.columns(2)

# Information
col1.header("Nah, I prefer tea...")
col1.subheader("or a Ko-fi!")
col1.write("")
col1.write("If you are finding this site useful, then great! I've made this app purely to make your life easier.")
col1.write("This is a hobby project, so it's only done in my spare time, and I'm not looking to earn anything from this.")

# Donation iframe
if KOFI_ACCOUNT:
    col1.write("")
    col1.write("If you want to contribute to me having more energy to work on this site, why not buy me a cuppa!")

    with col2:
        iframe(
            src=f'{KOFI_URL}/{KOFI_ACCOUNT}/?hidefeed=true&widget=true&embed=true&preview=true',
            height=640,
            scrolling=True
        )
