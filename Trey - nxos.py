import requests
import json
import urllib3

# Python3 code to iterate over a list 
list = ['10.10.20.58','10.10.20.57', '1.1.1.1', '2.2.2.2','10.10.20.58', '10.10.20.58'] 
   
for i in list:

    try:

        #supress warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        IP_ADDR = i

        ########################################
        ####  CALL ONE  ################
        #### Retrieve the NXOS Token

        #url = "https://10.10.20.58/api/aaaLogin.json"
        url = "https://" + IP_ADDR + "/api/aaaLogin.json"



        payload = "{\n\"aaaUser\" : {\n\"attributes\" : {\n\"name\" : \"admin\",\n\"pwd\" : \"Cisco123\"\n}\n}\n}"
        headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "138831b5-9e7f-47b7-9668-7488ff878aeb"
        }

        response = requests.request("POST", url, data=payload, headers=headers, verify=False, timeout=5)

        if response.status_code == 200:
            print('')
            print('Token Created for device = ' + IP_ADDR)
        else:
            print('Error creating token for device IP: ' + IP_ADDR)
            continue


        data1 = json.loads (response.text)

        mytoken = data1['imdata'][0]['aaaLogin']['attributes']['token']

        #NX-OS requires a Auth Tuple, keyword APIC-cookie as key and token as value pair
        auth_cookie = {"APIC-cookie" : mytoken}

        ########################################
        ####  CALL TWO  ################
        #Pass mytoken to the Call Two
        #url = "https://10.10.20.58/api/mo/sys/track.json"
        url = "https://" + IP_ADDR + "/api/mo/sys/track.json"


        payload = "{\n  \"trackEntity\": {\n    \"children\": [\n      {\n        \"trackObject\": {\n          \"attributes\": {\n            \"id\": \"1\"\n          },\n          \"children\": [\n            {\n        \t\t\"trackIf\": {\n            \t\t\"attributes\": {\n                        \"id\": \"eth1/3\",\n                        \"protocolType\": \"line-protocol\"\n }}}]}}]}}                       "
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "af49d3f3-c965-41e3-873b-8139959b6032"
            }

        response = requests.request("POST", url, data=payload, headers=headers, cookies=auth_cookie, verify=False)

        #data2 = json.loads (response.text)
        if response.status_code == 200:
            #print('')
            print('Track Installed for device = ' + IP_ADDR)
        else:
            print('Error configurating Tracker for device IP: ' + IP_ADDR)
            continue

        ###############################################
        ############# CALL THREE ######################
        #Pass Cookie to Call Three:  SNMP trap setting
        #url = "https://10.10.20.58/api/mo/sys/snmp/inst.json"
        url = "https://" + IP_ADDR + "/api/mo/sys/snmp/inst.json"



        payload = "\n            {\n              \"snmpInst\": {\n                \"children\": [\n                  {\n                    \"snmpLocalUser\": {\n                      \"attributes\": {\n                        \"authpwd\": \"cisco123!\",\n                        \"authtype\": \"sha\",\n                        \"privpwd\": \"Cisco123!\",\n                        \"privtype\": \"des\",\n                        \"userName\": \"NMS\"\n                      }\n                    }\n                  },\n                  {\n                    \"snmpTraps\": {\n                      \"children\": [\n                        {\n                          \"snmpTlink\": {\n                            \"children\": [\n                              {\n                                \"snmpLinkDown\": {\n                                  \"attributes\": {\n                                    \"trapstatus\": \"enable\"\n                                  }\n                                }\n                              }\n                            ]\n                          }\n                        }\n                      ]\n                    }\n                  },\n                  {\n                    \"snmpGlobals\": {\n                      \"children\": [\n                        {\n                          \"snmpSourceInterfaceTraps\": {\n                            \"attributes\": {\n                              \"ifname\": \"mgmt0\"\n                            }\n                          }\n                        }\n                      ]\n                    }\n                  },\n                  {\n                    \"snmpHost\": {\n                      \"attributes\": {\n                        \"commName\": \"NMS\",\n                        \"hostName\": \"10.10.20.1\",\n                        \"notifType\": \"traps\",\n                        \"secLevel\": \"auth\",\n                        \"udpPortID\": \"162\",\n                        \"version\": \"v3\"\n                      }\n                    }\n                  }\n                ]\n              }\n            }\n"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "5f5b551e-d6b9-4ff4-b7ba-06721872e79b"
            }

        response = requests.request("POST", url, data=payload, headers=headers, cookies=auth_cookie, verify=False)

        data = json.loads (response.text)

        if response.status_code == 200:
            print('SNMP Trap Installed for device = ' + IP_ADDR)
        else:
            print('Error configurating Tracker for device IP: ' + IP_ADDR)
            exit

        print('Moving on to next device')
        print('')

    except:  
        print('Cannot connect to IP address ' + IP_ADDR + '. Please continue.')
        print('')
        continue










