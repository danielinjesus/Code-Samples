####################### 파일저장 #######################
import os, time
RESULT_PATH = ''
file_name = os.path.splitext(os.path.basename(__file__))[0]
formatted_time = time.time().strftime("%Y_%m_%d_%H_%M")
if not os.path.exists(RESULT_PATH):
	os.makedirs(RESULT_PATH)
"".to_csv(f"{RESULT_PATH}/{file_name}_{formatted_time}.csv", index=False, encoding='utf-8-sig')
