#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import pandas as pd
import numpy as np
import time
start_time = time.time()
def seconds_to_hh_mm_ss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
vSSPs=['SSP2','SSP5']
vYears=[2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040,2041,2042,2043,2044,2045,2046,2047,2048,2049,2050,2051,2052,2053,2054,2055]
vTs=['ACCESS1_0','bcc_csm1_1', 'BNU_ESM', 'CanESM2', 'CCSM4', 'CESM1_BGC', 'CNRM_CM5', 'CSIRO_Mk3_6_0', 'GFDL_CM3', 'GFDL_ESM2G', 'GFDL_ESM2M', 'inmcm4', 'IPSL_CM5A_LR', 'IPSL_CM5A_MR', 'MIROC_ESM', 'MIROC_ESM_CHEM', 'MIROC5', 'MPI_ESM_LR', 'MPI_ESM_MR', 'MRI_CGCM3', 'NorESM1_M']

for _ssp in vSSPs:
    for _year in vYears:
        for _T in vTs:
            #for _vsen in vSenarios:
            strTemp='D:/5Figure1/2Temp_future/mod21_'+str(_year)+'_'+str(_ssp)+'.csv'
            f_temp = pd.read_csv(strTemp)
                # f_temp = pd.read_csv('D:/4new_data_hrd/2future temperature_from GEE/NewTemp_SSP2_RCP45_2030(UP2050).csv')
                # 读取tempcoef_mmt_fenqu_defT数据
            strPop='D:/5Figure1/0support files/Test1POP/T1_'+str(_ssp)+'_'+str(_year)+'.csv'
            f_POP = pd.read_csv(strPop)
                # f_POP = pd.read_csv('D:/4new_data_hrd/4Test1/POP_test1/SSP2_2050_test1_pop.csv',encoding='ANSI')
                # 根据列名读取温度数据


                    # 连接温度、分区和MMT表
            result = pd.DataFrame()
            result = pd.merge(f_temp, f_POP, on = 'ID_new')
                    # 分区计算每一行的RR（Yang）（不考虑适应性）
            #coef_list=['coef_1','coef_2','coef_3','coef_4','coef_5']
            
            RR_result = []
            for row in result.itertuples():
                
                T = getattr(row,str(_T)) - row.MMT
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
            strOutput='D:/5Figure1/5Test1/ED/T1_ED_'+str(_T)+'_'+str(_ssp)+'_'+str(_year)+'.csv'
            result_ED_new.to_csv(strOutput, index = None,encoding='utf_8_sig')
            print(strOutput)
end_time = time.time()
elapsed_time = round(end_time - start_time)
formatted_time = seconds_to_hh_mm_ss(elapsed_time)
print(f"运行时间：{formatted_time}")


# In[ ]:




