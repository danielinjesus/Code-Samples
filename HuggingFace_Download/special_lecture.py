from transformers import pipeline
generator = pipeline('text-generation', model='skt/ko-gpt-trinity-1.2B-v0.5')