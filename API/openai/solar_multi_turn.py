# pip install openai
 
from openai import OpenAI # openai==1.52.2
 
client = OpenAI(
    api_key="up_CV6neInxUsa4VWdauqE6P5nQTYEgv",
    base_url="https://api.upstage.ai/v1/solar"
)
 
def chat_with_solar(messages):
    response = client.chat.completions.create(
        model="solar-pro",
        messages=messages
    )
    return response.choices[0].message['content']
 
# Initial conversation setup
messages = [
    {"role": "user", "content": "Hello, who won the world series in 2020?"}
]
 
# First turn
response = chat_with_solar(messages)
print("Assistant:", response)
messages.append({"role": "assistant", "content": response})
 
# Second turn
messages.append({"role": "user", "content": "Where was it played?"})
response = chat_with_solar(messages)
print("Assistant:", response)
messages.append({"role": "assistant", "content": response})
 
# Third turn
messages.append({"role": "user", "content": "Who was the MVP?"})
response = chat_with_solar(messages)
print("Assistant:", response)
messages.append({"role": "assistant", "content": response})