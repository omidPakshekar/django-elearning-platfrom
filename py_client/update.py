from email import header
import requests
from getpass import getpass
import json

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

password = ""
email = ""
data ={
    "email" : email,
    "password" : password
}
auth_response = requests.post(auth_endpoint, json=data)

endpoint = "http://127.0.0.1:8000/api/v1/course/1/"


if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    
    payload = json.dumps({
        "id": 1,
        "modules_url": [
        "http://localhost:8000/api/v1/module/2/",
        "http://localhost:8000/api/v1/module/12/"
        ],
        "modules": [
            {
                "id": 2
            }
        ],
        "title": "it's postmanq3",
        "slug": "posta2",
        "overview": "it's overview3\nq",
        "created": "2022-07-25T10:11:03.786132Z",
        "owner": 1,
        "category": 1,
        "students": []
    })
    # print('get=', requests.get( endpoint, headers=headers).json())
    print('*'*10)
    get_response = requests.request("PUT", endpoint, headers=headers, data=payload) # HTTP request
    print(get_response.text)
    url = "http://localhost:8000/api/v1/course/1/"

    payload = json.dumps({
    "id": 1,
    "modules_url": [
        "http://localhost:8000/api/v1/module/2/",
        "http://localhost:8000/api/v1/module/12/"
    ],
    "modules": [
        {
        "id": 2
        }
    ],
    "title": "it's postmanq3",
    "slug": "posta2",
    "overview": "it's overview3\nq",
    "created": "2022-07-25T10:11:03.786132Z",
    "owner": 1,
    "category": 1,
    "students": []
    })
    headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NTM3MTk0LCJpYXQiOjE2NTk1MzY4OTQsImp0aSI6IjI2OTUzZTczY2UwYjQ1YjY4NDUzZWY5NDIyMWE0ODA5IiwidXNlcl9pZCI6MX0.n8Ge7ephHqb-ikuwKL_S10Qqrt7cO80g5OiYTILzhG0',
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)