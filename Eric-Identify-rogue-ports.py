#Dependencies
import requests
import json

# Set up device list and dictionary for later use
ipaddress = []
device = {}
devices = []
noncompliant = {}

# Authorization string.  Note that this is based on a username/password of cisco/cisco.  
# Update as needed
authorization = "Basic Y2lzY286Y2lzY28="

# Import file for reading
f = open('ip.txt')

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

# For each device, iterate all the interfaces and check if it is active.
# If so, check if there is a comment.  
# If not, then add the device to a list. (noncompliant-devices)
# The device list should contain a list of all of the out of policy interfaces (noncompliant-interfaces)
for device in devices :
    #Conecct to each device and pull list of interfaces
    url = "https://" + device['IP Address'] + ":55443/api/v1/interfaces"

    payload = ""
    headers = {
        'X-auth-token': device['token-id'],
        'Authorization': authorization,
        'cache-control': "no-cache",
        'Postman-Token': "7d876d07-f120-4515-8ee7-43d9ac7f2a12"
    }

    response = requests.request("GET", url, data=payload, headers=headers, verify = False)

    #Import output into dictionary
    interfaces = json.loads(response.text)

    # First, set up a list so we can store all the bad ports on this device
    badport = []

    # For each interface, find out if it is enabled 
    for interface in interfaces['items'] :
        
        url = "https://" + device['IP Address'] + ":55443/api/v1/interfaces/" + interface['if-name'] + "/state"

        payload = ""
        headers = {
            'X-auth-token': device['token-id'],
            'Authorization': authorization,
            'cache-control': "no-cache",
            'Postman-Token': "212a1f19-66fb-4d9d-8960-1db4b6247b0b"
            }

        response = requests.request("GET", url, data=payload, headers=headers, verify = False)

        # Save the interface state from the REST output
        state = json.loads(response.text)

        # If the state is enabled, and there is no description on the port, add it to the badport list
        if state['enabled'] and interface['description'] == "" :
                badport.extend([interface['if-name']])
            
                #print(device['IP Address']+ " Noncompliant on interface " + interface['if-name'])

    # We now have a list of noncompliant interfaces, and a device ID.  
    # Create a dictionary of lists to pair each device with its bad ports in a referencable manner
    noncompliant.update({device['IP Address'] : badport})
    
# We now have a dictionary containing device IP addresses as keys, and lists of interfaces without descriptions paired to them
# Output the dictionary in a readable format to a text file.  Overwrite if existing
f = open("output.txt", "w")

# Header
f.write("\nThe following devices and interfaces are enabled, but have no description.\n")
f.write("Please review and take appropriate action.\n")
f.write("--------------------------------------------------------------------------\n\n")

# Iterate through the results and print into the file
for resultdevice, resultinterface in noncompliant.items() :
    # Write the concatenation of the device ID, and all the interfaces on that device which are noncompliant
    f.write(resultdevice + ": " + ', '.join(resultinterface) +'\n') 

# Housekeeping
f.close()