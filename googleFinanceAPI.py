# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 10:18:11 2017

@author: tanmay
"""

import numpy as np
from pandas_datareader import data as dr
import matplotlib.pyplot as plt
import pandas as pd
import datetime

end =datetime.datetime.now()
start =end- datetime.timedelta(days=365)

data= dr.DataReader("BAC",'yahoo',start,end)

"""DataReader('TSLA','yahoo',start, end)"""

print(data.head())

data['pr_chg'] = data['Close'].shift(1)-data['Close'].shift(6)

print(data['pr_chg'])



data['std_100day'] = pd.rolling_std(data['pr_chg'],window=100)



data['5d_avg_vol'] = pd.rolling_mean(data['Volume'].shift(1),window=5)

data['5d_avg_vol'] = pd.rolling_mean(data['Volume'].shift(1),window=5)

data['past 5d_avg_vol'] = data['5d_avg_vol'].shift(5)

data['signal']=0

data.loc[((data['pr_chg'].abs() > data['std_100day']) & (data['5d_avg_vol']<data['past 5d_avg_vol']) 
               & (data['pr_chg']<0)),'signal' ]=1


data.loc[((data['pr_chg'].abs() > data['std_100day']) \
     & (data['5d_avg_vol']<data['past 5d_avg_vol']) \
        & (data['pr_chg']>0)),'signal' ]=-1


data['c_signal']=0 
data['exit']=0

for i in range(len(data)):
    if((data.iloc[i]['signal']!=0) &(data.iloc[i]['signal']!= data.iloc[i-1]['c_signal'])) :
        data.iloc[i,data.columns.get_loc('c_signal')]=data.iloc[i,data.columns.get_loc('signal')]
        if data['signal'][i] ==1:
            data.iloc[i,data.columns.get_loc('exit')]=1
        else:
            data.iloc[i,data.columns.get_loc('exit')]=-1
    if((data['signal'][i]!=0) & (data['signal'][i]== data['c_signal'][i-1])) :
        data.iloc[i,data.columns.get_loc('c_signal')]=data['c_signal'][i-1]
        if data['c_signal'][i-1]==1:
               data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])+1
        else:
            data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])-1
    if((data['signal'][i]==0)&(data['exit'][i-1]<5)&(data['exit'][i-1]>0)):    
        data.iloc[i,data.columns.get_loc('c_signal')]=data['c_signal'][i-1]
        data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])+1
    if((data['signal'][i]==0)&(data['exit'][i-1]>-5)&(data['exit'][i-1]<0)):    
        data.iloc[i,data.columns.get_loc('c_signal')]=data['c_signal'][i-1]
        data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])-1
    if((data['signal'][i]==0)&((data['exit'][i-1]==5)|(data['exit'][i-1]==-5))):    
        data.iloc[i,data.columns.get_loc('c_signal')]=0
        data.iloc[i,data.columns.get_loc('exit')]=0
        
        
        
print(data.tail())


data['return'] = np.log(data['Close']/data['Close'].shift(1))

data['str_return']=data['return']*data['c_signal']

data['cu_str_return']=0
data['cu_mar_return']=0

data.iloc[100:,data.columns.get_loc('cu_str_return')]=pd.expanding_sum(data['str_return'][100:])

data.iloc[100:,data.columns.get_loc('cu_mar_return')]=pd.expanding_sum(data['return'][100:])

data[['cu_mar_return','cu_str_return','c_signal']].tail()

plt.figure(figsize=(10,7))
plt.plot(data['cu_str_return'][100:], color='g',label='Strategy Returns')
plt.plot(data['cu_mar_return'][100:], color='r',label='Market Returns')
plt.legend(loc='best')
plt.show()