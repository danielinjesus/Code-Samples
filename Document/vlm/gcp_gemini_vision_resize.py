#pip install --upgrade google-cloud-aiplatform
import vertexai;from vertexai.generative_models import GenerativeModel,Part;import base64
import os;os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\credentials\gcp-test-451422-207d89327858.json"

from PIL import Image;import io

def resize_image(image_bytes, max_size=(512, 512)):
    """Resizes an image to a maximum size."""
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail(max_size)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    return img_byte_arr.getvalue()

#inside of your code where you load the image.
image_bytes = open(r"C:\code-samples\Document\img\책표지_총류_000002.jpg", "rb").read() #if using a local file.
resized_image_bytes = resize_image(image_bytes)
image_file=Part.from_data(resized_image_bytes, "image/jpeg")

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