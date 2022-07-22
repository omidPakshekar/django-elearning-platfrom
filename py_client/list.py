from email import header
import requests
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/course/"
# password = getpass()
data = {
    "title" : "create with api",
    "slug" : "apislug",
    "overview" : "it's simple api",
    "owner" : 1,
    "category" : 1,
    "students" : [1,2],
}
auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())
