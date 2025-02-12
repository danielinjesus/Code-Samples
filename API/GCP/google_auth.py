# echo 'export GOOGLE_APPLICATION_CREDENTIALS="/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/Daun/upstageailab5-llm-pjt-8a83e65dcb7a.json"' >> ~/.bashrc
# source ~/.bashrc
from google.auth import default

credentials, project = default()
print(f"Authenticated with project: {project}")
