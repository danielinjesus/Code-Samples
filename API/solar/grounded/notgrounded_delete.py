# %% 2버전 data csv 불러오기
import pandas as pd
train_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/groundness/solar-mini-chk.csv")
print(train_df.columns)
print(train_df.shape) # (12441, 4) (기본 12457-16개 중복행 삭제)

# %% solar-groundness check으로 선별된 197개 불러오기
notGrounded_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/groundness/notGround.csv")
print(notGrounded_df.columns)
notGrounded_list = notGrounded_df['summary'].tolist()
print(notGrounded_list)
print(len(notGrounded_list))

# %% data2버전 중 solar-groundness check에서 notGrounded로 분류된 197개 행제거
drop_notGrounded = train_df[~train_df['summary'].isin(notGrounded_list)]
print(drop_notGrounded) # (12441-197 = 12244 , 4) 
drop_notGrounded.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v3.csv", index=False, encoding="UTF-8-sig")

# %% 'Unnamed: 0.1' 칼럼 지우기
import pandas as pd
train_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v2.csv")
train_df = train_df.drop(columns="Unnamed: 0")
train_df.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v2.csv", index=False, encoding="utf-8-sig")
# %%
