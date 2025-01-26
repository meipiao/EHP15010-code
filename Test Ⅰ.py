#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import pandas as pd
import numpy as np
import time

#number=2*5*2=20
start_time = time.time()
def seconds_to_hh_mm_ss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
vSSPs=['SSP2','SSP5']
# vYears=[2008,2009,2010,2011,2012]
vYears=[2005,2006,2007]
# vSenarios=[2030,2050]
#vYears=[2030,2050,2100]
vTs=['mean']
for _ssp in vSSPs:
    for _year in vYears:
        strTemp='D:/source/His_'+str(_year)+'_'+str(_ssp)+'.csv'
        f_temp = pd.read_csv(strTemp)

        strPop='D:/5Figure1/0support files/Test0POP/T0_'+str(_ssp)+'_'+str(_year)+'.csv'
        f_POP = pd.read_csv(strPop)
 
        for _T in vTs:

            result = pd.DataFrame()
            result = pd.merge(f_temp, f_POP, on = 'ID_new')
            print(result)

            RR_result = []
            for row in result.itertuples():

                T=getattr(row,str(_T))- row.MMT
             
                if row.Yangjun == 'North' and T >= 0:
                    RR_Yangjun = 61.57*np.exp(-0.2699*(T+21.8063)) + 0.2924*np.exp(0.04816*(T+21.8063))
                elif row.Yangjun == 'Northeast' and T >= 0:
                    RR_Yangjun = 355.4*np.exp(-0.3509*(T+22.0315)) + 0.2439*np.exp(0.05717*(T+22.0315))
                elif row.Yangjun == 'Northwest' and T >= 0:
                    RR_Yangjun = 1205*np.exp(-0.3977*(T+24.7636)) + 0.493*np.exp(0.02619*(T+24.7636))
                elif row.Yangjun == 'East' and T >= 0:
                    RR_Yangjun = 267.7*np.exp(-0.2907*(T+24.4582)) + 0.1277*np.exp(0.07429*(T+24.4582))
                elif row.Yangjun == 'Central' and T >= 0:
                    RR_Yangjun = (4.515e+05)*np.exp(-0.5707*(T+25)) + 0.1356*np.exp(0.07097*(T+25))
                elif row.Yangjun == 'South' and T >= 0:
                    RR_Yangjun = 0.1363*np.exp(0.06902*(T+28.8742))
                elif row.Yangjun == 'Southwest' and T >= 0:
                    RR_Yangjun = (2.474e+05)*np.exp(-0.9893*(T+15)) + 0.4036*np.exp(0.05515*(T+15))
                else:
                    RR_Yangjun = 1
                RR_result.append(RR_Yangjun)
            result['RR_Clim-MMT'] = RR_result
            result['(RR-1)/RR'] = (result['RR_Clim-MMT'] - 1)/result['RR_Clim-MMT']
            df = pd.DataFrame(result[['ID_new1','(RR-1)/RR']])
            grouped = df.groupby('ID_new1').sum()
            result_ED = pd.merge(f_POP, grouped, on = 'ID_new1')
            result_ED_new = result_ED.rename(columns={'(RR-1)/RR': 'RR_sum'})
            result_ED_new['ED'] = result_ED_new['POP_new']/1000 * result_ED_new['MR'] * result_ED_new['RR_sum']
            strOutput='D:/5Figure1/4Test0/ED/T0_ED_'+str(_ssp)+'_2020_'+str(_year)+'.csv'
            result_ED_new.to_csv(strOutput, index = None,encoding='utf_8_sig')
            print(strOutput)
end_time = time.time()
elapsed_time = round(end_time - start_time)
formatted_time = seconds_to_hh_mm_ss(elapsed_time)
print(f"运行时间：{formatted_time}") 


# In[ ]:




