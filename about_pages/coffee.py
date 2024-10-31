import streamlit as st

KOFI_URL = "https://ko-fi.com/"
KOFI_IMAGE = "https://storage.ko-fi.com/cdn/kofi2.png?v=3"

st.header("Nah, I prefer tea...")
st.subheader("or a Ko-fi!")

st.write("")
st.write("If you are finding this site useful, then great! I've made this app purely to make your life easier.")
st.write("This is a hobby project, so it's only done in my spare time, and I'm not looking to earn anything from this.")
st.write("If you want to contribute to me having more time to work on this site, why not use my ko-fi link to send me a tip:")

st.subheader("Not currently setup")

st.markdown(
    f"""
    <a href='{KOFI_URL}' target='_blank'><img height='36' style='border:0px;height:36px;'
    src='{KOFI_IMAGE}' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
    """,
    unsafe_allow_html=True,
)
