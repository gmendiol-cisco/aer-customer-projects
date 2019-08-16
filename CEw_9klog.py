import logging
import requests
import json

#creat and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "n9klog.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT)

logger = logging.getLogger()


url='http://10.10.20.58/ins'
switchuser='admin'
switchpassword='Cisco123'

myheaders={'content-type':'application/json'}
payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "1",
    "input": "sh version ;sh loggin nvram ;sh loggin level syslog",
    "output_format": "json"
  }
}
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
