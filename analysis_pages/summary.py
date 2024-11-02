import datetime
import streamlit as st

from utils.data_frame import get_normalised_data
from library.normalise_data import AGE_CATEGORIES, SUPERVISION_LEVELS_SHORTNAME

normal_df = get_normalised_data()

st.header("Summary Analyses of Cases in Logbook")

if st.button("Recalculate"):
    get_normalised_data.clear()
    st.rerun()

# Date selection
col1, col2 = st.columns(2)
start_date = col1.date_input(
    "Period Start",
    value=datetime.datetime(2023, 8, 1),
    format="YYYY-MM-DD",
)
end_date = col2.date_input(
    "Period End",
    value=datetime.datetime(2024, 7, 31),
    format="YYYY-MM-DD",
)
# st.write("Period:", start_date.isoformat(), " to ", end_date.isoformat())

start_datetime = datetime.datetime(start_date.year, start_date.month, start_date.day)
end_datetime = datetime.datetime(end_date.year, end_date.month, end_date.day)
normal_df = normal_df[normal_df["Date"] >= start_datetime][normal_df["Date"] <= end_datetime]

# Summary tables
grand_total = len(normal_df)
st.subheader(f"Total number of anaesthetics given in this period : {grand_total}")

# Supervision totals
supervision_df = normal_df.groupby("Supervision Level").size().to_frame('Quantity')
st.write("Supervision Level")
st.dataframe(supervision_df)


# Primary Specialty totals
primary_df = (normal_df
    .groupby("Primary Specialty")
    .agg(dict(
    **{
        "Case ID": "count"
    },
    **{
        supervision_level: "sum"
        for supervision_level in sorted(set(SUPERVISION_LEVELS_SHORTNAME.values()))
    },
    **{
        age_category: "sum"
        for age_category in AGE_CATEGORIES
    },
    ))
    .rename(columns={"Case ID": "Quantity"})
)
primary_df.insert(1, "%", round(100 * primary_df["Quantity"] / grand_total), 0)
st.write("Primary Specialty")
st.dataframe(primary_df)


# Secondary Specialty totals
primary_df = (normal_df
    .groupby("Secondary Specialty")
    .agg(dict(
    **{
        "Case ID": "count"
    },
    **{
        supervision_level: "sum"
        for supervision_level in sorted(set(SUPERVISION_LEVELS_SHORTNAME.values()))
    },
    **{
        age_category: "sum"
        for age_category in AGE_CATEGORIES
    },
    ))
    .rename(columns={"Case ID": "Quantity"})
)
primary_df.insert(1, "%", round(100 * primary_df["Quantity"] / grand_total), 0)
st.write("Secondary Specialty")
st.dataframe(primary_df)
