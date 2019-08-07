#!/usr/bin/env python3

import sys, os, time, logging, os.path
from ncclient import manager
import getpass

SPAWN_OSPF = """
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config>
        <router>
            <ospf xmlns="urn:ietf:params:xml:ns:yang:ietf-ospf">
                <id>%s</id>
                <router-id>%s</router-id>
                <network>
                    <ip>%s</ip>
                    <mask>0.0.0.0</mask>
                    <area>0</area>
                </network>
            </ospf>
        </router>
    </config>
  </edit-config>
</rpc>
            """

def spawn_ospf(pyscript_conn, ospf_proc, ospf_rid, intf_ip, host, user, password):
    with manager.connect(host=host, port=22, username=user, password=password,
        look_for_keys=False, allow_agent=False, device_params={'name': 'csr'}) as ospf_push:
            pushit = SPAWN_OSPF % (ospf_proc, ospf_rid, intf_ip)
#           ospf_push.edit_config(target='running',config = pushit)
            ospf_push.edit_config(pushit, target='running')

def menu_screen():
    print('****************************************')
    print('*                                      *')
    print('*       Open Shortest Path First       *')
    print('*          Configuration Tool!         *')
    print('*                                      *')
    print('****************************************')
    print('1. Configure OSPF for Router.')
    print('2. Quit.')

def pyscript_conn():
    host = input('Host IP Address: ')
    user = input('Username: ')
    password = getpass.getpass('Password: ')

    with manager.connect(host=host, port=22, username=user, password=password,
        look_for_keys=False, allow_agent=False, device_params={'name': 'csr'}) as py_script:
        test = py_script.connected
    if test == True:
        print('')
        print('Connection Established!')
        print('')
        menu_screen()
        print('')
        menu_selection = int(input("What would you like to do? [1-2]: "))
        print('')
        if menu_selection == 1:
            #intf = input('Enter interface to put in OSPF process: ')
            intf_ip = input('Enter IP address of interface: ')
            ospf_proc = input('Enter OSPF Process ID: ')
            ospf_rid = input('Enter OSPF RID: ')
            #ospf_area = input('Enter the OSPF Area ID for interface: ')
            spawn_ospf(py_script, ospf_proc, ospf_rid, intf_ip, host, user, password)
            print('OSPF has been successfully configured!')
        elif menu_selection == 2:
            print('Goodbye!')
        else:
            print('You have made an invalid selection!')
    else:
        print('Connection Failed!')

if __name__ == '__main__':
    pyscript_conn()
