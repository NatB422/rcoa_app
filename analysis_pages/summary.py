import datetime
import streamlit as st

from utils.data_frame import get_normalised_data
from library.create_summary_dataframes import prepare_data
from library.pdf_utils import export_to_pdf


normal_df = get_normalised_data()

st.header("Summary Analyses of Cases in Logbook")

if False and st.button("Recalculate"):
    get_normalised_data.clear()
    st.rerun()


# Date selection
with st.expander("Date selection") as exp:
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

    if filtered:
        start_datetime = datetime.datetime(start_date.year, start_date.month, start_date.day)
        end_datetime = datetime.datetime(end_date.year, end_date.month, end_date.day)
        normal_df = normal_df[normal_df["Date"] >= start_datetime][normal_df["Date"] <= end_datetime]

# Calculate data based on the date filter
ALL_DATA_FRAMES = prepare_data(normal_df)

# Display summary
if filtered:
    time_period_text = f"{start_date.isoformat()} to {end_date.isoformat()}"
else:
    time_period_text =  "All records"

grand_total = len(normal_df)
summary_line = f"Total number of anaesthetics given in this period : {grand_total}"

col1, col2, col3 = st.columns((0.5,0.25,0.25))
col1.subheader(f"Period: {time_period_text}")

# Add PDF Export
if col2.button("Export as PDF"):
    st.session_state["summary_pdf_data"] = b""
    pdf_data = export_to_pdf(f"Period: {time_period_text}<br/>{summary_line}", ALL_DATA_FRAMES)
    st.session_state["summary_pdf_data"] = pdf_data

if st.session_state["summary_pdf_data"]:
    filename = f"logbook_{time_period_text.lower().replace(' ', '_')}.pdf"
    col3.download_button("Download", st.session_state["summary_pdf_data"], filename)


# Summary tables
st.subheader(summary_line)

# Supervision totals
with st.expander("Supervision level"):
    supervision_df = ALL_DATA_FRAMES["Supervision Level"]
    st.dataframe(supervision_df)

# Primary Specialty totals
with st.expander("Primary Specialty"):
    primary_df = ALL_DATA_FRAMES["Primary Specialty"]
    st.dataframe(primary_df)

# Secondary Specialty totals
with st.expander("Secondary Specialty"):
    secondary_df = ALL_DATA_FRAMES["Secondary Specialty"]
    st.dataframe(secondary_df)

# Time of day totals
with st.expander("Time of Day and level of supervision"):
    time_df = ALL_DATA_FRAMES["Time Period"]
    st.dataframe(time_df)

# Priority totals
with st.expander("Priority and level of supervision"):
    priority_df = ALL_DATA_FRAMES["Priority"]
    st.dataframe(priority_df)

# Working pattern
with st.expander("Working pattern"):
    working_df = ALL_DATA_FRAMES["Working Pattern"]
    st.dataframe(working_df)
