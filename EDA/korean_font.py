import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from datetime import datetime 
from statsmodels.tsa.seasonal import seasonal_decompose

plt.rc('font', family='NanumGothic') 
plt.rcParams['figure.figsize'] = 15,8
plt.figure(figsize=(4,4))