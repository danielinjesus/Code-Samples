# pip install --upgrade azure-cognitiveservices-vision-computervision
# subscription, Vision resource,

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array;from PIL import Image;import os,sys,time

from dotenv import load_dotenv;import os;load_dotenv()
subscription_key=os.getenv("azure_vision_key")
endpoint=os.getenv("azure_vision_endpoint")

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
print("===== Read File - remote =====")
# Get an image with text
read_image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"

# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url,  raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print("===== End of Reading File - remote =====")