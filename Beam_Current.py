import numpy as np
import matplotlib.pyplot as plt
import csv as csv 

cut_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/134MeV/Elastics/7.95kG/Beam_Elastic_Counts_cut.csv";

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
Nucleons = 20;
Beam_Energy_Per_Nucleon = Beam_Energy/Nucleons-0.06;

Energy = 0;
Cross_Section = 0;
min_diff = 1;

for i in range(len(Fernandez_Energy)):
	diff = abs(Beam_Energy_Per_Nucleon - Fernandez_Energy[i]);
	if diff < min_diff:
		min_diff = diff;
		Energy = Fernandez_Energy[i];
		Cross_Section = Fernandez_Cross_Section[i];

print('Fernandez Energy: ', Energy);
print('Fernandez Differential Cross Section (mb): ', Cross_Section);

#Fernandez plots done at 165 degrees in lab frame, which is about 7.946 degrees CM frame. Lands on ring 3, will take rings 1 thru 5
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

d_omega = 2*np.pi*(1-np.cos(168.673*np.pi/180)) - 2*np.pi*(1 - np.cos(162.381*np.pi/180)); #rings 1 to 5

BeamCurrent = (sum(Fernandez_gs_ring_counts)/((Cross_Section*10**(-27))*runtime*hydrogen_nuclei*d_omega))*(charge_state*elec_charge*10**12)

print('H atoms per cm^2: ', hydrogen_nuclei)
print('Time Correlated Proton Count: ', sum(Fernandez_gs_ring_counts))
print('Solid Angle Coverage Rings 1 to 5: ', d_omega)
print('Beam Current (epA): ', BeamCurrent)


'''
# d_omega = 2*np.pi*(1 - np.cos((15*np.pi/180) - (5*np.pi/180))); # should be about 3 quarters of a steradian, will need to figure out how that out

cross_section_ex = (sum(Fernandez_ex_ring_counts)/(hydrogen_nuclei*beam_particles*d_omega))*10**(27);
cross_section_gs = (sum(Fernandez_gs_ring_counts)/(hydrogen_nuclei*beam_particles*d_omega))*10**(27);
cross_section_total = (sum(Fernandez_gs_ring_counts)+sum(Fernandez_ex_ring_counts))/(hydrogen_nuclei*beam_particles*d_omega)*10**(27); # denominator should be on order 10^29

print('20Ne(p, p)20Ne* Cross Section (mb): ', cross_section_ex, '\n');
print('20Ne(p, p)20Ne Cross Section (mb): ', cross_section_gs, '\n');
print('Total Cross Section (mb): ', cross_section_total);
'''








