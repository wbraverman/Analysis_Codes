import numpy as np
import matplotlib.pyplot as plt
import csv as csv 

ring_spacing = ((15*np.pi / 180) - (5*np.pi / 180)) / 16;
#ring_num = [i for i in range(0, 16) if i!=11 and i!=1 and i!=14];
ring_num = [i for i in range(0, 16) if i!=11];
ring_angle = [((5*np.pi/180)+(ring_num[i]*ring_spacing) + ring_spacing/2) for i in range(len(ring_num))]; # ring midpoint angle

cut_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/132MeV/Elastics/9.87kG/Beam_Elastic_Counts_cut.csv";

with open(cut_data) as csvfile:
    lines = csvfile.readlines()[1:];
    cut_gs_counts_132 = [round(float(i.split(',', 2)[1]), 0) for i in lines[0:]];
    cut_gs_error_132 = [round(float(i.split(',', 3)[2]), 0) for i in lines[0:]];
    cut_ex_counts_132 = [round(float(i.split(',', 4)[3]), 0) for i in lines[0:]];
    cut_ex_error_132 = [round(float(i.split(',', 5)[4]), 0) for i in lines[0:]];

#Fernandez plots done at 165 degrees in lab frame, which is about 7.453 degrees. Lands on edge of ring 2, will take rings 1 thru 5
Fernandez_gs_ring_counts = [cut_gs_counts_132[i] for i in range(0, 5)];
Fernandez_ex_ring_counts = [cut_ex_counts_132[i] for i in range(0, 5)];

beam_current = 7; # in epA, taking 30% transmission rate from operator's last cup, entry 262
charge_state = 10; # Assuming Ne is fully stripped
elec_charge = 1.6*10**(-19); # coulomb
pps = beam_current / (charge_state*elec_charge*10**(12));

runtime = 2545+470; # run 246 ~7 min and run 246 is 470 seconds, run 247 is 2545 seconds
beam_particles = pps*runtime; # in ions

target_thickness = 285*10**(-6); # g/cm^2 from elog entry 226
methylene_molar_mass = 14.0266; #g/mol
hydrogen_nuclei = (target_thickness/methylene_molar_mass)*(6.0221408*10**(23))*2;


# d_omega = 2*np.pi*(1 - np.cos((15*np.pi/180) - (5*np.pi/180))); # should be about 3 quarters of a steradian, will need to figure out how that out
d_omega = 2*np.pi*(1-np.cos(168.679*np.pi/180)) - 2*np.pi*(1 - np.cos(162.39*np.pi/180)); #rings 1 to 5

cross_section_ex = (sum(Fernandez_ex_ring_counts)/(hydrogen_nuclei*beam_particles*d_omega))*10**(27);
cross_section_gs = (sum(Fernandez_gs_ring_counts)/(hydrogen_nuclei*beam_particles*d_omega))*10**(27);
cross_section_total = (sum(Fernandez_gs_ring_counts)+sum(Fernandez_ex_ring_counts))/(hydrogen_nuclei*beam_particles*d_omega)*10**(27); # denominator should be on order 10^29



print('20Ne(p, p)20Ne* Cross Section (mb): ', cross_section_ex, '\n');
print('20Ne(p, p)20Ne Cross Section (mb): ', cross_section_gs, '\n');
print('Total Cross Section (mb): ', cross_section_total, '\n');
print('Beam Current times Target Thickness: ', beam_particles*hydrogen_nuclei)
	

