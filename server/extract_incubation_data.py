import os
import pandas as pd


def extract_incubation_data(path_to_incubations):
    dfs = []
    for file_name in os.listdir(path_to_incubations):
        path_to_file = os.path.join(path_to_incubations, file_name)
        dfs.append(pd.read_csv(path_to_file))

    return pd.concat(dfs, ignore_index=True)

    
def tidy_incubation_data(df):
    df['sample_name'] = df['sample_id']
    df['sample_id'] = df.apply(lambda row: set_sample_id(row), axis=1)
    df = df.drop(['sample_name'], axis=1)
    return df
    


def set_sample_id(row):
    sample_name = row['sample_name']
    if sample_name.startswith('40ml'):
        return f"40mL_{sample_name[-3:]}"
    else:
        return f"2mL_{sample_name}"
        

def load_and_process_incubation_data(path_to_incubations):
    incubation_df = extract_incubation_data(path_to_incubations)
    incubation_df = tidy_incubation_data(incubation_df)
    return incubation_df