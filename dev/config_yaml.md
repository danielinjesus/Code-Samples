﻿설정변수들을 yaml파일에 따로 모아두려면 라이브러리가 필요하니?
ChatGPT의 말:
네, PyYAML 라이브러리가 필요해.

bash
복사
편집
pip install pyyaml
🔹 YAML 파일 예시 (config.yaml)
yaml
복사
편집
api_keys:
  openai: "sk-xxxxxxxxxxxxxxxxxxxx"
  upstage: "sk-yyyyyyyyyyyyyyyyyy"
database:
  host: "localhost"
  port: 5432
  user: "admin"
  password: "password123"
🔹 Python에서 불러오기
python
복사
편집
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

print(config["api_keys"]["openai"])  # OpenAI API 키 출력
print(config["database"]["host"])    # DB 호스트 출력
✅ yaml.safe_load() 사용 → 보안상 더 안전
✔️ 환경변수를 .env에 두는 것처럼 설정을 YAML로 관리 가능! 🚀

==========================

대안 1: yaml만
yaml
복사
편집
# config.yaml
data_dir: "./data"
log_dir: "./logs"
python
복사
편집
import yaml

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

print(cfg["data_dir"])

============
패키지 호출하기
from ocr.metrics ...처럼 하려면 baseline_code의 상위 폴더가 PYTHONPATH에 있어야 함.