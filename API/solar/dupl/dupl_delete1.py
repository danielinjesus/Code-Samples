# %%
import pandas as pd
# 중복제거
train_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v1.csv")
print(train_df.shape) # print(12457,4)
# %%
dropped_train_df = train_df.drop(index=[8785, 3654, 7551, 5673, 11608, 6189, 830, 2496, 7528, 7529, 10095, 10360, 7557, 6659, 2059, 11627])
print(len(dropped_train_df[dropped_train_df.duplicated(subset=['summary'], keep=False)]))
print(dropped_train_df.shape) # (12441, 4) 16개 행 삭제
dropped_train_df.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v2.csv")
# %%



# 중복 중 하나 : 8785, 3654, 7551, 5673, 11608, 6189, 830, 2496, 7528, 7529, 10095, 10360, 7557, 6659, 2059, 11627
# (참고) 중복이면서 내용이 완전 다른 거 : 7551, 830, 7528, 7529, 7557
# 이렇게 내용이 완전 다른게 더 있지 않을까?

# 특정 인덱스 삭제
# df_dropped = df.drop  # 인덱스 2, 3 제거