#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '..\\..\OneDrive - Helena Chemical Company\Desktop\stage\workspace\PFiles\class\ml'))
	print(os.getcwd())
except:
	pass

#%%
# dataset found here:
# pesticide: https://www.kaggle.com/usgs/pesticide-use/version/1
# food growth: https://www.kaggle.com/dorbicycle/world-foodfeed-production

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import requests
from bs4 import BeautifulSoup


#%%
# high and low estimates of pesticide use per county
df_2014 = pd.read_csv('data/pesticide_use/2014.csv')
df_2015 = pd.read_csv('data/pesticide_use/2015.csv')
df_dict = pd.read_csv('data/pesticide_use/dictionary.csv')

df_pestuse14 = pd.merge(df_dict, df_2014, how='right')
df_pestuse14.rename(columns={'LOW_ESTIMATE':'14_LOW_ESTIMATE','HIGH_ESTIMATE':'14_HIGH_ESTIMATE'}, inplace=True)
df_pestuse14.drop(['YEAR'], axis=1,inplace=True)

df_pestuse15 = pd.merge(df_dict, df_2015, how='right')
df_pestuse15.rename(columns={'LOW_ESTIMATE':'15_LOW_ESTIMATE','HIGH_ESTIMATE':'15_HIGH_ESTIMATE'}, inplace=True)
df_pestuse15.drop(['YEAR'], axis=1,inplace=True)

df_pestuse = pd.merge(df_pestuse14, df_pestuse15, how='left')
df_pestuse.drop(['STATE_CODE','COUNTY_CODE'], axis=1,inplace=True)
df_pestuse.index += 1

df_pestuse = df_pestuse.fillna(0)


#%%
df_pestuse.head()


#%%
# get average annual rainfall from below site
r = requests.get('https://www.currentresults.com/Weather/US/average-annual-state-precipitation.php')
soup = BeautifulSoup(r.text, 'lxml')

df1 = pd.read_html(str(soup.find_all('table')[0]))[0]
df2 = pd.read_html(str(soup.find_all('table')[1]))[0]
df3 = pd.read_html(str(soup.find_all('table')[2]))[0]

df1_indexed = df1.set_index('State')
df2_indexed = df2.set_index('State')
df3_indexed = df3.set_index('State')

df_rain = pd.concat([df1_indexed, df2_indexed, df3_indexed])
df_rain = df_rain.sort_values('State', ascending=True)
df_rain = df_rain.drop(['Rank'], axis=1)
df_rain = df_rain.reset_index()
df_rain.head()


#%%
r = requests.get('https://www.omnisci.com/docs/latest/3_apdx_states.html')
soup = BeautifulSoup(r.text, 'lxml')

df_stateabr = pd.read_html(str(soup.find_all('table')))
df_state = df_stateabr[0]
df_state.head()


#%%
# use lookup to get appropriate state abbreviations for average rainfall, then merge with pesticide table
df_rainfall = pd.merge(df_rain, df_state, how='left')
df_rainfall.drop(['State','Milli­metres'], axis=1, inplace=True) # note odd symbol in millimetres
df_rainfall.rename(columns={'Abbreviation':'STATE', 'Inches':'RAIN_INCHES'}, inplace=True)
df_rainfall.head()


#%%
pestuse_withrain = pd.merge(df_pestuse, df_rainfall, how='left')
pestuse_withrain.head()


#%%
# plot mississippi
ms_pestuse = pestuse_withrain[pestuse_withrain['STATE'] == 'MS']
ms_pestuse.reset_index(inplace=True)
ms_pestuse.drop(['index'], axis=1,inplace=True)

# just bolivar county
ms_bolivar_pestuse = ms_pestuse[ms_pestuse['COUNTY'] == 'Bolivar County']
ms_bolivar_pestuse.head()


#%%
ms_bolivar_pestuse.set_index(['COMPOUND'], inplace=True)
#ms_bolivar_15sorted.head()


#%%
ms_bolivar_sorted = ms_bolivar_pestuse.sort_values(by=['15_HIGH_ESTIMATE'], ascending=False)
# don't need rain for one county - all the same
ms_bolivar_sorted.drop(['RAIN_INCHES'], axis=1, inplace=True)


#%%
ms_bolivar_sorted.head()


#%%
ms_bolivar_sorted['15_AVG'] = ms_bolivar_sorted[['15_LOW_ESTIMATE', '15_HIGH_ESTIMATE']].mean(axis=1)
ms_bolivar_sorted['14_AVG'] = ms_bolivar_sorted[['14_LOW_ESTIMATE', '14_HIGH_ESTIMATE']].mean(axis=1)
ms_bolivar_final = ms_bolivar_sorted.drop(['14_LOW_ESTIMATE', '15_LOW_ESTIMATE', '15_HIGH_ESTIMATE', '14_HIGH_ESTIMATE'], axis=1)
ms_bolivar_final.head()


#%%
ms_bolivar_final = ms_bolivar_final.sort_values(by=['15_AVG'], ascending=False)
ms_bolivar_final.head()


#%%
#plot mississippi
fig = plt.figure()
plt.style.use('ggplot')
ms_bolivar_final.plot(subplots=True, figsize=(10,15))


