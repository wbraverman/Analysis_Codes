import numpy as np
import matplotlib.pyplot as plt
import csv as csv


Fernandez_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/Fernandez_fig2.csv"

with open(Fernandez_data) as csvfile:
    lines = csvfile.readlines()[1:];
    Fernandez_Energy = [float(i.split(',', 1)[0]) for i in lines[0:]];
    Fernandez_Cross_Section = [float(i.split(',', 2)[1]) for i in lines[0:]];
    
cut_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/128MeV/Elastics/7.65kG/Beam_Elastic_Counts_raw.csv";

with open(cut_data) as csvfile:
    lines = csvfile.readlines()[1:];
    cut_gs_counts_132 = [round(float(i.split(',', 2)[1]), 0) for i in lines[0:]];
    cut_gs_error_132 = [round(float(i.split(',', 3)[2]), 0) for i in lines[0:]];
    cut_ex_counts_132 = [round(float(i.split(',', 4)[3]), 0) for i in lines[0:]];
    cut_ex_error_132 = [round(float(i.split(',', 5)[4]), 0) for i in lines[0:]];
    
PAlpha_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/128MeV/PAlpha/7.21kG/PAlpha_Counts.csv"

with open(PAlpha_data) as csvfile:
    lines = csvfile.readlines()[1:];
    ring_num = [float(i.split(',', 1)[0]) for i in lines[0:]];
    alpha_counts = [float(i.split(',', 2)[1]) for i in lines[0:]];
    error = [float(i.split(',', 3)[2]) for i in lines[0:]];


Beam_Energy = 128;
Nucleons = 20;
EnergyLoss = 0.09; # MeV/u of energy lost through target
Beam_Energy_Per_Nucleon = Beam_Energy/Nucleons;
Efficiency = 0.2039


Energy = [((Beam_Energy_Per_Nucleon - EnergyLoss) + i*(EnergyLoss/1000)) for i in range(0, 1001)]


Cross_Section = [];
EnergyList = [];


for i in range(len(Fernandez_Energy)):
	if Fernandez_Energy[i] <= Beam_Energy_Per_Nucleon and Fernandez_Energy[i] >= (Beam_Energy_Per_Nucleon - EnergyLoss):
		EnergyList.append(Fernandez_Energy[i])
		Cross_Section.append(Fernandez_Cross_Section[i])

CorrectedEnergyList = []
CorrectedCrossSection = []


for i in range(0, len(EnergyList)-1):
	if EnergyList[i] != EnergyList[i+1]:
		CorrectedEnergyList.append(EnergyList[i])
		CorrectedCrossSection.append(Cross_Section[i])

if EnergyList[len(EnergyList)-1] != EnergyList[len(EnergyList)-2]:
	CorrectedEnergyList.append(EnergyList[len(EnergyList)-1])
	CorrectedCrossSection.append(Cross_Section[len(EnergyList)-1])
	
print('Fernandez Energy: ', CorrectedEnergyList);
print('Fernandez Differential Cross Section (mb): ', CorrectedCrossSection);

# Elastic Scattering Calculations

Fernandez_gs_ring_counts = [cut_gs_counts_132[i] for i in range(2, 6)]; # called cut but linked to raw data file. Too lazy to change names.

runtime = 1200;  

charge_state = 10; # Assuming Ne is fully stripped
elec_charge = 1.6*10**(-19); # coulomb

target_thickness = 270*10**(-6); # g/cm^2
methylene_molar_mass = 14.0266; #g/mol
PolypropeleneMolMass = methylene_molar_mass*3;
hydrogen_nuclei = (target_thickness/methylene_molar_mass)*(6.0221408*10**(23))*2; 

CMAnglesElastics = [167.42, 166.162, 164.904, 163.646, 162.388]
#LabAngles = [6.25, 6.875, 7.5, 8.125, 8.75] # Lab angles for rings 2 thru 5 (counting from 0)

d_omega = 2*np.pi*(1-np.cos(CMAnglesElastics[0]*np.pi/180)) - 2*np.pi*(1 - np.cos(CMAnglesElastics[-1]*np.pi/180)); #rings 2 to 5

BeamCurrent = [(sum(Fernandez_gs_ring_counts)/((CorrectedCrossSection[i]*10**(-27))*runtime*hydrogen_nuclei*d_omega))*(charge_state*elec_charge*10**12) for i in range(len(CorrectedCrossSection))]
AvgBeamCurrent = (sum(BeamCurrent)/len(BeamCurrent))

CurrentTimeTarget = [(sum(Fernandez_gs_ring_counts)/((CorrectedCrossSection[i]*10**(-27))*d_omega)) for i in range(len(CorrectedCrossSection))]
CurrentTimeTargetAvg = (sum(CurrentTimeTarget)/len(CurrentTimeTarget))

print('H atoms per cm^2: ', hydrogen_nuclei)
print('Solid Angle Coverage Rings 2 to 5: ', d_omega)
print('Beam Current: ', "%.2f" % AvgBeamCurrent, 'epA')
print('Number of Hydrogen: ', hydrogen_nuclei)
print('Elastics Solid Angle: ', '%.2f' % d_omega, ' str')
print('I*Nt*t = ', CurrentTimeTargetAvg)

# Alpha Calculations

CMAnglesAlphas = [149.202, 145.944, 142.628, 139.241, 135.771]; # Start of ring 2 to end of ring 5

DOmegaAlpha = [2*np.pi*(1-np.cos(CMAnglesAlphas[i]*np.pi/180)) - 2*np.pi*(1 - np.cos(CMAnglesAlphas[i+1]*np.pi/180)) for i in range(len(CMAnglesAlphas)-1)]; #rings 2 to 5

PAlphaDiffCS = [alpha_counts[i]/(CurrentTimeTargetAvg*DOmegaAlpha[i])*10**(27) for i in range(len(alpha_counts))]

PAlphaRSum = [PAlphaDiffCS[i]*np.sin((CMAnglesAlphas[i+1]+CMAnglesAlphas[i])/2)*(CMAnglesAlphas[i+1]-CMAnglesAlphas[i]) for i in range(len(PAlphaDiffCS))]

PAlphaTotalCS = (2*np.pi*sum(PAlphaRSum))/Efficiency;

print('(p, alpha) cross section at ', Beam_Energy, ' MeV: ', '%.2f' % PAlphaTotalCS, ' mb')










