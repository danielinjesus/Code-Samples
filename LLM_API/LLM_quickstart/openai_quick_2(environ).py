import openai;from dotenv import load_dotenv;import os;load_dotenv();openai.api_key=os.getenv("OPENAI_API_KEY")
gpt4_answer=openai.chat.completions.create(model="gpt-4",messages=[
    {"role": "system", "content": "Respond like a casual friend."},
    {"role": "user", "content": "What is quantum mechanics?"}
]);print(f"openai 답변: {gpt4_answer.choices[0].message.content}")