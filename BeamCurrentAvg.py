import numpy as np
import matplotlib.pyplot as plt
import csv as csv 

cut_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/134MeV/Elastics/7.95kG/Beam_Elastic_Counts_raw.csv";

with open(cut_data) as csvfile:
    lines = csvfile.readlines()[1:];
    cut_gs_counts_132 = [round(float(i.split(',', 2)[1]), 0) for i in lines[0:]];
    cut_gs_error_132 = [round(float(i.split(',', 3)[2]), 0) for i in lines[0:]];
    cut_ex_counts_132 = [round(float(i.split(',', 4)[3]), 0) for i in lines[0:]];
    cut_ex_error_132 = [round(float(i.split(',', 5)[4]), 0) for i in lines[0:]];
    
    
Fernandez_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/Fernandez_fig2.csv"

with open(Fernandez_data) as csvfile:
    lines = csvfile.readlines()[1:];
    Fernandez_Energy = [float(i.split(',', 1)[0]) for i in lines[0:]];
    Fernandez_Cross_Section = [float(i.split(',', 2)[1]) for i in lines[0:]];
    
    
Beam_Energy = 134;
EnergyLoss = 0.09; # MeV/u of energy lost through target
Nucleons = 20;
Beam_Energy_Per_Nucleon = Beam_Energy/Nucleons;

Energy = [((Beam_Energy_Per_Nucleon - EnergyLoss) + i*(EnergyLoss/100)) for i in range(0, 101)]


Cross_Section = [];
EnergyList = [];

for j in range(len(Energy)):
	min_diff = 1
	for i in range(len(Fernandez_Energy)):
		if Fernandez_Energy[i] <= Beam_Energy_Per_Nucleon and Fernandez_Energy[i] >= (Beam_Energy_Per_Nucleon - EnergyLoss):
			diff = abs(Energy[j] - Fernandez_Energy[i]);
			if diff < min_diff:
				min_diff = diff;
				EnergyBuffer = Fernandez_Energy[i]
				CrossSectionBuffer = Fernandez_Cross_Section[i]
	EnergyList.append(EnergyBuffer);
	Cross_Section.append(CrossSectionBuffer);

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

#Fernandez plots done at 165 degrees in lab frame, which is about 7.1 degrees CM frame. Lands on ring 3 (starting from 0), will take rings 1 thru 5
Fernandez_gs_ring_counts = [cut_gs_counts_132[i] for i in range(1, 6)];
Fernandez_ex_ring_counts = [cut_ex_counts_132[i] for i in range(1, 6)];

#beam_current = 12-13 epA, should probably still assume 33% transmission
charge_state = 10; # Assuming Ne is fully stripped
elec_charge = 1.6*10**(-19); # coulomb
#pps = beam_current / (charge_state*elec_charge*10**(12));

runtime =  1833; # entry 243 states 15 to 20 min, but I had this 1833 input from what I could pull scalars, so this is what I will stick with. 
#beam_particles = pps*runtime; # in ions

target_thickness = 285*10**(-6); # g/cm^2 from elog entry 226
methylene_molar_mass = 14.0266; #g/mol
PolypropeleneMolMass = methylene_molar_mass*3;
hydrogen_nuclei = (target_thickness/methylene_molar_mass)*(6.0221408*10**(23))*2; # Results in a number that agrees with LISE

CMAngles = [168.678, 167.42, 166.162, 164.904, 163.646, 162.388]
#LabAngles = [5.625, 6.25, 6.875, 7.5, 8.125, 8.75] # Lab angles for rings 1 thru 5 (counting from 0)

d_omega = 2*np.pi*(1-np.cos(CMAngles[0]*np.pi/180)) - 2*np.pi*(1 - np.cos(CMAngles[-1]*np.pi/180)); #rings 1 to 5

#Efficiency = 90.71428571428571/100;

BeamCurrent = [(sum(Fernandez_gs_ring_counts)/((CorrectedCrossSection[i]*10**(-27))*runtime*hydrogen_nuclei*d_omega))*(charge_state*elec_charge*10**12) for i in range(len(CorrectedCrossSection))]
#AvgBeamCurrent = (sum(BeamCurrent)/len(BeamCurrent))/Efficiency
AvgBeamCurrent = (sum(BeamCurrent)/len(BeamCurrent))

print('H atoms per cm^2: ', hydrogen_nuclei)
print('Solid Angle Coverage Rings 1 to 5: ', d_omega)
print('Beam Current: ', "%.2f" % AvgBeamCurrent, 'epA')

# Want to calculate beam current measured by each individual ring


for i in range(len(Fernandez_gs_ring_counts)):
	RingBeamCurrent = []
	RingSolidAngle = 2*np.pi*(1-np.cos(CMAngles[i]*np.pi/180)) - 2*np.pi*(1 - np.cos(CMAngles[i+1]*np.pi/180))
	for j in range(len(CorrectedCrossSection)):
		RingBeamCurrent.append((Fernandez_gs_ring_counts[i]/((CorrectedCrossSection[j]*10**(-27))*runtime*hydrogen_nuclei*RingSolidAngle))*(charge_state*elec_charge*10**12))
	RingAvgBeamCurrent = (sum(RingBeamCurrent)/len(RingBeamCurrent))
	print('Ring', i+1, 'Average Beam Current: ', "%.2f" % RingAvgBeamCurrent, ' epA')
		
		
		
		
		
		
		

