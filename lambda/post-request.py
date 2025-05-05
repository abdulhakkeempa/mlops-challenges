"""
This is file is used to test the AWS Lambda function using a POST request.
This code reads an image file, encodes it in base64, and sends it to the Lambda function via an API Gateway endpoint.
This is to ensure that the deployed Lambda function works as expected.
"""

import base64
import requests

# Read and encode the image
with open("car.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# Your API Gateway endpoint
url = "ENDPOINT_URL"

# Payload format expected by Lambda
payload = {
    "isBase64Encoded": True,
    "body": encoded_string
}

response = requests.post(url, json=payload)
print(response.text)
print(response.status_code)
print(response.json())
