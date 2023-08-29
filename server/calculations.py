from .constants import COMPOUNDS, V_m

# V_m = 24.0  #  Assuming at room temp (298K) and 1 atm => molar volue of gas is 24.0 dm^3
#     # https://chemistrymadesimple.net/episode/16/#:~:text=Room%20Temperature%20and%20Pressure%20(RTP,24.0%20dm%C2%B3%20(%2024.0%20L)


def convert_ppb_to_mols(amount, substrate):
    pass

def convert_ppm_to_mols(amount, substrate):
    pass

def convert_methane_area_to_ppm_JAMES_FID(amount):
    ppm = 0.0324 * amount + 172.51 
    return ppm

def convert_methane_area_to_ppm_FID(amount):
    if amount == -1:
        return 1 # TODO FIND ACTUAL SOURCE FOR GCFID DETECTION LIMIT
    ppm =  0.141*amount + -7.31
    return ppm
 

def convert_CO2_area_to_ppm_TCD_CO2(amount):
    if amount==-1:
        return 10 # This is the limit of detection for the GCTCD # TODO FIND SOURCE
    ppm = 1.75* amount + -25.5
    return ppm

def convert_area_to_mols(amount, substrate):
    pass

def convert_gas_to_organic_matter(amount, substrate):
    pass

def microliters_to_mols_by_density(amount_in_microliters, substrate):
    amount_in_liters =  amount_in_microliters * 1/(1e6)
    amount_cubic_meters = amount_in_liters * 1000
    amount_in_kg = amount_cubic_meters * COMPOUNDS[substrate]["density"]
    amount_in_grams = amount_in_kg * 1000
    amount_in_mols = amount_in_grams / COMPOUNDS[substrate]["molecular_weight"]
    return amount_in_mols


def microliters_to_mols_by_ideal_gas_law(amount_in_microliters):
    mols_of_substrate = amount_in_microliters / V_m
    return mols_of_substrate

