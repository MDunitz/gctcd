from datetime import datetime
import pandas as pd


def process_sample_data(data_df, incubation_df):
    df = pd.merge(data_df, incubation_df, on='sample_id', how='left')
    df['incubation_length'] = df.apply(lambda row: set_incubation_length(row), axis=1)
    df['salt_ratio'] = df.apply(lambda row: set_salt_to_biomass(row), axis=1)
    df['treatment'] = df.apply(lambda row: set_treatment_type(row), axis=1)
    df["percent_organic_matter"] = df.apply(lambda row: set_percent_organic_matter(row), axis=1)

    return df


def set_incubation_length(row):
    if (row['is_std'] == False) & (row['sample_id'] != "DROP_ME"):
        try:
            sample_date  = datetime.strptime(row['Sample_Date'], '%m/%d/%Y')
            incubation_start_date  = datetime.strptime(row['incubation_start_date'], '%m/%d/%y')
            return (sample_date - incubation_start_date).days

        except Exception as e:
            print(e)
            print(row)
            return None
    else:
        return None
    
def set_salt_to_biomass(row):
    if row['is_std']:
        return None
    if row['sample_id'] == 'DROP_ME':
        return None
    if row['ratio'] == "01:00":
        return "1:0"
    if row['ratio'] == "01:01":
        return "1:1"
    if row['ratio'] == "16:01":
        return "16:1"
    if row['ratio'] == "01:05":
        return "1:5"

def set_percent_organic_matter(row):
    if row['is_std']:
        return None
    if row['sample_id'] == 'DROP_ME':
        return None
    if row['ratio'] == "01:00":
        return "100%"
    if row['ratio'] == "01:01":
        return "50%"
    if row['ratio'] == "16:01":
        return "94%"
    if row['ratio'] == "01:05":
        return "16.7%"


def set_treatment_type(row):
    sample_id = row['sample_id']
    treatments = {"1": "Dry", "2": "Wet"}
    if sample_id.startswith('40mL'):
        return treatments[sample_id[5]]
    if sample_id.startswith('2mL'):
        return treatments[sample_id[4]]
    return None
