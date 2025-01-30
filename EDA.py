import pandas as pd
####################### 테이블 기본 정보 #######################
df=pd.read_csv("")
print(f"shape : {df.shape}") # 행,열 갯수보기
print(f"columns : {df.columns}") # 열 목록
print(f"describe() : {pd.describe(df)}") # 평균, 중위값, 표준편차, 25%, 50%, 75%
print(f"head() : {df.head()}")
####################### null 갯수 확인 #######################
df_null=df.isnull().sum()
df_not_null=df.notnull().sum()
df_cnt=df_null+df_not_null
df_table=pd.DataFrame({
    'null_count': df_null,
    'notnull_count': df_not_null,
    'full_number' : df_cnt })
print(df_table)
####################### 중복행 찾기 #######################
print(f"모든 중복 행 수 : {len(df[df.duplicated()])}") # 중복행 keep='first'기본값. 두번째 값만 True로 반환.
print(f"모든 중복 행 수 두번째만: {df.duplicated(subset=df.columns,keep=False).sum()}") # 첫번째 행은 두고, 두번째 행만 센다. 모든 열을 기준으로 하나라도 중복된 행 개수를 반환
print(f"열별 두번째 이상 중복 수 : {df.apply(lambda col: col.duplicated().sum())}") # 각 열별 중복 개수
print(f"중복 아닌 행 갯수 : {len(df[~df.duplicated()])}") 