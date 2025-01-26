#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import pandas as pd
import numpy as np
import time
import random


# In[2]:


def seconds_to_hh_mm_ss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


# In[3]:


# tmp_folder_path = r'D:\5Figure1\2Temp_future_new'
# pop_folder_path = r'E:\Reviewer4\0support files\Test2POP'

# gdp_path = r'D:\5Figure1\0support files\GDP\2010年全国各城市人均GDP统计_new.csv'
# f_GDP_Per = pd.read_csv(gdp_path, encoding = 'ANSI')

# fpop_folder_path = 'D:/5Figure1/0support files/Future POP_shi'
# fGDP_folder_path = 'D:/5Figure1/0support files/Future GDP_shi'

# out_path = r'E:\Reviewer4\6Test4allfactors_positive'

# #vSSPs=['SSP2','SSP5']
# #vYears=[x for x in range(2016, 2056)]

# vSSPs=['SSP2']#,'SSP5']
# vYears=[x for x in range(2016, 2026)]
# iters = 1000



# start_time = time.time()
# for _ssp in vSSPs:
#     for _year in vYears:
#         sum_pop_list = []
#         sum_ED_list = []
        
#         for idx in range(iters):
        
#             tmp_path = tmp_folder_path+'\\'+'mod21_'+str(_year)+'_'+_ssp+'.csv'
#             f_temp = pd.read_csv(tmp_path)

#             model1 = f_temp.columns[3]
#             model = list(f_temp.columns[5:])
#             model.append(model1)

#             pop_path = pop_folder_path+'\\'+'T2_'+str(_ssp)+'_'+str(_year)+'.csv'
#             f_POP = pd.read_csv(pop_path)

#             strPOP_FUT=fpop_folder_path+'\\'+'F_POP_'+str(_ssp)+'_'+str(_year)+'.csv'
#             f_POP_future=pd.read_csv(strPOP_FUT,encoding='ANSI')

#             strGDP_FUT=fGDP_folder_path+'\\'+'F_GDP_'+str(_ssp)+'_'+str(_year)+'.csv'
#             f_GDP_future=pd.read_csv(strGDP_FUT,encoding='ANSI')
            
#             _T = 'mean'
#             d = random.uniform(0.1,0.4)
#             e = random.uniform(0.1, 0.37)
#             f = random.uniform(0.08, 0.18)
#             g = random.uniform(0.05, 0.17)
            
#             result = pd.DataFrame()
#             result = pd.merge(f_temp, f_POP, on = 'ID_new')
#             result=pd.merge(result, f_GDP_Per, on = '市')

#             result['defT_new1'] = (0.567 * np.log10(result['Area'])-0.02718)*0.91

            
#             result['daily_intensity'] =  result[_T] + result['defT_new1'] - result['MMT']-(d+e)-(f+g) * result['建筑比例'] #- result['def_MMT']
#             df = pd.DataFrame(result[['ID_new','daily_intensity']])
#             df = df[(df.daily_intensity)>0]
#             grouped = df.groupby('ID_new').mean()
#             result = pd.DataFrame()
#             result = pd.merge(f_POP, grouped, how = 'left', on = 'ID_new')
#             result['daily_intensity'] = result['daily_intensity'].fillna(0) #空值赋值为0

#             df = pd.DataFrame(f_GDP_Per[['市', '人均GDP']]) # 历史2010
#             result = pd.merge(result, df, how = 'left', on = '市')
#             df = pd.DataFrame(f_POP_future[['市', 'POP']])
#             result = pd.merge(result, df, how = 'left', on = '市')
#             df = pd.DataFrame(f_GDP_future[['市', 'GDP']])
#             result = pd.merge(result, df, how = 'left', on = '市')
#             result['GDP_fut'] =result['GDP'] * 8.1013/3.06344193166044
#             result['GDPperP_fut'] = result['GDP_fut'] / result['POP']
#             result['RR_his']=13.2312883*(result['daily_intensity']/(result['人均GDP']/1000))**2+0.2357026*(result['daily_intensity']/(result['人均GDP']/1000))+1.001445
#             result['RR_fut']=13.2312883*(result['daily_intensity']/(result['GDPperP_fut']/1000))**2+0.2357026*(result['daily_intensity']/(result['GDPperP_fut']/1000))+1.001445
#             result['RR_change'] = (result['RR_his']-result['RR_fut'])/result['RR_his']

