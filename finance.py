import numpy as np
from pandas_datareader import data as dr
import matplotlib.pyplot as plt
import pandas as pd
import datetime

end =datetime.datetime.now()
start =end- datetime.timedelta(days=365)

data= dr.DataReader('TSLA','yahoo',start, end)

print(data.head())