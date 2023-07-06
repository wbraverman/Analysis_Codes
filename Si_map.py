# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:52:32 2022

@author: wbrav
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 15 05:02:03 2022

@author: wbrav
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import time


start_time = time.time();

#mpl.rcParams['agg.path.chunksize'] = 10000

data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/141MeV/PAlpha/7.51kG/rings_wedges.csv";

with open(data) as csvfile:
    lines = csvfile.readlines()[1:];
    ring_num = [int(i.split(',', 1)[0]) for i in lines[0:]];
    wedge_num = [int(i.split(',', 2)[1]) for i in lines[0:]];
    num_counts = [int(i.split(',',3)[2]) for i in lines[0:]];

ring_num_nonzero =[];
wedge_num_nonzero = [];
counts_nonzero = [];

for i in range(len(ring_num)):
    if num_counts[i] != 0 and wedge_num[i]!=4:
        ring_num_nonzero.append(ring_num[i]);
        wedge_num_nonzero.append(wedge_num[i]);
        counts_nonzero.append(num_counts[i]);
        

r = [((70-22)/16)*(ring_num_nonzero[i]+1) for i in range(len(ring_num_nonzero)) ];
theta = [(((2*np.pi)/16)*(wedge_num_nonzero[i]+1) - np.pi/2) for i in range(len(wedge_num_nonzero))];  


ax = plt.subplot(111, polar=True);
ax.set_rmax(70);
ax.set_rmin(22);
cm = plt.cm.get_cmap('rainbow')

sc = ax.scatter(theta, r, label='events', c=counts_nonzero, vmin=0, vmax=max(counts_nonzero), alpha=0.75, edgecolor='k', cmap=cm); 
plt.colorbar(sc)

plt.show()

print("--- %s seconds ---" % (time.time() - start_time));
