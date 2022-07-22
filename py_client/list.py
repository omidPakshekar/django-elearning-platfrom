from email import header
import requests
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/token/"

# password = getpass()
# email = input('your email?')
# data ={
#     "email" : email,
#     "password" : password
# }
# auth_response = requests.post(auth_endpoint, json=data)
# print('auth_response=', auth_response.json())

endpoint = "http://127.0.0.1:8000/api/course/"
response = requests.post(endpoint)
print('response=', response.json())

# if auth_response.status_code == 200:
#     token = auth_response.json()['token']    
#     headers = {
#         "Authorization" : f"Bearer {token}"
#     }
#     get_response = requests.get( endpoint, headers=headers) # HTTP request
#     data = get_response.json()
    

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