#             df = pd.DataFrame(f_GDP_Per[['市', '建筑比例']])
#             result = pd.merge(result, df, how = 'left', on = '市')

#             f_RRchange = pd.DataFrame(result[['ID_5buffer', 'RR_change', '建筑比例']])

#             result = pd.DataFrame()
#             table1 = pd.merge(f_POP, f_temp, on = 'ID_new')
#             result = pd.merge(table1, f_RRchange, on = 'ID_5buffer')
#             result['defT_new1'] = (0.567 * np.log10(result['Area'])-0.02718)*0.91 # 计算热岛强度的升温

#             coef_list = ['coef_1','coef_2','coef_3','coef_4','coef_5']

#             for i in range(len(coef_list)):       

#                 RR_result = []
#                 for row in result.itertuples():
#                 #     print(row.Temp) # 输出每一行
#                     T = getattr(row,str(_T))+ getattr(row,coef_list[i]) * row.defT_new1/row.sum_coef_area - row.MMT-(d+e)-(f+g) * row.建筑比例 #- row.def_MMT
#                     coef = row.RR_change
#                     if row.Yangjun == 'North' and T >= 0:
#                         RR_Yangjun = (61.57*np.exp(-0.2699*(T+21.8063)) + 0.2924*np.exp(0.04816*(T+21.8063))- 1) * (1 - coef) + 1
#                     elif row.Yangjun == 'Northeast' and T >= 0:
#                         RR_Yangjun = (355.4*np.exp(-0.3509*(T+22.0315)) + 0.2439*np.exp(0.05717*(T+22.0315))- 1) * (1 - coef) + 1
#                     elif row.Yangjun == 'Northwest' and T >= 0:
#                         RR_Yangjun = (1205*np.exp(-0.3977*(T+24.7636)) + 0.493*np.exp(0.02619*(T+24.7636))- 1) * (1 - coef) + 1
#                     elif row.Yangjun == 'East' and T >= 0:
#                         RR_Yangjun = (267.7*np.exp(-0.2907*(T+24.4582)) + 0.1277*np.exp(0.07429*(T+24.4582))- 1) * (1 - coef) + 1
#                     elif row.Yangjun == 'Central' and T >= 0:
#                         RR_Yangjun = ((4.515e+05)*np.exp(-0.5707*(T+25)) + 0.1356*np.exp(0.07097*(T+25))- 1) * (1 - coef) + 1
#                     elif row.Yangjun == 'South' and T >= 0:
#                         RR_Yangjun = (0.1363*np.exp(0.06902*(T+28.8742))- 1) * (1 - coef) + 1
#                     elif row.Yangjun == 'Southwest' and T >= 0:
#                         RR_Yangjun = ((2.474e+05)*np.exp(-0.9893*(T+15)) + 0.4036*np.exp(0.05515*(T+15))- 1) * (1 - coef) + 1
#                     else:
#                         RR_Yangjun = 1
#                     RR_result.append(RR_Yangjun)
#                 result['RR_Clim+UHI-MMT_'+str(i+1)] = RR_result
#                 result['RR_'+str(i+1)] = (result['RR_Clim+UHI-MMT_'+str(i+1)] - 1)/result['RR_Clim+UHI-MMT_'+str(i+1)]

#             df = pd.DataFrame(result[['ID_5buffer','RR_1', 'RR_2', 'RR_3', 'RR_4', 'RR_5']])
#             grouped = df.groupby('ID_5buffer').sum()

#             result_ED = pd.merge(f_POP, grouped, on = 'ID_5buffer')

#             ED_list = []
#             for row in result_ED.itertuples():
#             #     print(row.Temp) # 输出每一行
#                 if row.gridcode == 1:
#                     ED = row.POP_new/1000 * row.MR * row.RR_1
#                 elif row.gridcode == 2:
#                     ED = row.POP_new/1000 * row.MR * row.RR_2
#                 elif row.gridcode == 3:
#                     ED = row.POP_new/1000 * row.MR * row.RR_3
#                 elif row.gridcode == 4:
#                     ED = row.POP_new/1000 * row.MR * row.RR_4
#                 elif row.gridcode == 5:
#                     ED = row.POP_new/1000 * row.MR * row.RR_5
#                 else:
#                     ED = 0
#                 ED_list.append(ED)
#             result_ED['ED'] = ED_list

