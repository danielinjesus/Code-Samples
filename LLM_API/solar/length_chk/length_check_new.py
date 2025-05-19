#%% 외부데이터 기본분포도 확인
import pandas as pd; from datetime import datetime 
df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_173229.csv")
df['dialogue_len'] = df['dialogue'].apply(lambda x: len(x))
df['summary_len'] = df['summary'].apply(lambda x: len(x))
df['summary/dial'] = df['summary_len'] / df['dialogue_len']
print(df['summary/dial'].describe())
# 훈련셋 dial 438, sum 87, 비율 20~21
# 263, 43, 17

import matplotlib.pyplot as plt; import seaborn as sns
sns.histplot(df["summary/dial"], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Summary/Dialogue ratio'); plt.xlabel('Value'); plt.ylabel('Frequency'); plt.show()
print(df['dialogue_len'].describe())
import matplotlib.pyplot as plt; import seaborn as sns
sns.histplot(df["dialogue_len"], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Dialogue Length'); plt.xlabel('Value'); plt.ylabel('Frequency'); plt.show()
print(df['summary_len'].describe())
import matplotlib.pyplot as plt; import seaborn as sns
sns.histplot(df["summary_len"], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Summary Length'); plt.xlabel('Value'); plt.ylabel('Frequency'); plt.show()
print(datetime.now())
#%% 2차_최종본
import pandas as pd; from datetime import datetime 
df = pd.read_csv("/data/ephemeral/home/baseline/data/full_data_173229.csv")
#훈련셋 대화438, 요약87, 비율20~21
print(a:=len(df)) #
df['dialogue_len'] = df['dialogue'].apply(lambda x: len(x))
df['summary_len'] = df['summary'].apply(lambda x: len(x))
df['summary/dial'] = df['summary_len']/df['dialogue_len']
df = df[(df['summary/dial']>=0.21)]
df = df[(df['summary_len']>80) & (df['summary_len']<300)]
df = df[(df['dialogue_len']<800)]
print(b:=len(df)) #
print(a-b)
df.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_12941_v3.csv")
#%% 1차_최종본
import pandas as pd; from datetime import datetime 
df = pd.read_csv("/data/ephemeral/home/baseline/data/full_data_173229.csv")
#훈련셋 대화438, 요약87, 비율20~21
print(a:=len(df)) #
df['dialogue_len'] = df['dialogue'].apply(lambda x: len(x))
df['summary_len'] = df['summary'].apply(lambda x: len(x))
df['summary/dial'] = df['summary_len']/df['dialogue_len']
df = df[(df['summary/dial']>0.13) & (df['summary/dial']<0.21)]
df = df[(df['summary_len']>50) & (df['summary_len']<80)]
df = df[(df['dialogue_len']<800)]
print(b:=len(df)) #
print(a-b)
df.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_12941_v2.csv")
# import matplotlib.pyplot as plt; import seaborn as sns
# sns.histplot(df['dialogue_len'], kde=True, bins=30, alpha=0.6, color='blue')
# plt.title('Daun - ratio'); plt.xlabel('Value'); plt.ylabel('Frequency'); plt.show()
# import matplotlib.pyplot as plt; import seaborn as sns
# sns.histplot(df['summary_len'], kde=True, bins=30, alpha=0.6, color='blue')
# plt.title('Daun - ratio'); plt.xlabel('Value'); plt.ylabel('Frequency'); plt.show()
# import matplotlib.pyplot as plt; import seaborn as sns
# sns.histplot(df['summary/dial'], kde=True, bins=30, alpha=0.6, color='blue')
# plt.title('Daun - ratio'); plt.xlabel('Value'); plt.ylabel('Frequency'); plt.show()
# print(df['dialogue_len'].describe())
# print(df['summary_len'].describe())
# print(df['summary/dial'].describe())
#%% 특정 문자열 바꾸기기
# df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_173229.csv")
# print(len(df)) #
# df['dialogue'] = df['dialogue'].str.replace('/n', '\n')
# df.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/미용과건강.csv")

import pandas as pd; from datetime import datetime 
# df = pd.read_csv("/data/ephemeral/home/baseline/data/dev.csv")
# df_infer = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/result/02_solar_length21_output_solar.csv")
# %% 추론 버전 비율확인
df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/미용과건강.csv")
df_infer = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/googletrans-translate/01_2025_01_24_17_42.csv")
df['summary'] = df_infer['summary']

# valid
# df = pd.read_csv("/data/ephemeral/home/baseline/data/dev.csv")
# print(df.head())

df['dialogue_len'] = df['dialogue'].apply(lambda x: len(x))
df['summary_len'] = df['summary'].apply(lambda x: len(x))
df['summary / dial'] = df['summary_len'] / df['dialogue_len']
# df.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/dev/dev_len.csv")
# print(df.head())
print(df["summary / dial"].describe())
import matplotlib.pyplot as plt
import seaborn as sns
sns.histplot(df["summary / dial"], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Daun - ratio')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
print(datetime.now())
# %% 추론 길이 확인
import pandas as pd
df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/v7.csv")
# df['summary'] = df_infer['summary']
# df['dialogue_len'] = df['dialogue'].apply(lambda x: len(x))
df['summary_len'] = df['summary'].apply(lambda x: len(x))
# print(df['dialogue_len'].describe())
print(df['summary_len'].describe())
import matplotlib.pyplot as plt; import seaborn as sns
sns.histplot(df['summary_len'], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Daun - length')
plt.xlabel('length')
plt.ylabel('Frequency')
plt.show()
print(datetime.now())
#%% 요약길이 분포 : summary distribution
import pandas as pd; from datetime import datetime 
df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/미용과건강.csv")

df['dialogue_len'] = df['dialogue'].apply(lambda x: len(x))
df['summary_len'] = df['summary'].apply(lambda x: len(x))

print(df['dialogue_len'].describe())
print(df['summary_len'].describe())

import matplotlib.pyplot as plt; import seaborn as sns
sns.histplot(df['dialogue_len'], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Train - Dialogue Length')
plt.xlabel('length')
plt.ylabel('Frequency')
plt.show()

sns.histplot(df['summary_len'], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Train - Summary Length')
plt.xlabel('length')
plt.ylabel('Frequency')
plt.show()
print(datetime.now())

# %% train/dev 셋 csv 분석
import pandas as pd
df_lan = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/dev/leng.csv")
df_interest = df_lan["summary / dial"]
print(df_lan["summary / dial"].info())
print(df_lan["summary / dial"].describe())

import matplotlib.pyplot as plt
import seaborn as sns
sns.histplot(df_interest, kde=True, bins=30, alpha=0.6, color='blue')
plt.title('train_Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# %%
df_interest_4 = df[df["summary / dial"] > 0.4]
print(df_interest_4)
print(len(df_interest_4))
print(df_interest_4)
# %%

# %%
import pandas as pd; import matplotlib.pyplot as plt; import seaborn as sns
test_result = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/dev/leng.csv")
test_result['summary_len'] = test_result['summary'].apply(lambda x: len(x))
sns.histplot(test_result['summary_len'], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Daun - length'); plt.xlabel('length'); plt.ylabel('Frequency'); plt.show()
# %%
import pandas as pd
print(len(pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_12941_v2.csv")))
# %%