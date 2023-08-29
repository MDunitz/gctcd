import os
from .calculations import convert_CO2_area_to_ppm_TCD_CO2, convert_methane_area_to_ppm_FID

import numpy as np
import pandas as pd

from .constants import COMPOUNDS, STANDARDS, GCFID, GCTCD


def tidy_data(input_file):
    df = pd.read_csv(input_file)
    df['sample_id'] = df.apply(lambda row: generate_sample_id_from_sample_name(row['Sample_Name']), axis=1)
    df['peak_compound'] = df.apply(lambda row: label_peaks_by_retention_time(row), axis=1)
    df['is_std'] = df.apply(lambda row: label_is_std(row), axis=1)

    ## include peaks below limit of detection
    extra_peaks_df = handle_limit_of_detection(df)
    df =  pd.concat([df, extra_peaks_df], ignore_index=True)
    df['known_conc'] = df.apply(lambda row: set_standards_conc(row), axis=1)
    df['calculated_conc'] = df.apply(lambda row: set_theoretical_conc(row), axis=1)
    return df


def handle_limit_of_detection(df):
    sub_df = df[(df['sample_id']!="DROP_ME") & (df['is_std']==False)]
    groups = sub_df.groupby(['sample_id', 'Sample_Date', 'Instrument'])
    extra_peaks = []
    group_dict = dict(list(groups))
    for key, value in group_dict.items():
        if key[2] == GCTCD:
            compounds = value['peak_compound'].values
            if 'CO2' not in compounds:
                print('no CO2 here')
                extra_peaks.append({
                'Sample_Name': value['Sample_Name'].iloc[0],
                'Sample_Date':key[1],
                'Instrument': key[2],
                'Peak': int(-1),
                'Time': None,
                'Type': None, 
                'Area': -1,
                'Height': None,
                'Width': None,
                'Start': None,
                'End': None,
                "pdf_file_name": value['pdf_file_name'].iloc[0],
                "sample_id": value['sample_id'].iloc[0],
                "peak_compound": "CO2",
                "is_std": False
            })
        elif key[2] == GCFID:
            compounds = value['peak_compound'].values
            if 'CH4' not in compounds:
                extra_peaks.append({
                'Sample_Name': value['Sample_Name'].iloc[0],
                'Sample_Date':key[1],
                'Instrument': key[2],
                'Peak': int(-1),
                'Time': None,
                'Type': None, 
                'Area': -1,
                'Height': None,
                'Width': None,
                'Start': None,
                'End': None,
                "pdf_file_name": value['pdf_file_name'].iloc[0],
                "sample_id": value['sample_id'].iloc[0],
                "peak_compound": "CH4",
                "is_std": False
            })
        else:
            print(f"issue with the instrument in {key}, \n {value}")
    df = pd.DataFrame(extra_peaks)
    return df

# data cleanup

# NOTE THIS WILL BREAK IF YOU HAVE OVER 10 SAMPLES IN A TREATMENT or 10 diff treatments
# also set up a consistent naming scheme moving forward ffs
def generate_sample_id_from_sample_name(sample_name):
    try:
        #  40ML1003 
        if sample_name is None:
            return "DROP_ME"
        sample_info = sample_name.split('_')
        if sample_name.startswith('40ML_'):
            return f"40mL_{sample_info[0][-1]}.{sample_info[1][-1]}"
        if sample_name.startswith('40ML10'):
            return f"40mL_{sample_name[4]}.{sample_name[-1]}"
        if sample_name.startswith('40ML1'):
            return f"40mL_{sample_name[4]}.{sample_name[-2]}"
        if sample_name.startswith('40ML20'):
            return f"40mL_{sample_name[4]}.{sample_name[-1]}"
        if sample_name.startswith('40ML2'):
            return f"40mL_{sample_name[4]}.{sample_name[-2]}"
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


def set_theoretical_conc(row):
    if row['peak_compound'] is None:
        return None
    if row['Instrument'] == 'GCTCD':
            if row['peak_compound'] == COMPOUNDS["CO2"]["name"]:
                print(row['Area'])
                return convert_CO2_area_to_ppm_TCD_CO2(row['Area'])
    if row["Instrument"] == "GCFID":
        if row['peak_compound'] == COMPOUNDS["CH4"]["name"]:
            return convert_methane_area_to_ppm_FID(row['Area'])




def set_standards_conc(row):
    if row['peak_compound'] is None:
        return None
    if row['is_std'] == True:
        sample_id = row['sample_id']
        compound = row['peak_compound']
        return STANDARDS[sample_id]['makeup_in_ppm'][compound]

