import requests

url = "http://localhost:8000/echo/"
payload = {
    "name": "<script>alert('XSS')</script>",
    "age": 30,
    "secret_name": "Clark Kent"
}

response = requests.post(url, json=payload)
print("Status code:", response.status_code)
print("Response JSON:", response.json())
