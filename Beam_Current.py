import numpy as np
import matplotlib.pyplot as plt
import csv as csv


Fernandez_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/Fernandez_fig2.csv"

with open(Fernandez_data) as csvfile:
    lines = csvfile.readlines()[1:];
    Fernandez_Energy = [float(i.split(',', 1)[0]) for i in lines[0:]];
    Fernandez_Cross_Section = [float(i.split(',', 2)[1]) for i in lines[0:]];
    
cut_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/132MeV/Elastics/9.87kG/Beam_Elastic_Counts_cut.csv";

with open(cut_data) as csvfile:
    lines = csvfile.readlines()[1:];
    cut_gs_counts_132 = [round(float(i.split(',', 2)[1]), 0) for i in lines[0:]];
    cut_gs_error_132 = [round(float(i.split(',', 3)[2]), 0) for i in lines[0:]];
    cut_ex_counts_132 = [round(float(i.split(',', 4)[3]), 0) for i in lines[0:]];
    cut_ex_error_132 = [round(float(i.split(',', 5)[4]), 0) for i in lines[0:]];
    
PAlpha_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/132MeV/PAlpha/7.298kG/PAlpha_Counts.csv"

with open(PAlpha_data) as csvfile:
    lines = csvfile.readlines()[1:];
    ring_num = [float(i.split(',', 1)[0]) for i in lines[0:]];
    alpha_counts = [float(i.split(',', 2)[1]) for i in lines[0:]];
    error = [float(i.split(',', 3)[2]) for i in lines[0:]];


Beam_Energy = 132;
Nucleons = 20;
Beam_Energy_Per_Nucleon = Beam_Energy/Nucleons;

Energy = 0;
Cross_Section = 0;
min_diff = 1;

for i in range(len(Fernandez_Energy)):
	diff = abs(Beam_Energy_Per_Nucleon - Fernandez_Energy[i]);
	if diff < min_diff:
		min_diff = diff;
		Energy = Fernandez_Energy[i];
		Cross_Section = Fernandez_Cross_Section[i];

print('Energy: ', Energy);
print('Fernandez Cross Section: ', Cross_Section);

# Elastics Runs

d_omega1 = 2*np.pi*(1-np.cos(169.937*np.pi/180)) - 2*np.pi*(1 - np.cos(163.648*np.pi/180)); #rings 0 thru 4 

Proton_Counts = cut_gs_counts_132[0]+cut_gs_counts_132[1]+cut_gs_counts_132[2]+cut_gs_counts_132[3]+cut_gs_counts_132[4];

Beam_Current = (Proton_Counts/(Cross_Section*d_omega1))*10**(27);

print("Beam Intensity*Target Thickness*Time: ", Beam_Current);

# Beam Intensity check

elec_charge = 1.9*10**(-19);
charge_state = 10; 
target_thickness = 285*10**(-6); # g/cm^2
methylene_molar_mass = 14.0266; # g/mol
mol = 6.022*10**23; 

time = 4*60*60; # 4 runs, I'm just taking them to be an hour each for now, should check log book.

BC_check = (Beam_Current*(charge_state*elec_charge*10**(12)) / ((target_thickness / methylene_molar_mass)*mol*2))/time;

print('Beam Current (epA): ', BC_check)

# (p, alpha) runs

ring_cm_angles_deg = [23.821, 26.898, 30.013, 33.173, 36.386, 39.66, 43.008, 46.441, 49.976, 53.635, 57.443, 61.439, 65.676, 70.234, 75.25, 80.979, 88.055];
ring_cm_angles = [ring_cm_angles_deg[i]*(np.pi/180) for i in range(len(ring_cm_angles_deg))]
ring_solid_angles = [2*np.pi*(np.cos(ring_cm_angles[i-1]) - np.cos(ring_cm_angles[i])) for i in range(1, len(ring_cm_angles))]

PAlpha_diff_cs = [(alpha_counts[i]/(Beam_Current*ring_solid_angles[i]))*10**27 for i in range(len(alpha_counts))];

PAlpha_Rsum = [PAlpha_diff_cs[i]*np.sin((ring_cm_angles[i+1] + ring_cm_angles[i])/2)*(ring_cm_angles[i+1] - ring_cm_angles[i]) for i in range(len(PAlpha_diff_cs))];

PAlpha_cs = 2*np.pi*sum(PAlpha_Rsum);

print('(p, alpha) cross section (mb): ', PAlpha_cs)







