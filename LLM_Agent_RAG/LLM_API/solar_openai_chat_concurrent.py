from openai import OpenAI;from dotenv import load_dotenv;import os, concurrent.futures,time;
load_dotenv();st=time.time() 
upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
openai = OpenAI(api_key=os.getenv("openai"), base_url="https://api.openai.com/v1")
def solar():
    solar_answer = upstage.chat.completions.create(model="solar-pro",messages=[
        {"role": "system", "content": "Respond like a casual friend."},
        {"role": "user", "content": "What is quantum mechanics?"}
    ]); return "solar", solar_answer.choices[0].message.content, round(time.perf_counter()-st,2)
def gpt4():
    gpt4_answer = openai.chat.completions.create(model="gpt-4",messages=[
        {"role": "system", "content": "Respond like a casual friend."},
        {"role": "user", "content": "What is quantum mechanics?"}
    ]); return "openai", gpt4_answer.choices[0].message.content, round(time.perf_counter()-st,2)
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures={executor.submit(solar):"solar", executor.submit(gpt4):"openai"}
    for future in concurrent.futures.as_completed(futures):
        service, answer, perf=future.result()
        print(f"{service}답변{perf}초초: {answer}")