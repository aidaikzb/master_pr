#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:30:11 2022

@author: aidai
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: aidai
"""
#%% Memory task. Input: 15 segments, 30 ms each. 7 segments from template 1 and 
#                8 segments from template 2 are randomly permuted. 

import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd

# function for creating poisson train. 
def homogeneous_poisson(rate, tmax, bin_size):
    nbins = np.floor(tmax/bin_size).astype(int)
    prob_of_spike = rate * bin_size
    spikes = np.random.rand(nbins) < prob_of_spike
    return spikes 

# function for previous function on several trials
def homogeneous_poisson_generator(n_trials, rate, tmax, bin_size):
    for i in range(n_trials):
        yield homogeneous_poisson(rate, tmax, bin_size)


# initialize constants

label1= 0      # template1
label2 = 1     # template2

rate1 = 40     # spike rate for template 1
rate2 = 60    # spike rate for template 2
bin_size = 0.001  # bin size  [s]
tmax = 0.03       # the total time lenght of each segment [s]

trials = 50     #trials for testing



# empty matricies of poisson trains for two templates: 7 segments for template1;
#                                                      8 segments for template2.

spikes_poisson0 = np.zeros((trials, 7, int(tmax/bin_size)))
spikes_poisson1 = np.zeros((trials, 8, int(tmax/bin_size)))
all_spikes2 = np.zeros((trials, 15, int(tmax/bin_size)))

all_spikes = np.zeros((trials, 15, int(tmax/bin_size)))
ind = np.zeros((50,15))
ind = ind.astype(int)

# empty varables to save 4 different outputs later
out1 = np.zeros((trials,15))
out2 = np.zeros((trials,15))
out3 = np.zeros((trials,15))
out4 = np.zeros((trials,15))

#%% for saving output ina dict
#output1 =[]
#output2 = []
#output3 = []
#output4 = []
#for o in range(trials):
#    output1.append([])
#    output2.append([])
#    output3.append([])
#    output4.append([])

#%%
# poisson trians for n trials
for ii in range(trials):
    
    spikes_poisson0[ii] = list(homogeneous_poisson_generator(7,rate1, tmax, bin_size))
    spikes_poisson1[ii] = list(homogeneous_poisson_generator(8,rate2, tmax, bin_size))

# all segments from both templates concatenated and permuted    
    all_spikes2 = np.concatenate((spikes_poisson0,spikes_poisson1), axis = 1)
    ind[ii] = (np.random.permutation(all_spikes2.shape[1]))
    all_spikes[ii,:,:] = all_spikes2[ii,ind[ii],:]
       
#%% Output for 4 different dt

# memory task for each segment. output: segment number -> label of the template 

#for ii in range(trials):
    all_sp = all_spikes[ii, :, :]
    #random.shuffle(all_sp)
    spikes_poi0 = spikes_poisson0[ii, :, :]
    spikes_poi1 = spikes_poisson1[ii, :, :]
    
    for i, seg in enumerate(all_sp):
    
        if any((all_sp[i] == x).all() for x in spikes_poi0):
            #print("segment ", i, "is from ", label1)
            out1[ii, i] = label1
            #output1[ii].append({i:label1})
        else:
            #print("segment ", i, "is from ", label2)
            #output1[ii].append({i:label2})
            out1[ii, i] = label2
            
# memory task for segment with dt 30 [ms](1 segments bofore). 
# output: segment number -> label of the template of previous segment
    dt1 = 0.03 #[s]

    step1 = int(dt1/tmax)
    print("\n")
    for i in range(len(all_sp)-1,0 ,-1):
        
        if any((all_sp[i-step1] == x).all() for x in spikes_poi0):
            #print("for segment ", i, ": segment " ,i-step1, "is from ", label1)
            out2[ii, i] = label1
           # output2[ii].append({i:label1})
        else:
            #print("for segment ", i, ": segment " ,i-step1, "is from ", label2)
            out2[ii, i] = label2
            #output2[ii].append({i:label2})

# memory task for segment with dt 60 [ms](2 segments bofore). 
# output: segment number -> label of the template of 2 segments before
    dt2 = 0.06 #[s]
    step2 = int(dt2/tmax)

    print("\n")
    for i in range(len(all_sp)-1, 1 ,-1):

        if any((all_sp[i-step2] == x).all() for x in spikes_poi0):
            #print("for segment ", i, ": segment " ,i-step2, "is from ", label1)
            out3[ii, i] = label1
            #output3[ii].append({i:label1})
        else:
            #print("for segment ", i, ": segment " ,i-step2, "is from ", label2)
            out3[ii, i] = label2
            #output3[ii].append({i:label2})
# memory task for segment with dt 90 [ms](3 segments bofore). 
# output: segment number -> label of the template of 3 segments before
    dt3 = 0.09 #[s]

    step3 = int(dt3/tmax)
    
    print("\n")
    for i in range(len(all_sp)-1, 2 ,-1):
        
        if any((all_sp[i-step3] == x).all() for x in spikes_poi0):
            #print("for segment ", i, ": segment " ,i-step3, "is from ", label1)
            out4[ii, i] = label1
            #output4[ii].append({i:label1})
        else:
            #print("for segment ", i, ": segment " ,i-step3, "is from ", label2)
            out4[ii, i] = label2
            #output4[ii].append({i:label2})
            
#%% Visualization of input-output 3 segment, all trials

# input
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.spy(all_spikes[:,0,:], marker='.', origin = 'lower')
ax1.set_title('segment1')
ax2.spy(all_spikes[:,1,:],marker='.', origin = 'lower')
ax2.set_title('segment2')
ax3.spy(all_spikes[:,2,:],marker='.', origin = 'lower')
ax3.set_title('segment3')

#output
#%%
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
ax1.spy(out1, marker='.', origin = 'lower')
ax1.set_title('output1')
ax2.spy(out2,marker='.', origin = 'lower')
ax2.set_title('output2')
ax3.spy(out3,marker='.', origin = 'lower')
ax3.set_title('output3')
ax4.spy(out4,marker='.', origin = 'lower')
ax4.set_title('output4')
#%% Amorphous NN
            
import networkx as nx
import random
n = random.randrange(100)
p = random.uniform(0,1)
seed = random.randrange(12345)
amorph_graph = nx.gnp_random_graph(n, p, seed, directed = True)


#%% Small world NN

n = random.randrange(100)
k = random.randrange(10)
p = random.uniform(0,1)
small_w_graph = nx.watts_strogatz_graph(n, k,p)























