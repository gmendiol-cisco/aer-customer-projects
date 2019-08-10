import netmiko
import requests
import json

# define device connection information (OLD use dictionary)
# connection = netmiko.ConnectHandler(ip="192.168.19.130", device_type="cisco_ios", username="administrator", password="FOaaS")

# define device dictionary for netmiko
cisco = {
    'device_type': 'cisco_ios',
    'ip': '192.168.19.130',
    'username': 'administrator',
    'password': 'FOaaS',
}

# define device variables for API call
IPADDRESS = '192.168.19.130'
APIPORT = '55443'
TOKEN = 'b3ioBzxarPKADuaSWIZ2BUbObPEzn7j3rWdxNa3uV6c='

# API call to get token
url = 'https://' + IPADDRESS + ':' + APIPORT + '/api/v1/auth/token-services'
print(url)

payload = ""
headers = {
    'Accept': "application/json",
    'Authorization': "Basic YWRtaW5pc3RyYXRvcjpGT2FhUw==",
    'cache-control': "no-cache",
    'Postman-Token': "260dec64-a995-4b69-ba94-a694dcff0e5a"
    }

response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)
data = json.loads(response.text)

# API call to show logging statements
url = 'https://' + IPADDRESS + ':' + APIPORT + '/api/v1/global/logging'

payload = ""
headers = {
    'Accept': "application/json",
    'X-auth-token': TOKEN,
    'Authorization': "Basic YWRtaW5pc3RyYXRvcjpGT2FhUw==",
    'cache-control': "no-cache",
    'Postman-Token': "8fa63062-536b-4ba7-a3b3-c879cb5723d3"
    }

response = requests.request("GET", url, data=payload, headers=headers, verify=False) 

print(response.text)

# opens file named logging.txt (file can be used to host a set of commands to push to device)
with open('logging.txt') as f:
    lines = f.read().splitlines()
print(lines)

# start ssh session 
connection = netmiko.ConnectHandler(**cisco) 

# send configuration commands from .txt file 
output = connection.send_config_set(lines) 
print(output) 

# disconnect ssh session 
connection.disconnect()

# API call to show logging statement after netmiko configuration push
url = 'https://' + IPADDRESS + ':' + APIPORT + '/api/v1/global/logging'

payload = ""
headers = {
    'Accept': "application/json",
    'X-auth-token': TOKEN,
    'Authorization': "Basic YWRtaW5pc3RyYXRvcjpGT2FhUw==",
    'cache-control': "no-cache",
    'Postman-Token': "8fa63062-536b-4ba7-a3b3-c879cb5723d3"
    }

response = requests.request("GET", url, data=payload, headers=headers, verify=False) 

print(response.text)
