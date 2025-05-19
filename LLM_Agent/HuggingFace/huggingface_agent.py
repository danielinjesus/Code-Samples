from dotenv import load_dotenv;load_dotenv();
import os
from huggingface_hub import InferenceClient
token=os.getenv("HF_TOKEN")

client = InferenceClient("meta-llama/Llama-3.2-3B-Instruct")
# if the outputs for next cells are wrong, the free model may be overloaded. You can also use this public endpoint that contains Llama-3.2-3B-Instruct
# client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")

output = client.text_generation(
    "The capital of france is",
    max_new_tokens=100,
)

print(output)