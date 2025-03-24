# pip install openai
 
from openai import OpenAI # openai==1.52.2
 
client = OpenAI(
    api_key="up_CV6neInxUsa4VWdauqE6P5nQTYEgv",
    base_url="https://api.upstage.ai/v1/solar"
)
 
stream = client.chat.completions.create(
    model="solar-pro",
    messages=[
        {
            "role": "user",
            "content": "Who create the universe?"
        }
    ],
    stream=True,
)
 
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
 
# Use with stream=False
# print(stream.choices[0].message.content)