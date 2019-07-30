# From UCI dataset, citations:

# U. S. Department of Commerce, Bureau of the Census, Census Of Population And Housing 
# 1990 United States: Summary Tape File 1a & 3a (Computer Files),

# U.S. Department Of Commerce, Bureau Of The Census Producer, Washington, DC and 
# Inter-university Consortium for Political and Social Research Ann Arbor, Michigan. 
# (1992)

# U.S. Department of Justice, Bureau of Justice Statistics, Law Enforcement Management 
# And Administrative Statistics (Computer File) U.S. Department Of Commerce, Bureau Of 
# The Census Producer, Washington, DC and Inter-university Consortium for Political and 
# Social Research Ann Arbor, Michigan. (1992)

# U.S. Department of Justice, Federal Bureau of Investigation, Crime in the United 
# States (Computer File) (1995)

# Redmond, M. A. and A. Baveja: A Data-Driven Software Tool for Enabling Cooperative 
# Information Sharing Among Police Departments. European Journal of Operational Research 
# 141 (2002) 660-678. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

crime_data = np.genfromtxt("data/crime/communities.data",delimiter=",")
# delete columns for county, community and community name due to missing data and low predictive quality
# remove stats relating to police - around 85% missing data
arr1 = np.array([1,2,3])
arr2 = np.arange(101,118,1)
arr3 = np.arange(121,125,1)
arr = np.concatenate([arr1,arr2,arr3,[126]])
crime_data_r = np.delete(crime_data, arr,axis=1)

#print(np.isnan(crime_data_r))
print(type(crime_data_r[1,0]))