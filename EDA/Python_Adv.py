print(f"value_counts() : {df['특정열'].value_counts()}")
print(f"시군구 : {len(dt_train['특정열'].unique())}")
print(dt_train['전용면적(㎡)'].mean()) # 평균
concat.isnull().sum()
중복값 제거      
구간별 갯수
고유값별 갯수
missing.sort_values(inplace=True)
list(concat.columns[concat.isnull().sum() <= 1000000])
concat_select['본번'].astype('str') # str 타입으로 바꾸기
concat_select['구'] = concat_select['시군구'].map(lambda x : x.split()[1])
concat_select['동'] = concat_select['시군구'].map(lambda x : x.split()[2])
concat_select['계약년'] = concat_select['계약년월'].astype('str').map(lambda x : x[:4])
df_list = df['fname'].unique().tolist() # unique()는 Series에 적용됨
df_address_needed = df_train[df_train['좌표X'].isnull()][['도로명']] # null인 것의 '도로명'칼럼만 떼어서 따로 만들
df_train['full_address'] = dt_train['시군구'] + df_train['도로명'] # str 붙이
drop_notGrounded = train_df[~train_df['summary'].isin(notGrounded_list)]
concat['등기신청일자'] = concat['등기신청일자'].replace(' ', np.nan)
df4_0=df4[df4['summary'].fillna("abc").apply(len)>=15]
print(df[df['fname']=="train_11886"])
concat = pd.concat([x_train, x_test]) #df붙이
train_df = train_df.drop(columns="Unnamed: 0") #열 지우기
# 1) 행 지우기 : summary열에서 notGrounded_list에 없는 것만 drop_notGrounded에 저장
# 3) 중복 행 제거(특정 열 기준) keep=True로 하면 두번째 것만 나옮
duplicates = train_df[train_df.duplicated(subset=['summary'], keep=False)]
dropped_train_df = train_df.drop(index=[8785, 3654, 7551])
# 4) 중복 행 제거(전체열기준)
new_df = df.drop_duplicates(subset=['summary'], keep='first')
df_unique = solar_df.drop_duplicates()

# 5) 기존 df에 칼럼명 추가하기
solar_df.columns=['fname','dialogue', 'summary']

# 9) 문자열 바꾸기
df['dialogue'] = df['dialogue'].str.replace('/n', '\n') # df 안 특정열에 바꾸고 싶은 문자열

summaries = train_df['summary'][:10]
for idx, row in tqdm(df.iterrows(), total=len(test_df)):
df=df[['fname', 'dialogue', 'summary']] # 새 df 만들기

a_sorted = a.sort_values(by=['summary']) # summary기준으로 정렬

===============================================
# %% 아직 처리 안 한 행만 작업하기 위해, df 만들기
import pandas as pd
df=pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_12941_v2.csv")
df1=pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/add_data/final_data/full_data_12941_v2_1.csv")
df0=df[~df['fname'].isin(df1['fname'])]
print(len(df)); print(len(df1)); print(len(df0))
df0.sort_values(by='fname', inplace=True)
##########################################################################
# 지울 df의 unique값을 리스트로 추출
notGrounded_df = pd.read_csv("")
print(notGrounded_df.columns)
notGrounded_list = notGrounded_df['summary'].tolist()

# %% data2버전 중 solar-groundness check에서 notGrounded로 분류된 197개 행제거
drop_notGrounded = train_df[~train_df['summary'].isin(notGrounded_list)]

# 열지우기
train_df = train_df.drop(columns="Unnamed: 0")


# 파일 읽기
test_df = pd.read_csv(os.path.join(DATA_PATH, 'test.csv'))