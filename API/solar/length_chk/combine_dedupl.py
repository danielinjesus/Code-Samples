# 합치기 코드
import pandas as pd; import os
input_folder = "/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/refined_data"
output_csv = "/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/full_data.csv"
merged_df = pd.DataFrame()
for file_name in sorted(os.listdir(input_folder)):
    print(file_name)    
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        temp_df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
merged_df.to_csv(output_csv, index=False, encoding="utf-8-sig")

# 칼럼명 같은지 확인
# import pandas as pd; import os
# a = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/refined_data/개인및관계.csv")
# print(a.columns)
# b = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v3.csv")
# print(b.columns)
 #%% 숫자
import pandas as pd; import os
df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/full_data.csv") # print(len(df)) # len == 173229
# 중복값만 따로 저장
# duplicate_values = df['summary'][df['summary'].duplicated()]
# 중복값 제외하고 저장
# deduple = df[~df['summary'].duplicated] # 22개
new_df = df.drop_duplicates(subset=['summary'], keep='first')
print(len(new_df))
# %%
import pandas as pd; import os
full_data = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_12941_v2.csv") # 12941
train_v3 = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/train_dh_v3.csv") # 12441
print(len(train_v3))
train_v6 = pd.concat([full_data, train_v3])
train_v6.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/train_dh_v6.csv", index=False, encoding="utf-8-sig")
print(len(train_v6)) # 25,186

# %%
import pandas as pd; df=pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/solar-mini-chk/solar-mini-chk.csv",encoding="utf-8-sig", header=None); print(len(df));
print(df.columns)
deduple = df[~df[0].duplicated()]; print(len(deduple))
deduple.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/solar-mini-chk/solar-mini-chk-300.csv", index=False, encoding="utf-8-sig")
# %%
