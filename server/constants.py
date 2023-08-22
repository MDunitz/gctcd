
COMPOUNDS = {
"CO2": {"name": "CO2", "molecular_weight": 44.01, "density": 1.87, "retention_time": [4.6, 4.75]},
"CH4": {"name": "CH4", "molecular_weight": 16.04, "density": 0.657, "retention_time": [2.56, 2.57]},
"CO":  {"name": "CO", "molecular_weight": 28.01, "density": 1.14, "retention_time": [2.38, 2.39]}
}
STANDARDS = {
 "CH4_2pph" : {"name": "CH4_2pph", "description":"2% Methane" },
 "CO2_600ppm_CH4_2179ppb" : {"name": "CO2_600ppm_CH4_2179ppb", "description":"2.179 ppm Methane, 60? ppm CO2" },
 "CO2_20pph" : {"name": "CO2_20pph", "description":"20% CO2, 80% Nitrogen" },
 "AMBIENT_AIR" : {"name": "AMBIENT_AIR", "description":"WHO KNOWS, probs around 440ppm CO2, 1921 ppb?" }
}

V_m = 24.0  #  Assuming at room temp (298K) and 1 atm => molar volue of gas is 24.0 dm^3
    # https://chemistrymadesimple.net/episode/16/#:~:text=Room%20Temperature%20and%20Pressure%20(RTP,24.0%20dm%C2%B3%20(%2024.0%20L)
