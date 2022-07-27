from email import header
import requests
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

password = getpass()
email = input('your email?')
data ={
    "email" : email,
    "password" : password
}
auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())