# %%
import pandas as pd; import time, os; from tqdm import tqdm; from openai import OpenAI;from dotenv import load_dotenv; import openai; import csv
train_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v3.csv")
load_dotenv(); client = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
file_name = (os.path.basename(__file__))
def build_prompt(dialogue):
    system_prompt = """
    [역할] : 너는 한국어 대화문을 영어로 번역하는 전문가야. [지시사항]과 [주의사항]을 참고하여 업무수행해.
    [지시사항] : [대화] 다음 줄부터 나오는 대화문을 영어로 번역해.\n
    [주의사항] : #으로 표시된 단어들은 변경하지 마.
    """.strip()
    few_shot_user_prompt_1 = """\n\n 
    [대화] :\n
    #Person1#: 안녕하세요, 오늘 하루 어떠셨어요?\n 
    #Person2#: 요즘 숨쉬기가 좀 힘들어요.\n
    #Person1#: 최근에 감기 같은 것에 걸리신 적이 있나요?\n
    #Person2#: 아니요, 감기는 아니에요. 그냥 숨을 쉴 때마다 가슴이 무겁게 느껴져요.\n
    #Person1#: 알고 있는 알레르기가 있나요?\n
    #Person2#: 아니요, 알고 있는 알레르기는 없어요.\n
    #Person1#: 이런 증상이 항상 나타나나요, 아니면 활동할 때 주로 나타나나요?\n
    #Person2#: 운동을 할 때 많이 나타나요.\n
    #Person1#: 저는 당신을 폐 전문의에게 보내서 천식에 대한 검사를 받게 할 거예요.\n
    #Person2#: 도와주셔서 감사합니다, 의사 선생님.
    """.strip()
    few_shot_assistant_prompt_1 = """
    #Person1#: Hello, how was your day?\n
    #Person2#: I'm having a hard time breathing these days.\n
    #Person1#: Have you caught a cold recently?\n
    #Person2#: No, I don't have a cold. I just feel heavy in my chest every time I breathe. \n
    #Person1#: Do you know any allergies?\n
    #Person2#: No, I don't know any allergies.\n
    #Person1#: Do you have these symptoms all the time, or do you usually have them during activities?\n
    #Person2#: It appears a lot when I exercise.\n
    #Person1#: I'll send you to a pulmonologist for a test for asthma.\n
    #Person2#: Thank you for your help, doctor.\n
    """.strip()
    user_prompt = f"""
    [대화] :\n
    {dialogue}
    """.strip()
    # print("dialogue 완성")
    return_txt = [ {"role": "system", "content": system_prompt},
            {"role": "user", "content": few_shot_user_prompt_1},
            {"role": "assistant", "content": few_shot_assistant_prompt_1},
            {"role": "user", "content": user_prompt} ]
    print(return_txt)
    return return_txt
start_time=None
def chk(idx, dialogue):
    while True:
        try:
            print(f"Processing index before: {idx}")
            summary = client.chat.completions.create(model="solar-1-mini-chat", messages=build_prompt(dialogue), temperature=0.2, top_p=0.3, timeout=10)
            print(f"Processing index after: {idx}")
            global start_time
            if idx == 0:
                start_time=time.time()
                print(start_time)
            if (idx + 1) % 100 == 0:   # Rate limit 방지를 위해 1분 동안 최대 100개의 요청을 보내도록 합니다.
                end_time = time.time()
                elapsed_time = end_time-start_time            
                if elapsed_time < 60:
                    wait_time = 60 - elapsed_time + 5
                    print(f"Elapsed time: {elapsed_time:.2f} sec")
                    print(f"Waiting for {wait_time} sec")
                    time.sleep(wait_time)  
                start_time=time.time()
            print(summary.choices[0].message.content)
            return summary.choices[0].message.content
        except openai.RateLimitError as e:
            print(f"too many requests : {e}")
            time.sleep(60)
        except Exception as e:
            print(f"effor : {e}")
    
if __name__ == "__main__" :     
    dialogue_trans=[]
    for row in tqdm(train_df.itertuples(index=True), total=len(train_df)):
        idx=row.Index; fname=row.fname; dialogue=row.dialogue; # summary=row.summary
        print(idx, dialogue)
        result = chk(idx, dialogue)
        print("결과받기\n", result)
        dialogue_trans.append(result)
    trans = pd.DataFrame({"fname":train_df['fname'], "dialogue":dialogue_trans})
    trans.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/translate/solar-mini-dial-trans.csv",index=False, encoding="utf-8-sig")
        # with open("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/translate/solar-mini-trans.csv", mode='a', newline='', encoding='utf-8-sig') as file:
        #     writer = csv.writer(file).writerow([fname, result])
# %%