import os

class Standards:
    CH4_2pph="Two percent methane"
    CO2_600ppm_CH4_2179ppb="619? ppm Methane, 2.X ppm CH4"
    CO2_20pph="20% CO2, 80% Nitrogen"
    AMBIENT_AIR="WHO KNOWS, probs around 440ppm CO2, 1921 ppb?"
    


# data cleanup

# NOTE THIS WILL BREAK IF YOU HAVE OVER 10 SAMPLES IN A TREATMENT or 10 diff treatments
def generate_sample_id_from_sample_name(sample_name):
    if sample_name is None:
        return "DROP_ME"
    sample_info = sample_name.split('_')
    if sample_name.startswith('40ML_'):
        return f"40mL_{sample_info[0][-1]}.{sample_info[1][-1]}"
    if sample_name.startswith('40ML'):
       return f"40mL_{sample_name[4]}.{sample_name[-1]}"
    if sample_name.startswith('40_'):
        return f"40mL_{sample_info[1][0]}.{sample_info[1][-1]}"
   
    if sample_name.startswith(tuple(['BEN', '600'])):
        return "CO2_600ppm_CH4_2179ppb"
    
    if sample_name.startswith('2ML'):
         return f"2mL_{sample_info[1]}.{sample_info[2][0]}.{sample_info[2][1]}"
    if sample_name.startswith('1'):
        return f"2mL_{sample_info[0]}.{sample_info[1][0]}.{sample_info[1][-1]}"
    if sample_name.startswith('STD_AIR'):
        return "AMBIENT_AIR"
    
    if sample_name.startswith(tuple(['2%CH4', 'CH4_STD'])):
        return "CH4_2pph"
    
    if sample_name.startswith(tuple(['20%', 'EXHALE01'])):
        return "CO2_20pph"
    return "DROP_ME"




def print_samples(a, match):
    for x in a:
        b = generate_sample_id_from_sample_name(x)
        if b == match:
            print(b, ":", x)




def incubation_csvs_to_df(path_to_incubations=None):
    if path_to_incubations is None:
        path_to_incubations = "~/Desktop/lab_work/sessions/incubations"

    for file_name is os.listdir(path_to_incubations)
