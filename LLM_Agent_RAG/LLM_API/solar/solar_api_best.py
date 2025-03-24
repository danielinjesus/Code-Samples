# %%
import pandas as pd; import time, os; from tqdm import tqdm; from openai import OpenAI;from dotenv import load_dotenv
DATA_PATH = "/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data"
RESULT_PATH = "/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/dev/solar_basic/solar_basic_RAG/result"
load_dotenv(); client = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
# %%
train_df = pd.read_csv(os.path.join(DATA_PATH,'train.csv'))
file_name = (os.path.basename(__file__))

# 함수실행순서 3.추론→2.요약생성→1.프롬프트생성

shot_no = 8
# 1. 프롬프트 생성 함수 정의
sample_dialogue1 = train_df.iloc[shot_no]['dialogue']; sample_summary1 = train_df.iloc[shot_no]['summary']
print(f"Sample Dialogue1:\n{sample_dialogue1}\n"); print(f"Sample Summary1: {sample_summary1}\n")
def build_prompt(dialogue):
    system_prompt = "You are a expert in the field of dialogue summarization, summarize the given dialogue in a concise manner. Follow the user's instruction carefully and provide a summary that is relevant to the dialogue."
    few_shot_user_prompt_1 = (
        "Following the instructions below, summarize the given document.\n"
        "Instructions:\n"
        "1. Read the provided sample dialogue and corresponding summary.\n"
        "2. Read the dialogue carefully.\n"
        "3. Following the sample's style of summary, provide a concise summary of the given dialogue. Be sure that the summary is simple but captures the essence of the dialogue.\n\n"

        "Dialogue:\n"
        f"{sample_dialogue1}\n\n" 
        "Summary:\n")
    
    few_shot_assistant_prompt_1 = sample_summary1
    user_prompt = ( 
        "Dialogue:\n"
        f"{dialogue}\n\n"
        "Summary:\n")    
    return [ {"role": "system", "content": system_prompt},
        {"role": "user", "content": few_shot_user_prompt_1},
        {"role": "assistant", "content": few_shot_assistant_prompt_1},
        {"role": "user", "content": user_prompt} ]

# 2. 요약 실행 함수 정의
def summarization(dialogue):
    summary = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=build_prompt(dialogue), # 1. 요약할 dialogue가 포함된 프롬프트를 생성하는 함수를 호출합니다.
        temperature=0.2, top_p=0.3,); return summary.choices[0].message.content

# 3. 추론 함수 정의
def inference():
    test_df = pd.read_csv(os.path.join(DATA_PATH, 'test.csv'))
    summary = []
    start_time = time.time()
    for idx, row in tqdm(test_df.iterrows(), total=len(test_df)):
        dialogue = row['dialogue']
        summary.append(summarization(dialogue))        # 2. 요약 실행 함수를 test.csv row수만큼 호출출
        if (idx + 1) % 100 == 0:   # Rate limit 방지를 위해 1분 동안 최대 100개의 요청을 보내도록 합니다.
            end_time = time.time()
            elapsed_time = end_time-start_time            
            if elapsed_time < 60:
                wait_time = 60 - elapsed_time + 5
                print(f"Elapsed time: {elapsed_time:.2f} sec")
                print(f"Waiting for {wait_time} sec")
                time.sleep(wait_time)
            start_time = time.time()
    output = pd.DataFrame(   {   "fname": test_df['fname'],     "summary" : summary,   }  )
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    formatted_time = time.strftime("%m%d_%H%M", time.localtime())
    output.to_csv(os.path.join(RESULT_PATH, f"{file_name}_{formatted_time}.csv"), index=False, encoding='utf-8-sig')
    return output
if __name__ == "__main__" : output = inference()
# %%