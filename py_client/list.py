from email import header
import requests
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/token/"

password = getpass()
email = input('your email?')
data ={
    "email" : email,
    "password" : password
}
auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://127.0.0.1:8000/api/course/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "title" : "create with api2",
        "slug" : "apislug2",
        "overview" : "it's simple api2222222222222",
        "owner" : 2,
        "category" : 2,
        "students" : [3],
    }
    get_response = requests.post( endpoint, headers=headers, json=data) # HTTP request
    data = get_response.json()
    print('data=', data)

# auth_endpoint = "http://127.0.0.1:8000/api/course/"
# # password = getpass()
# data = {
#     "title" : "create with api",
#     "slug" : "apislug",
#     "overview" : "it's simple api",
#     "owner" : 1,
#     "category" : 1,
#     "students" : [1,2],
# }
# auth_response = requests.post(auth_endpoint, json=data)
# print('auth_response=', auth_response.json())
