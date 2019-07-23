#Dependencies
import requests
import json

# Set up device list and dictionary for later use
ipaddress = []
device = {}
devices = []
user = {}
users = []

# Authorization string.  Note that this is based on a username/password of cisco/cisco.  
# Update as needed
authorization = "Basic Y2lzY286Y2lzY28="

# Import file for reading
f = open('/Users/eleigh/router-ip.txt', 'rt')

#read devices into variable 
for line in f :
    ipaddress.extend (line.split())

# Clean up and close file
f.close()

# Obtain the token for each device.  
# At the end of this loop, expect to have a list (devices) containing a dictionary of each device with IP address and Token
# Note the authorization string is based on cisco/cisco username/password.  Update this string as appropriate
for i in range(len(ipaddress)) :
    url = "https://" + ipaddress[i] + ":55443/api/v1/auth/token-services"

    payload = ""
    headers = {
        'Accept': "application/json",
        'Authorization': authorization,
        'cache-control': "no-cache",
        'Postman-Token': "b35758cc-06e8-4c6a-a2c4-92690b61e2f2"
        }

    response = requests.request("POST", url, data=payload, headers=headers, verify = False)

    # Convert json text to a list
    token = json.loads(response.text)
    
    # Construct the device dictionary
    device = {'IP Address' : ipaddress[i], 'token-id' : token['token-id']}

    # Append the individual device dictionary to the list of devices
    devices.append(device)

# For each device, pull a list of users and then add a new local user

for device in devices :
    #Connect to each device and pull list of users
    url = "https://" + device['IP Address'] + ":55443/api/v1/global/local-users"

    payload = ""
    headers = {
        'X-auth-token': device['token-id'],
        'Authorization': authorization,
        'cache-control': "no-cache",
        'Postman-Token': "7d876d07-f120-4515-8ee7-43d9ac7f2a12"

}

    response = requests.request("GET", url, data=payload, headers=headers, verify = False)

    #Import output into dictionary
    users = json.loads(response.text)

f = open("output.txt", "w")

# Add a new user

for user in users :
    #Add user
    url = "https://" + device['IP Address'] + ":55443/api/v1/global/local-users"

    payload = {
	"username": "newLocalUser",
	"password" : "cisco123",
	"pw-type" : 7,
	"privilege": 15
}
    headers = {
        'X-auth-token': device['token-id'],
        'Authorization': authorization,
        'cache-control': "no-cache",
        'Postman-Token': "7d876d07-f120-4515-8ee7-43d9ac7f2a12"

}

    response = requests.request("POST", url, data=payload, headers=headers, verify = False)

    #Import output into dictionary
    users = json.loads(response.text)

f = open("output.txt", "w")


f.close()

