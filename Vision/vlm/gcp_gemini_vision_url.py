#pip install --upgrade google-cloud-aiplatform #import base64
import vertexai;from vertexai.generative_models import GenerativeModel,Part
import os;os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\credentials\gcp-test-451422-207d89327858.json"

image_file=Part.from_uri("https://storage.googleapis.com/cloud-samples-data/generative-ai/image/scones.jpg","image/jpeg")
    
vertexai.init(project="gcp-test-451422", location="us-central1")
model=GenerativeModel("gemini-1.5-flash-002")

# Query the model
response = model.generate_content([image_file, "what is this image?"])
print(response.text)
# Example response:
# That's a lovely overhead flatlay photograph of blueberry scones.
# The image features:
# * **Several blueberry scones:** These are the main focus,
# arranged on parchment paper with some blueberry juice stains.
# ...