from nornir import InitNornir
import getpass
from nornir_utils.plugins.functions import print_result
from pprint import pprint
from nornir_netmiko.tasks import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_get, napalm_ping, napalm_cli
import ipdb
from nornir.core.task import Task, Result
from nornir_scrapli.tasks.core import send_command
from nornir.core.filter import F 
import time 
import logging
logging.getLogger('paramiko.transport').disabled = True


with InitNornir(config_file='/home/alin/Python/demo/Inventory/config.yaml') as nr:

    cisco_xr = nr.filter(F(groups__contains="cisco_iosxr")) 
    print(cisco_xr.inventory.hosts.keys())
    cisco_ios = nr.filter(F(groups__contains="cisco_ios")) 

    #password = getpass.getpass(prompt="eneter pass:")
    #nr.inventory.defaults.password = password

    def napalm_vrf(task):
        r = task.run(task=napalm_get, getters=['get_interfaces'])
        task.host["facts"] = r.result 
        pprint(task.host["facts"])
    #results = cisco_ios.run(task=napalm_vrf)
    #num_host = len(results)
    #print(f"task was run to a number of {num_host} routers ")
    #pprint(results.failed_hosts)
    #print_result(results)

    def napalm_command(task):
        r = task.run(task=napalm_cli, commands = ['show version'] ) 
        task.host["version"] = r.result 
        pprint(task.host["version"])
    #results = cisco_ios.run(task=napalm_command)




    def netmiko_show(task):
        r = task.run(task=netmiko_send_command, command_string='show version',use_textfsm=True)
        router = task.host  # Store the Router on which the task is runned against 
        print(router)
        task.host["facts"] = r.result  # This is the dictionary were we store the structured data 
        up_days = task.host["facts"][0]['uptime']
        print(f"Router {router} is up for {up_days} days ")


    result = cisco_ios.run(task=netmiko_show)
    pprint(result.failed_hosts)
    print_result(result)
    #ipdb.set_trace()

                                                                                       

'''
    def napalm_ping_test(task):
        
        r = task.run(task=napalm_ping,dest='172.19.157.135',source='lo0')
        task.host["facts"]=r.result 
        packet_loss = task.host["facts"]['success']['packet_loss']
        router = task.host

        print(f"Router {router} has a packet loss count of {packet_loss}")
        if packet_loss !=0: 
            print(f"Router {router} failed to reach the destination ")
    start_time = time.time()
    results = cisco_ios.run(task=napalm_ping_test)
    end_time= time.time()
    exec_time = end_time - start_time

    num_hosts = len(results)
    print(f"task was run to a number of {num_hosts} routers ") 
    print(f" the execution time was {exec_time} seconds")
    print('This routers failed upon executing the task: ')
    pprint(results.failed_hosts)

'''















