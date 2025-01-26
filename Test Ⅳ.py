#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import re
import pandas as pd
import numpy as np
import time

#number=2*10*22=440
start_time = time.time()
def seconds_to_hh_mm_ss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        
def calculate_RR(row):
    coef1 = row['RR_change']
    if row['Yangjun'] == 'North' and row['T'] >= 0:
        RR_Yangjun = (61.57*np.exp(-0.2699*( row['T']+21.8063)) + 0.2924*np.exp(0.04816*( row['T']+21.8063))- 1) * (1 - coef1) + 1
    elif row['Yangjun'] == 'Northeast' and row['T'] >= 0:
        RR_Yangjun = (355.4*np.exp(-0.3509*( row['T']+22.0315)) + 0.2439*np.exp(0.05717*( row['T']+22.0315))- 1) * (1 - coef1) + 1
    elif row['Yangjun'] == 'Northwest' and row['T'] >= 0:
        RR_Yangjun = (1205*np.exp(-0.3977*( row['T']+24.7636)) + 0.493*np.exp(0.02619*( row['T']+24.7636))- 1) * (1 - coef1) + 1
    elif row['Yangjun'] == 'East' and row['T'] >= 0:
        RR_Yangjun = (267.7*np.exp(-0.2907*( row['T']+24.4582)) + 0.1277*np.exp(0.07429*(row['T']+24.4582))- 1) * (1 - coef1) + 1
    elif row['Yangjun'] == 'Central' and row['T'] >= 0:
        RR_Yangjun = ((4.515e+05)*np.exp(-0.5707*( row['T']+25)) + 0.1356*np.exp(0.07097*(row['T']+25))- 1) * (1 - coef1) + 1
    elif row['Yangjun'] == 'South' and row['T'] >= 0:
        RR_Yangjun = (0.1363*np.exp(0.06902*( row['T']+28.8742))- 1) * (1 - coef1) + 1
    elif row['Yangjun'] == 'Southwest' and row['T'] >= 0:
        RR_Yangjun = ((2.474e+05)*np.exp(-0.9893*( row['T']+15)) + 0.4036*np.exp(0.05515*( row['T']+15))- 1) * (1 - coef1) + 1
    else:
        RR_Yangjun = 1
    return (RR_Yangjun-1)/RR_Yangjun

vSSPs=['SSP2','SSP5']
vYears=[2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040,2041,2042,2043,2044,2045,2046,2047,2048,2049,2050,2051,2052,2053,2054,2055]
vTs=['ACCESS1_0','bcc_csm1_1', 'BNU_ESM', 'CanESM2', 'CCSM4', 'CESM1_BGC', 'CNRM_CM5', 'CSIRO_Mk3_6_0', 'GFDL_CM3', 'GFDL_ESM2G', 'GFDL_ESM2M', 'inmcm4', 'IPSL_CM5A_LR', 'IPSL_CM5A_MR', 'MIROC_ESM', 'MIROC_ESM_CHEM', 'MIROC5', 'MPI_ESM_LR', 'MPI_ESM_MR', 'MRI_CGCM3', 'NorESM1_M']

for _ssp in vSSPs:
    for _year in vYears:
        strTemp='D:/5Figure1/2Temp_future/mod21_'+str(_year)+'_'+str(_ssp)+'.csv'
        f_temp = pd.read_csv(strTemp)
        # f_temp = pd.read_csv('D:/4new_data_hrd/2future temperature_from GEE/NewTemp_SSP2_RCP45_2030(UP2050).csv')
        # 读取tempcoef_mmt_fenqu_defT数据
        
        # 读取POP数据
        strPop='E:/Reviewer4/0support files/Test2POP/T2_'+str(_ssp)+'_'+str(_year)+'.csv'
        f_POP = pd.read_csv(strPop)
        f_POP['defT_level']=f_POP['defT_level'].fillna(0)
        f_GDP_Per = pd.read_csv('D:/5discussion_YAO/0support files/GDP/2010年全国各城市人均GDP统计_new.csv', encoding = 'ANSI')
        strPOP_FUT='D:/5Figure1/0support files/Future POP_shi/F_POP_'+str(_ssp)+'_'+str(_year)+'.csv'
        f_POP_future=pd.read_csv(strPOP_FUT,encoding='ANSI')
        strGDP_FUT='D:/5Figure1/0support files/Future GDP_shi/F_GDP_'+str(_ssp)+'_'+str(_year)+'.csv'
        f_GDP_future=pd.read_csv(strGDP_FUT,encoding='ANSI')
        for _T in vTs:
            result = pd.DataFrame()
            result = pd.merge(f_temp, f_POP, on = 'ID_new')
