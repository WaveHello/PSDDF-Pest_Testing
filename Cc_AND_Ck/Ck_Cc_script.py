# %%
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
from csv import writer as csv_writer
# %% Functions
def write_to_csv_startNend_line(file_path, starting_line, len_data, new_data):
    with open(file_path, 'r', newline='') as csvfile:
        lines = csvfile.readlines()
    
    # 
    # Rewrite the file content up to the starting_line (excluding the starting_line itself)
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.writelines(lines[:starting_line])

    with open(file_path, "a", newline="") as csvfile:
        writer = csv_writer(csvfile, delimiter= " ")
        writer.writerows(new_data)  # Write the data rows

    with open(file_path, "a", newline="") as csvfile:
        csvfile.writelines(lines[starting_line + len_data:])  # Write the data rows

def write_2_PSI(file_path, starting_line, len_data, new_rows, Cr_ratio):
    with open(file_path, 'r', newline='') as csvfile:
        lines = csvfile.readlines()
    
    # Update Cr/Cc ratio
    # Split the material prop line
    Cr_Ratio_line = lines[starting_line - 1].split()

    # Select Cr/Cc and set value
    Cr_Ratio_line[4] = str(Cr_ratio)

    #Rejoin the line
    lines[starting_line - 1] = " ".join(Cr_Ratio_line)+"\r\n"

    # Rewrite the file content up to the starting_line (excluding the starting_line itself)
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.writelines(lines[:starting_line])

    # Write in the new data (e, eff_stress, k)
    with open(file_path, "a", newline="") as csvfile:
        writer = csv_writer(csvfile, delimiter= " ")
        writer.writerows(new_rows)  # Write the data rows

    # Rewrite the previous data
    with open(file_path, "a", newline="") as csvfile:
        csvfile.writelines(lines[starting_line + len_data:])  # Write the data rows

def Collect_Material_Props(input_file_path, token):
    Material_prop = []
    current_material_dict = {}
    
    with open(input_file_path, "r") as file:
        line = file.readline().strip()
        while line:
            if line.startswith(token) and current_material_dict:
                # if line starts with token and the dictionary is not
                Material_prop.append(current_material_dict) # Add dictionary values to array
                current_material_dict = {} # Clear dictionary
            # if not retrive next...
            key = line[2:].strip() # Material property name
            value = float(file.readline().strip()) # Material property value
            current_material_dict[key] = value # Store Material property name and value
            line = file.readline().strip() # Read next file line
    Material_prop.append(current_material_dict) # append the last material
    return Material_prop

# %%
# Input and out directories
input_file_path = r"Cc_Ck_Input_Params.txt"

# Get path to output file
# addamse.tmp holds the name of the PSI file
addamse_file_path = r"addamse.tmp"

# Read addamse file
with open(addamse_file_path, 'r', newline = "") as file:
    lines = file.readlines()

# Create output file path from addamse text
output_file_path = lines[0].split()[-1] + ".psi"

### Retrieve input paramters
Material_Flag = '$$ MATERIAL' # Token used to determine when a material begins

# List of dictionaries containing each material property
Material_prop = Collect_Material_Props(input_file_path, Material_Flag)

# %%
### Store general material properties
gamma_w = Material_prop[0]["Gamma_w (kN/m^3)"]

### Calc e, eff_stress, and k for each material
for Material in Material_prop[1:]:
    # For each Material in Material_prop

    # Store Cc Inputs
    Pre_ConsolStress = Material["PRECONSOLIDATION_STRESS"]
    Cc = Material["Cc"] # Virgin compression slope
    Cr_ratio = Material["Cr/Cc"] # Ratio of C_r to C_c
    e0 = Material["e0"] # Initial void ratio
    ef = Material["ef"] # Final value of void ratio

    # Store Line number Inputs
    input_num_points = int(Material["INPUT_NUM_POINTS"]) # Number of spaces avalialable for inputs in PSDDF
    Void_Relation_Start_Line = int(Material["VOID_RELATION_START_LINE"]) - 100 # Convert PSI start line to python start
    
    # Create array of line numbers for PSI file
    Line_Numbers = np.arange(Void_Relation_Start_Line + 100, Void_Relation_Start_Line + 100 + input_num_points)

    # Store Cv Inputs
    Cv = Material["Cv (cm^2/s)"] * 1e-4 #[cm/s], consolidation coeff

    ## Calc Final eff_stress = f(ef)
    # e at preconsolidation pressure
    ep = e0 - Cc * Cr_ratio * np.log10(Pre_ConsolStress)

    # Effective stress at ef
    max_stress = Pre_ConsolStress * 10**((ep-ef)/Cc)

    if Pre_ConsolStress > 1:
        # Additional point to correct point lost when appending Cr and Cc arrays
        num_points = input_num_points + 1

        # Calc percentage of the loading that is reloading
        Perc_reloading = (Pre_ConsolStress-1)/max_stress

        # Number of reloading points
        num_Cr_points = int(num_points * Perc_reloading + 1)
        
        if num_Cr_points < 4:
        # Add additional points in num_Cr_points is too small
            num_Cr_points = 4
    else:
        num_points = input_num_points
        num_Cr_points = 0

    # Number of virgin compression points
    num_Cc_points = num_points - num_Cr_points

    # Virgin compression stresses
    Cc_eff_stress = np.linspace(Pre_ConsolStress, max_stress, num_Cc_points)

    # Recompression stresses
    Cr_eff_stress = np.linspace(1, Pre_ConsolStress,num_Cr_points)

    # Calc recompression void ratios
    e_recomp = -1 * Cr_ratio * Cc * np.log10(Cr_eff_stress) + e0

    # Calc virgin compression intercept
    if len(e_recomp) == 0:
        b = e0 + Cc * np.log10(Pre_ConsolStress)
    else:
        b = e_recomp[-1] + Cc * np.log10(Pre_ConsolStress)

    # Calc virgin compression void ratios
    e_virgin = -Cc * np.log10(Cc_eff_stress) + b

    if num_Cr_points > 0:
        # Append the compression lines
        eff_stress = np.append(Cr_eff_stress, Cc_eff_stress[1:])

        # Append the void ratio lines
        es = np.append(e_recomp, e_virgin[1:])
    else:
        # if Virgin compression is the full cycle then
        eff_stress = Cc_eff_stress
        es = e_virgin

    ## Calc m_v = delta Epsilon_v/(delta eff_stress)
    # Calc changes in void ratio
    delta_es = es[num_Cr_points:-1] - es[num_Cr_points+1:]

    # Calc volumetric strain
    epsilon_V = np.cumsum(delta_es)/(1+e0)

    # Calc delta volumetric strain
    delta_epsilon_V = epsilon_V[:-1] - epsilon_V[1:]

    # Calc delta stress
    delta_eff_stress = eff_stress[num_Cr_points:-1] - eff_stress[num_Cr_points+1:]

    # Calc m_v
    m_v = delta_epsilon_V/delta_eff_stress[1:] #[-/kN]

    # Calc permeability
    k = gamma_w * m_v * Cv * 100 #[cm/s]
    # plt.semilogx(k, es[num_Cr_points + 2:], label = "calc")
    # Fit permeability data
    k_fit_coeff = np.polyfit(es[num_Cr_points + 2:], np.log10(k), deg = 1)
    
    # Generate missing permeability values
    k_fit = 10**np.polyval(k_fit_coeff, es)

    #plot data
    # plt.semilogx(k_fit, es, label = "Mat: {:.0f}".format(Material["MATERIAL_ID"]))

    #least-Squares fit of data`
    coefficients = np.polyfit(np.log10(k), es[num_Cr_points + 2:], deg = 1)
    # print(coefficients[0])
    # Generate the best-fit line
    best_fit_line = np.polyval(coefficients, np.log10(k))

    # Print Best fit coefficients
    # print("## LS- Best fit coefficients ##")
    # print("Slope: {:.4f}\nIntercept: {:.4f}".format(coefficients[0], coefficients[1]))
    # plt.semilogx(eff_stress, es)
    # plt.show()

    Void_Relation_Data = zip(["{:}".format(value) for value in Line_Numbers],\
                             ["{:.3f}".format(value) for value in es],\
                            ["{:.2e}".format(value) for value in eff_stress],\
                            ["{:.2e}".format(value) for value in k_fit])
    write_2_PSI(output_file_path, Void_Relation_Start_Line, input_num_points, Void_Relation_Data, Cr_ratio)


# plt.legend()
# plt.show()

# %%
# %%
