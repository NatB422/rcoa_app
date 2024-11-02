from pandas import DataFrame, concat, to_datetime
from library.transform_functions import age_in_years

SUPERVISION_LEVEL_LOOKUP = {
    "Immediate": "Directly supervised",
    "Local":     "Directly supervised",
    "2B":        "Indirectly supervised",
    "Distant":   "Indirectly supervised",
    "Teaching":  "Teaching Others",
    # Uncategorised
    "Supervised": "Uncategorised",
}

SUPERVISION_LEVELS_SHORTNAME = {
    "Directly supervised": "Direct",
    "Indirectly supervised": "Indirect",
    "Teaching Others": "Teaching",
    "Uncategorised": "Uncategorised",
}

supervision_levels = DataFrame({
    "Supervision": [k for k,v in SUPERVISION_LEVEL_LOOKUP.items()],
    "Supervision Level": [v for k,v in SUPERVISION_LEVEL_LOOKUP.items()]
})

AGE_CATEGORIES = {
    'Age <1':    lambda x: x < 1,
    'Age 1-5':   lambda x: 1 <= x < 6,
    'Age 6-15':  lambda x: 6 <= x < 16,
    'Age 16-80': lambda x:16 <= x < 81,
    'Age 80+':   lambda x:81 <= x,
}

TIME_CATEGORIES = {
    "Morning (0800-1300)": "morning-0800-1300",
    "Afternoon (1300-1800)": "afternoon-1300-1800",
    "Evening (1800-2200)": "evening-1800-2200",
    "Night (2200-0800)": "night-2200-0800",
}

NORMALISED_COLUMNS = [
    "Case ID",
    "Case Type",
    "Date",
    "Time",
    "Age",
    "Primary Specialty",
    "Secondary Specialty",
    "Priority",
    "Supervision",
]


def normalise_all_tables(case_dataframes:"dict[str, DataFrame]"):

    normalisers = {
        "Case Anaesthetic": normalise_case_anaesthetic,
        "Case Intensive": normalise_case_intensive,
        "Case Acute Pain": normalise_case_acute_pain,
        "Stand Alone Procedure": normalise_stand_alone,
        "Session": normalise_session,
    }

    normalised_data = [
        normalisers[case_type](df)
        for case_type, df in case_dataframes.items()
    ]

    frame = concat(df for df in normalised_data if df is not None)

    # Join with lookup data
    frame = frame.merge(supervision_levels, left_on="Supervision", right_on="Supervision")

    # Column conversions
    frame['Date'] = to_datetime(frame['Date'])
    frame['Age'] = frame['Age'].apply(age_in_years)

    frame["Priority"] = frame["Priority"].apply(lambda x: (x or "day case").capitalize())

    # New columns
    for age_category, age_filter in AGE_CATEGORIES.items():
        frame[age_category] = frame["Age"].apply(age_filter)

    for supervision_level in SUPERVISION_LEVEL_LOOKUP.values():
        shortname = SUPERVISION_LEVELS_SHORTNAME.get(supervision_level, "Uncategorised")
        frame[shortname] = frame["Supervision Level"].apply(lambda x: x == supervision_level)

    for time_category, time_value in TIME_CATEGORIES.items():
        frame[time_category.capitalize()] = frame["Time"].apply( lambda x: time_value in x if x else None)

    return frame