#             result['def_MMT'] = result['MFT'] - result['MMT'] 
#             result['def_MMT'] = result['def_MMT'].apply(lambda x : x if x <= 1 else 1) #
#             result['def_MMT'] = result['def_MMT'].apply(lambda x : x if x >= -1 else -1) #
            result['defT_new'] = (0.567 * np.log10(result['Area'])-0.02718)*0.91
            
            result['daily_intensity'] =  result[_T] + result['defT_new'] - result['MMT']# - result['def_MMT']
           
            df = pd.DataFrame(result[['ID_new','daily_intensity']])
            df = df[(df.daily_intensity)>0]
            grouped = df.groupby('ID_new').mean()
            result = pd.DataFrame()
            result = pd.merge(f_POP, grouped, how = 'left', on = 'ID_new')
            result['daily_intensity'] = result['daily_intensity'].fillna(0) #空值赋值为0
#             print(result)
            df = pd.DataFrame(f_GDP_Per[['市', '人均GDP']]) # 历史2010
            result = pd.merge(result, df, how = 'left', on = '市')
            df = pd.DataFrame(f_POP_future[['市', 'POP']])
            result = pd.merge(result, df, how = 'left', on = '市')
            df = pd.DataFrame(f_GDP_future[['市', 'GDP']])
            result = pd.merge(result, df, how = 'left', on = '市')
            result['GDP_fut'] =result['GDP'] * 8.1013/3.06344193166044
            result['GDPperP_fut'] = result['GDP_fut'] / result['POP']
            result['RR_his']=13.2312883*(result['daily_intensity']/(result['人均GDP']/1000))**2+0.2357026*(result['daily_intensity']/(result['人均GDP']/1000))+1.001445
            result['RR_fut']=13.2312883*(result['daily_intensity']/(result['GDPperP_fut']/1000))**2+0.2357026*(result['daily_intensity']/(result['GDPperP_fut']/1000))+1.001445
            result['RR_change'] = (result['RR_his']-result['RR_fut'])/result['RR_his']
            
            
            f_RRchange = pd.DataFrame(result[['ID_5buffer', 'RR_change']])
            #print(f_RRchange)
            result = pd.DataFrame()
            table1 = pd.merge(f_POP, f_temp, on = 'ID_new')
            result = pd.merge(table1, f_RRchange, on = 'ID_5buffer')
            
            result['T'] = result[f'{_T}']+ result['defT_level'] - result['MMT']
            result['AF']= result.apply(calculate_RR, axis=1)
            result['ED'] = result['POP_new']*result['MR']*result['AF']/1000
            grouped = result.groupby('ID_5buffer').sum(numeric_only=True).reset_index()
            df_output = pd.merge(f_POP,grouped[['ID_5buffer','ED']], on = 'ID_5buffer')
            strOutput='E:/Reviewer4/5Test3/ED/T3_ED_'+str(_T)+'_'+str(_ssp)+'_'+str(_year)+'.csv'
            df_output.to_csv(strOutput,index = None,encoding='utf_8_sig')
            print(strOutput)
end_time = time.time()
elapsed_time = round(end_time - start_time)
formatted_time = seconds_to_hh_mm_ss(elapsed_time)
print(f"运行时间：{formatted_time}")


# In[ ]:




