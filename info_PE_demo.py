from ttp import ttp
from pprint import pprint
from datetime import datetime
import csv,re,time,sys,json,requests,os,urllib.request,urllib.parse,urllib.response,urllib.error
import logging
import pandas as pd


def lista_router_PE_live_Stablenet():
    url = "https://csf-get-config-device:Pr3Q632uxpp4FMXR@stablenetserver.infra.orange.intra:443/TopNStatisticSrvlet?tagfilter=H4sIAAAAAAAAALXUTQuCQBAG4Lu_Ytk_4PdHoB60boHRobvoJEuisK6S_z5xY8oOdWn2sjC8vM9pxojLrlZlcxWtApkabHkx3MWgBpwy0U0gFdQJV3IErlNrcslUpYKmlzO7wZzwI0zQMoszsaQdy7K4-Sw1P1r_Zdlo2eSWg5ZDbrloueSWh5ZHbvlo-eRWgFZAboVoheRWhFZEbu3Q2hFaxbnInCw_HbRmLxv2c8Wmsh3hpelvHSY8F0PVfxX3MIkK2AW6upda9d82bVueGrG5PZQPuctumjkFAAA=&stat=50081&top=0&minlevel=-1000&last=2,2&offset=0,0&tz=Europe%2FAthens&visible=1&width=100&type=json"   
    payload={}
    headers = {}    
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)    
    #pprint(json.loads(response.text))
    device_table =json.loads(response.text)
    #print(device_table[0])

    yaml_data = {}
    for line in device_table:
        device_name = line.get('Device Name', '')
        version = line.get('Device Operating System', '')
        groups = ['cisco_iosxr'] if version.startswith('IOS XR') else ['cisco_iosnx'] if version.startswith('NX-OS') else ['cisco_ios']

        yaml_data[device_name] = {
            'username': 'robot.csf',
            'hostname': device_name,
            'groups': groups
        }
        print(line['Device Operating System'])
        #device_name.append(line['Device Name']) 

     #Write YAML data to a file
    with open('output.yaml', 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)


    device_name = []    


    #Creez un fisier xlsx
    secondMockData = {'Device_Name': device_name}
    #secondMockDF = pd.DataFrame.from_dict(secondMockData, orient='index')
    #secondMockDF = secondMockDF.transpose()
    #secondMockDF.to_excel('C:\\Scripts_CSF\\biblioteci_CSF\\Lista_Router_retea.xlsx','Lista_Router_retea', index=False) 
    return device_name #returneaza o lista cu toate routerele din retea
lista_router_PE_live_Stablenet()