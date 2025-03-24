# %% summary 기준 중복된 것만 dupl.csv로 저장 (01_dupl.csv로 이름 변경해놓았습니다.)
import pandas as pd
train_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v1.csv")
# print(train_df.value_counts())
# %%
duplicates = train_df[train_df.duplicated(subset=['summary'], keep=False)]
duplicates_sorted = duplicates.sort_values(by=['summary'])
duplicates_sorted_column_order_change = duplicates_sorted[['fname', 'summary', 'topic', 'dialogue']]
duplicates_sorted_column_order_change.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/dupl/dupl.csv")