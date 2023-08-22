import os
import pandas as pd
import numpy as np

from .constants import COMPOUNDS, STANDARDS



def tidy_data(input_file):
    df = pd.read_csv(input_file)
    df['sample_id'] = df.apply(lambda row: generate_sample_id_from_sample_name(row['Sample_Name']), axis=1)
    df['peak_compound'] = df.apply(lambda row: label_peaks_by_retention_time(row), axis=1)
    df['is_std'] = df.apply(lambda row: label_is_std(row), axis=1)
    print(df)
    return df

# data cleanup

# NOTE THIS WILL BREAK IF YOU HAVE OVER 10 SAMPLES IN A TREATMENT or 10 diff treatments
def generate_sample_id_from_sample_name(sample_name):
    try:
        if sample_name is None:
            return "DROP_ME"
        sample_info = sample_name.split('_')
        if sample_name.startswith('40ML_'):
            return f"40mL_{sample_info[0][-1]}.{sample_info[1][-1]}"
        if sample_name.startswith('40ML'):
            return f"40mL_{sample_name[4]}.{sample_name[-1]}"
        if sample_name.startswith('40_'):
            return f"40mL_{sample_info[1][0]}.{sample_info[1][-1]}"
        if sample_name.startswith(tuple(['BEN', '600', '2.979'])):
            return  STANDARDS['CO2_600ppm_CH4_2179ppb']['name']
        if sample_name.startswith('2ML'):
            return f"2mL_{sample_info[1]}.{sample_info[2][0]}.{sample_info[2][1]}"
        if sample_name.startswith('1'):
            return f"2mL_{sample_info[0]}.{sample_info[1][0]}.{sample_info[1][-1]}"
        if sample_name.startswith('STD_AIR'):
            return STANDARDS['AMBIENT_AIR']['name']
        if sample_name.startswith(tuple(['2%CH4', 'CH4_STD', '2307'])):
            return STANDARDS['CH4_2pph']['name']
        if sample_name.startswith(tuple(['20%', 'EXHALE01'])):
            return STANDARDS['CO2_20pph']['name']
    except Exception as e:
        print(f"ISSUE: {e}: {sample_name}")
    print(f"Setting {sample_name} to DROP_ME")
    return "DROP_ME"



def label_peaks_by_retention_time(row):
    peak_retention_time = row['Time']
    CO2_retention_time = COMPOUNDS['CO2']['retention_time']
    CH4_retention_time = COMPOUNDS['CH4']['retention_time']
    CO_retention_time = COMPOUNDS['CO']['retention_time']
    if row['Instrument'] == "GCTCD":
        if CO2_retention_time[0]< peak_retention_time < CO2_retention_time[1]:
            return "CO2"
    elif row['Instrument'] == "GCFID":
        if CH4_retention_time[0]< peak_retention_time < CH4_retention_time[1]:
            return "CH4"
        if CO_retention_time[0] < peak_retention_time < CO_retention_time[1]:
            return "CO"
    else:
        return None
    
    
def label_is_std(row):
    sample_name = row['sample_id']
    standards = [value['name'] for key, value in STANDARDS.items()]
    if sample_name in standards:
        return True
    else:
       return False


# def incubation_csvs_to_df(path_to_incubations=None):
#     if path_to_incubations is None:
#         path_to_incubations = "~/Desktop/lab_work/sessions/incubations"

#     for file_name is os.listdir(path_to_incubations)


def get_relevant_columns(df):
    df = df[(df['peak_compound'].notnull()) & (df['sample_id']!="DROP_ME")&(df['is_std']==False)]
    print(df)
