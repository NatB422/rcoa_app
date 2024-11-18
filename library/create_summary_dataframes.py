
import pandas as pd
from library.normalise_data import AGE_CATEGORIES, SUPERVISION_LEVELS_SHORTNAME, TIME_CATEGORIES

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

def prepare_data(normal_df:pd.DataFrame):

    dataframes = {} # type: dict[str, pd.DataFrame]

    grand_total = len(normal_df)


    # supervision_df
    dataframes["Supervision Level"] = normal_df.groupby("Supervision Level").size().to_frame('Quantity')

    # Primary
    dataframes["Primary Specialty"] = primary_specialty(normal_df, grand_total)

    # secondary
    dataframes["Secondary Specialty"] = secondary_specialty(normal_df, grand_total)

    # time
    dataframes["Time Period"] = time_of_day(normal_df)

    # priority
    dataframes["Priority"] = priority(normal_df)

    # working pattern
    dataframes["Working Pattern"] = working_pattern(normal_df)

    return dataframes

# Section builders
def primary_specialty(normal_df:pd.DataFrame, total_cases):
    primary_df = (normal_df
        .groupby("Primary Specialty")
        .agg(dict(
            **totals_counter,
            **sum_supervision_levels,
            **sum_ages,
        ))
        .rename(columns={"Case ID": "Quantity"})
    )
    primary_df.insert(1, "%", round(100 * primary_df["Quantity"] / total_cases), 0)
    return primary_df

def secondary_specialty(normal_df:pd.DataFrame, total_cases):
    secondary_df = (normal_df
        .groupby("Secondary Specialty")
        .agg(dict(
            **totals_counter,
            **sum_supervision_levels,
            **sum_ages,
        ))
        .rename(columns={"Case ID": "Quantity"})
    )
    secondary_df.insert(1, "%", round(100 * secondary_df["Quantity"] / total_cases), 0)
    return secondary_df

def time_of_day(normal_df):
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

        if time_df is None:
            time_df = tc_df
        else:
            time_df = pd.concat([time_df, tc_df])

    return time_df

def priority(normal_df:pd.DataFrame):
    priority_df = (normal_df
        .groupby("Priority", dropna=False)
        .agg(dict(
            **sum_supervision_levels,
            **totals_counter,
        ))
        .rename(columns={"Case ID": "Totals"})
    )
    return priority_df

def working_pattern(normal_df:pd.DataFrame):
    working_df = normal_df
    working_df["DayType"] = working_df["Date"].apply(lambda x: "Weekday" if x.dayofweek < 5 else "Weekend")
    working_df["Day"] = working_df.apply(lambda row: row["Morning (0800-1300)"] or row["Afternoon (1300-1800)"], axis=1)
    working_df["Evening"] = working_df["Evening (1800-2200)"]
    working_df["Night"] = working_df["Night (2200-0800)"]

    working_df = working_df.groupby("DayType").agg(dict(Day="sum", Evening="sum", Night="sum"))
    return working_df
