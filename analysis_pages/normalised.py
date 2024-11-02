import streamlit as st

from utils.data_frame import get_normalised_data


st.subheader("Normalised Data")
st.dataframe(get_normalised_data())