# -- Case specific normalisations
def normalise_case_anaesthetic(df:DataFrame):
    """['Case ID', 'Case Type', 'Date', 'Time', 'Deanery', 'School', 'Hospital',
       'Did this happen somewhere else', 'Personal Reference', 'Age', 'ASA',
       'Day Case', 'Priority', 'Primary Specialty',
       'Secondary Specialty (Optional)', 'Operation', 'Supervision',
       'Supervisor', 'Teaching', 'Mode of Anaesthesia', 'Intubation',
       'Regional Type', 'Regional Technique', 'Regional Catheter',
       'Regional Supervision', 'Regional Notes', 'Procedure Type',
       'Procedure Supervision', 'Procedure Supervisor', 'Procedure Notes',
       'Significant Event', 'Significant Event Type', 'Notes',]"""

    # Standard sanitisation
    if df is None:
        return None
    cases = df.loc[df["Case ID"].notnull()] # TODO - work out how to handle multiple rows

    # Add case type specific columns
    cases["Case Type"] = "Case Anaesthetic"

    # Rename columns
    cases = cases.rename(columns={'Secondary Specialty (Optional)': "Secondary Specialty"})

    return cases[NORMALISED_COLUMNS]

def normalise_case_intensive(df:DataFrame):
    """['ID', 'Case Type', 'Date', 'Time', 'Personal Reference', 'Age',
       'Deanery', 'School', 'Hospital', 'Did this happen somewhere else',
       'Event', 'Supervision', 'Supervisor', 'Notes', 'Supervision Level']"""

    # Standard sanitisation
    if df is None:
        return None
    cases = df.loc[df["ID"].notnull()] # TODO - work out how to handle multiple rows

    # Add case type specific columns
    cases["Case Type"] =  "Case Anaesthetic"
    cases["Primary Specialty"] = None
    cases["Secondary Specialty"] = None
    cases["Priority"] = None

    # Rename columns
    cases = cases.rename(columns={'ID': "Case ID"})

    return cases[NORMALISED_COLUMNS]

def normalise_case_acute_pain(df:DataFrame):
    """['ID', 'Date', 'Time', 'Deanery', 'School', 'Hospital',
       'Did this happen somewhere else', 'Ward', 'Personal Reference',
       'Patient', 'Age', 'Pain Type', 'Review Type', 'Review Nature',
       'Supervision', 'Supervisor', 'Role', 'Notes', ]"""

    # Standard sanitisation
    if df is None:
        return None
    cases = df.loc[df["ID"].notnull()] # TODO - work out how to handle multiple rows


    # Add case type specific columns
    cases["Case Type"] =  "Case Acute Pain"
    cases["Primary Specialty"] = None
    cases["Secondary Specialty"] = None
    cases["Priority"] = None

    # Rename columns
    cases = cases.rename(columns={'ID': "Case ID"})

    return cases[NORMALISED_COLUMNS]

def normalise_stand_alone(df:DataFrame):
    """['Case ID', 'Date', 'Reference', 'Specialty',
       'Procedure Type (Anaesthesia)', 'Procedure Type (Medicine)',
       'Procedure Type (Pain)', 'Supervision', 'Supervisor', 'Notes',]"""

    # Standard sanitisation
    if df is None:
        return None
    cases = df.loc[df["Case ID"].notnull()] # TODO - work out how to handle multiple rows

    # Add case type specific columns
    cases["Case Type"] =  "Stand Alone"
    cases["Time"] = None
    cases["Age"] = None
    cases["Secondary Specialty"] = None
    cases["Priority"] = None

    # Rename columns
    cases = cases.rename(columns={'Specialty': "Primary Specialty"})

    return cases[NORMALISED_COLUMNS]

def normalise_session(df:DataFrame):
    """['Case ID', 'Date', 'Time', 'Deanery', 'School', 'Hospital',
       'Did this happen somewhere else', 'Activity',
       'Specialty (only if Activity=Theatre)', 'Supervision', 'Supervisor',
       'Notes', ],"""

    # Standard sanitisation
    if df is None:
        return None
    cases = df.loc[df["Case ID"].notnull()] # TODO - work out how to handle multiple rows

    # Add case type specific columns
    cases["Case Type"] =  "Session"
    cases["Age"] = None
    cases["Secondary Specialty"] = None
    cases["Priority"] = None

    # Rename columns
    cases = cases.rename(columns={'Specialty (only if Activity=Theatre)': "Primary Specialty"})

    return cases[NORMALISED_COLUMNS]