#             sum_pop_list.append(sum(result_ED['POP_new']))
#             sum_ED_list.append(sum(result_ED['ED']))
            
#         # 创建一个包含两个列表数据的DataFrame
#         data_frame = pd.DataFrame({'pop': sum_pop_list, 'ED': sum_ED_list})

#         # 将DataFrame导出为CSV文件（假设文件名为'output_file.csv'）
#         data_frame.to_csv(out_path+'\\'+str(_ssp)+'_'+str(_year)+'.csv', index=False)
            
        
# end_time = time.time()
# elapsed_time = round(end_time - start_time)
# formatted_time = seconds_to_hh_mm_ss(elapsed_time)
# print(f"运行时间：{formatted_time}")              


# In[5]:


tmp_folder_path = r'D:\5Figure1\2Temp_future_new'
pop_folder_path = r'E:\Reviewer4\0support files\Test2POP'

gdp_path = r'D:\5Figure1\0support files\GDP\2010年全国各城市人均GDP统计_new.csv'
f_GDP_Per = pd.read_csv(gdp_path, encoding = 'ANSI')

fpop_folder_path = 'D:/5Figure1/0support files/Future POP_shi'
fGDP_folder_path = 'D:/5Figure1/0support files/Future GDP_shi'

out_path = r'E:\Reviewer4\6Test4allfactors_positive'

#vSSPs=['SSP2','SSP5']
#vYears=[x for x in range(2016, 2056)]

vSSPs=['SSP2']#,'SSP5']
vYears=[x for x in range(2042, 2043)]
iters = 1000



