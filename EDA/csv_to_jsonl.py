import pandas as pd; import json

# CSV 파일 읽기
file_path = '/data/ephemeral/home/upstageailab-ir-competition-ir_s3/person/DU/output/02-2-5_solar_o1.csv'
df = pd.read_csv(file_path)

# JSON 파일로 저장 (JSON Lines 형식)
json_file_path = '/data/ephemeral/home/upstageailab-ir-competition-ir_s3/person/DU/output/02-2-5_solar_o1.jsonl'
df.to_json(json_file_path, orient='records', lines=True, force_ascii=False)