# pip install --upgrade azure-cognitiveservices-vision-computervision
# subscription, Vision resource,

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time

from dotenv import load_dotenv;import os;load_dotenv()
subscription_key=os.getenv("azure_vision_key")
endpoint=os.getenv("azure_vision_endpoint")

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
print("===== Read File - remote =====")
# Get image path
images_folder=r"C:\code-samples\Document\img"
read_image_path = os.path.join (images_folder,"python_vis_code.png")
# Open the image
read_image = open(read_image_path, "rb")

# Call API with image and raw response (allows you to get the operation location)
read_response = computervision_client.read_in_stream(read_image, raw=True)
# Get the operation location (URL with ID as last appendage)
read_operation_location = read_response.headers["Operation-Location"]
# Take the ID off and use to get results
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for the retrieval of the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status.lower () not in ['notstarted', 'running']:
        break
    print ('Waiting for result...')
    time.sleep(10)

# Print results, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print("===== End of Reading File - remote =====")