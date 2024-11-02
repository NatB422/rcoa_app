import datetime
import streamlit as st
import pandas as pd

from utils.data_frame import get_normalised_data
from library.normalise_data import AGE_CATEGORIES, SUPERVISION_LEVELS_SHORTNAME, TIME_CATEGORIES

normal_df = get_normalised_data()

st.header("Summary Analyses of Cases in Logbook")

if False and st.button("Recalculate"):
    get_normalised_data.clear()
    st.rerun()

# Date selection
with st.expander("Date selection"):
    col0, col1, col2 = st.columns(3)
    filtered = col0.checkbox("Apply date filter")
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

    if filtered:
        start_datetime = datetime.datetime(start_date.year, start_date.month, start_date.day)
        end_datetime = datetime.datetime(end_date.year, end_date.month, end_date.day)
        normal_df = normal_df[normal_df["Date"] >= start_datetime][normal_df["Date"] <= end_datetime]

# Summary tables
grand_total = len(normal_df)
st.subheader(f"Total number of anaesthetics given in this period : {grand_total}")

# Supervision totals
with st.expander("Supervision level"):
    supervision_df = normal_df.groupby("Supervision Level").size().to_frame('Quantity')
    st.dataframe(supervision_df)

# COMMON AGGREGATE COLUMNS
totals_counter = {"Case ID": "count"}
sum_supervision_levels = {
    supervision_level: "sum"
    for supervision_level in sorted(set(SUPERVISION_LEVELS_SHORTNAME.values()))
}
sum_ages = {
    age_category: "sum"
    for age_category in AGE_CATEGORIES
}

# Primary Specialty totals
with st.expander("Primary Specialty"):
    primary_df = (normal_df
        .groupby("Primary Specialty")
        .agg(dict(
            **totals_counter,
            **sum_supervision_levels,
            **sum_ages,
        ))
        .rename(columns={"Case ID": "Quantity"})
    )
    primary_df.insert(1, "%", round(100 * primary_df["Quantity"] / grand_total), 0)
    st.dataframe(primary_df)


# Secondary Specialty totals
with st.expander("Secondary Specialty"):
    secondary_df = (normal_df
        .groupby("Secondary Specialty")
        .agg(dict(
            **totals_counter,
            **sum_supervision_levels,
            **sum_ages,
        ))
        .rename(columns={"Case ID": "Quantity"})
    )
    secondary_df.insert(1, "%", round(100 * primary_df["Quantity"] / grand_total), 0)
    st.dataframe(secondary_df)

# Time of day totals
with st.expander("Time of Day and level of supervision"):
    time_df = None
    source_df = normal_df
    for time_category in TIME_CATEGORIES:
        source_df["Time Period"] = time_category.capitalize()
        tc_df = (source_df
            .where(source_df[time_category.capitalize()])
            .groupby("Time Period")
            .agg(dict(
                **sum_supervision_levels,
                **totals_counter,
            ))
            .rename(columns={"Case ID": "Totals"})
        )
        print(tc_df)

        if time_df is None:
            time_df = tc_df
        else:
            time_df = pd.concat([time_df, tc_df])

    st.dataframe(time_df)

# Priority totals
with st.expander("Priority and level of supervision"):
    priority_df = (normal_df
        .groupby("Priority", dropna=False)
        .agg(dict(
            **sum_supervision_levels,
            **totals_counter,
        ))
        .rename(columns={"Case ID": "Totals"})
    )
    st.dataframe(priority_df)

# Working pattern
with st.expander("Working pattern"):
    working_df = normal_df
    working_df["DayType"] = working_df["Date"].apply(lambda x: "Weekday" if x.dayofweek < 5 else "Weekend")
    working_df["Day"] = working_df.apply(lambda row: row["Morning (0800-1300)"] or row["Afternoon (1300-1800)"], axis=1)
    working_df["Evening"] = working_df["Evening (1800-2200)"]
    working_df["Night"] = working_df["Night (2200-0800)"]

    st.dataframe(working_df.groupby("DayType").agg(dict(Day="sum", Evening="sum", Night="sum")))
