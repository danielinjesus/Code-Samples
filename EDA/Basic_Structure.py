####################### 환경변수 가져오기 #######################
# pip install python-dotenv
from dotenv import load_dotenv; import os
load_dotenv(); os.getenv("upstage")
# .gitignore기준으로 경로 입력 예) 동일 폴더시 .env
# .env 파일 형식 :
#  - upstage=abd
#  - huggingface=abc
# 참고자료 https://codingdog.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-dotenv-loaddotenv%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%B4%EC%84%9C-%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EB%A5%BC-load%ED%95%B4-%EB%B4%85%EC%8B%9C%EB%8B%A4
# 참고자료 https://www.youtube.com/shorts/LQ1tm5lkaLI

####################### 파일저장 #######################
import os, time
RESULT_PATH = ''
file_name = os.path.splitext(os.path.basename(__file__))[0]
formatted_time = time.time().strftime("%Y_%m_%d_%H_%M")
if not os.path.exists(RESULT_PATH):
	os.makedirs(RESULT_PATH)
"".to_csv(f"{RESULT_PATH}/{file_name}_{formatted_time}.csv", index=False, encoding='utf-8-sig')

####################### 작업시간 측정 #######################
# 순수 프로세스 작업시간만 측정: time.process_time()
import time
start=time.perf_counter()
start_process=time.process_time()
def do_something():
    print('Sleeping 1 second...')
    time. Sleep(3)    
참조) https://mebadong.tistory.com/106

####################### 현재 경로 #######################
현재파일경로 : Path(__file__).resolve()
from pathlib import Path
wandb_dir = Path(__file__).resolve().parent / "wandb_logs"
wandb_dir.mkdir(parents=True, exist_ok=True)

####################### 라이브러리 일괄 설치 #######################
pip list --format=freeze > requirements.txt # 현재 라이브러리를 저장하기
pip install -r requirements.txt # requirements.txt에 있는 라이브러리 설치하기

####################### csv 저장 #######################
if not os.path.exists(RESULT_PATH):
	os.makedirs(RESULT_PATH)
        
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    formatted_time = now.strftime("%Y_%m_%d_%H_%M")
    
    output.to_csv(f"{RESULT_PATH}/{file_name}_{formatted_time}_output_solar.csv", index=False, encoding='utf-8-sig')
    
    train_df[['fname', 'summary']].to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/dev/solar_basic/solar_basic_RAG/result/train_result.csv", index=False, encoding='utf-8-sig')