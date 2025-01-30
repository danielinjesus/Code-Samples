openai.py
# https://pypi.org/project/ratelimit/ 이런 것도 있음.
import openai
start_time=None
def chk(idx, dialogue, summary):
  while True:
    try:
      client.chat.completions.create(model="solar-1-mini-chat",
      messages=build_prompt(dialogue, summary), temperature=0.2, top_p=0.3)
      
      idx=row.Index; fname=row.fname; dialogue=row.dialogue; summary=row.summary
      write_row = [fname, dialogue, summary]
      with open("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/groundness/solar-mini-chk.csv", mode='a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file).writerow([fname, dialogue, summary])         
            global start_time
            if idx == 0:
                start_time=time.time()
            if (idx + 1) % 100 == 0:   # Rate limit 방지를 위해 1분 동안 최대 100개의 요청을 보내도록 합니다.
                end_time = time.time()
                elapsed_time = end_time-start_time            
                if elapsed_time < 60:
                    wait_time = 60 - elapsed_time + 5
                    print(f"Elapsed time: {elapsed_time:.2f} sec")
                    print(f"Waiting for {wait_time} sec")
                    time.sleep(wait_time)  
                start_time=time.time()          
        except openai.RateLimitError as e:
            print(f"too many requests : {e}")
            time.sleep(60)
        except Exception as e:
            print(f"effor : {e}")
            return None        
  return summary.choices[0].message.content    