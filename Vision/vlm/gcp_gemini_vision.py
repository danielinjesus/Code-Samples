#pip install --upgrade google-cloud-aiplatform
# https://ai.google.dev/gemini-api/docs/models?hl=ko#gemini-2.0-flash
# I am unable to locate any text within the provided image. My analysis only detects graphical elements and I am unable to extract textual information.
# 한글, text 내용 이해 못함
import vertexai;from vertexai.generative_models import GenerativeModel,Part;import base64
import os;os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\credentials\gcp-test-451422-207d89327858.json"

# For base64-encoded images
image_path=r"C:\code-samples\Document\img\python_vis_code.png"
with open(image_path, "rb") as image_file:
    image_file = base64.b64encode(image_file.read()).decode("utf-8")

vertexai.init(project="gcp-test-451422", location="us-central1")
model=GenerativeModel("gemini-2.0-pro-exp-02-05")

# Query the model
response = model.generate_content([image_file, "can you give me coordinates of texts in the image?"])
print(response.text)
# Example response:
# That's a lovely overhead flatlay photograph of blueberry scones.
# The image features:
# * **Several blueberry scones:** These are the main focus,
# arranged on parchment paper with some blueberry juice stains.
# ...