start_time = time.time()
for _ssp in vSSPs:
    for _year in vYears:
        sum_pop_list = []
        sum_ED_list = []
        
        for idx in range(iters):
        
            tmp_path = tmp_folder_path+'\\'+'mod21_'+str(_year)+'_'+_ssp+'.csv'
            f_temp = pd.read_csv(tmp_path)

            model1 = f_temp.columns[3]
            model = list(f_temp.columns[5:])
            model.append(model1)

            pop_path = pop_folder_path+'\\'+'T2_'+str(_ssp)+'_'+str(_year)+'.csv'
            f_POP = pd.read_csv(pop_path)

            strPOP_FUT=fpop_folder_path+'\\'+'F_POP_'+str(_ssp)+'_'+str(_year)+'.csv'
            f_POP_future=pd.read_csv(strPOP_FUT,encoding='ANSI')

            strGDP_FUT=fGDP_folder_path+'\\'+'F_GDP_'+str(_ssp)+'_'+str(_year)+'.csv'
            f_GDP_future=pd.read_csv(strGDP_FUT,encoding='ANSI')
            
            _T = 'mean'
            d = random.uniform(0.1,0.4)
            e = random.uniform(0.1, 0.37)
            f = random.uniform(0.08, 0.18)
            g = random.uniform(0.05, 0.17)
            print(d)
            result = pd.DataFrame()
            result = pd.merge(f_temp, f_POP, on = 'ID_new')
            result=pd.merge(result, f_GDP_Per, on = '市')

            result['defT_new1'] = (0.567 * np.log10(result['Area'])-0.02718)*0.91

            
            result['daily_intensity'] =  result[_T] + result['defT_new1'] - result['MMT']-(d+e)-(f+g) * result['建筑比例'] #- result['def_MMT']
            df = pd.DataFrame(result[['ID_new','daily_intensity']])
            df = df[(df.daily_intensity)>0]
            grouped = df.groupby('ID_new').mean()
            result = pd.DataFrame()
            result = pd.merge(f_POP, grouped, how = 'left', on = 'ID_new')
            result['daily_intensity'] = result['daily_intensity'].fillna(0) #空值赋值为0

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

            df = pd.DataFrame(f_GDP_Per[['市', '建筑比例']])
            result = pd.merge(result, df, how = 'left', on = '市')

            f_RRchange = pd.DataFrame(result[['ID_5buffer', 'RR_change', '建筑比例']])

            result = pd.DataFrame()
            table1 = pd.merge(f_POP, f_temp, on = 'ID_new')
            result = pd.merge(table1, f_RRchange, on = 'ID_5buffer')
            result['defT_new1'] = (0.567 * np.log10(result['Area'])-0.02718)*0.91 # 计算热岛强度的升温

            coef_list = ['coef_1','coef_2','coef_3','coef_4','coef_5']

            for i in range(len(coef_list)):       

                RR_result = []
                for row in result.itertuples():
                #     print(row.Temp) # 输出每一行
                    T = getattr(row,str(_T))+ getattr(row,coef_list[i]) * row.defT_new1/row.sum_coef_area - row.MMT-(d+e)-(f+g) * row.建筑比例 #- row.def_MMT
                    coef = row.RR_change
                    if row.Yangjun == 'North' and T >= 0:
                        RR_Yangjun = (61.57*np.exp(-0.2699*(T+21.8063)) + 0.2924*np.exp(0.04816*(T+21.8063))- 1) * (1 - coef) + 1
                    elif row.Yangjun == 'Northeast' and T >= 0:
                        RR_Yangjun = (355.4*np.exp(-0.3509*(T+22.0315)) + 0.2439*np.exp(0.05717*(T+22.0315))- 1) * (1 - coef) + 1
                    elif row.Yangjun == 'Northwest' and T >= 0:
                        RR_Yangjun = (1205*np.exp(-0.3977*(T+24.7636)) + 0.493*np.exp(0.02619*(T+24.7636))- 1) * (1 - coef) + 1
                    elif row.Yangjun == 'East' and T >= 0:
                        RR_Yangjun = (267.7*np.exp(-0.2907*(T+24.4582)) + 0.1277*np.exp(0.07429*(T+24.4582))- 1) * (1 - coef) + 1
                    elif row.Yangjun == 'Central' and T >= 0:
                        RR_Yangjun = ((4.515e+05)*np.exp(-0.5707*(T+25)) + 0.1356*np.exp(0.07097*(T+25))- 1) * (1 - coef) + 1
                    elif row.Yangjun == 'South' and T >= 0:
                        RR_Yangjun = (0.1363*np.exp(0.06902*(T+28.8742))- 1) * (1 - coef) + 1
                    elif row.Yangjun == 'Southwest' and T >= 0:
                        RR_Yangjun = ((2.474e+05)*np.exp(-0.9893*(T+15)) + 0.4036*np.exp(0.05515*(T+15))- 1) * (1 - coef) + 1
                    else:
                        RR_Yangjun = 1
                    RR_result.append(RR_Yangjun)
                result['RR_Clim+UHI-MMT_'+str(i+1)] = RR_result
                result['RR_'+str(i+1)] = (result['RR_Clim+UHI-MMT_'+str(i+1)] - 1)/result['RR_Clim+UHI-MMT_'+str(i+1)]

            df = pd.DataFrame(result[['ID_5buffer','RR_1', 'RR_2', 'RR_3', 'RR_4', 'RR_5']])
            grouped = df.groupby('ID_5buffer').sum()

            result_ED = pd.merge(f_POP, grouped, on = 'ID_5buffer')

            ED_list = []
            for row in result_ED.itertuples():
            #     print(row.Temp) # 输出每一行
                if row.gridcode == 1:
                    ED = row.POP_new/1000 * row.MR * row.RR_1
                elif row.gridcode == 2:
                    ED = row.POP_new/1000 * row.MR * row.RR_2
                elif row.gridcode == 3:
                    ED = row.POP_new/1000 * row.MR * row.RR_3
                elif row.gridcode == 4:
                    ED = row.POP_new/1000 * row.MR * row.RR_4
                elif row.gridcode == 5:
                    ED = row.POP_new/1000 * row.MR * row.RR_5
                else:
                    ED = 0
                ED_list.append(ED)
            result_ED['ED'] = ED_list

            sum_pop_list.append(sum(result_ED['POP_new']))
            sum_ED_list.append(sum(result_ED['ED']))
            
        # 创建一个包含两个列表数据的DataFrame
        data_frame = pd.DataFrame({'pop': sum_pop_list, 'ED': sum_ED_list})

        # 将DataFrame导出为CSV文件（假设文件名为'output_file.csv'）
        data_frame.to_csv(out_path+'\\'+str(_ssp)+'_'+str(_year)+'.csv', index=False)
            
        
end_time = time.time()
elapsed_time = round(end_time - start_time)
formatted_time = seconds_to_hh_mm_ss(elapsed_time)
print(f"运行时间：{formatted_time}")              


# In[ ]:




