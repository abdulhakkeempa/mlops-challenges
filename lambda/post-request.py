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
