import requests
import json

url = 'http://127.0.0.1:5000/api/order'
data = {
    "customer_name": "Test User",
    "items": [
        {"id": 1, "quantity": 1}
    ]
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
