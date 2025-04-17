import json

file_path = '/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.jsonl'

with open(file_path, 'r') as file:
    documents = [json.loads(line) for line in file]

print(documents)

# # 확인
# for doc in documents[:5]:  # 처음 5개만 출력
#     print(doc)
