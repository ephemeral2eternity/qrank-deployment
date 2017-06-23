"""Create and manage virtual machines.

This script expects that the following environment vars are set:

AZURE_TENANT_ID: your Azure Active Directory tenant id or domain
AZURE_CLIENT_ID: your Azure Active Directory Application Client ID
AZURE_CLIENT_SECRET: your Azure Active Directory Application Secret
AZURE_SUBSCRIPTION_ID: your Azure Subscription Id
"""
import os
import traceback
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption
from msrestazure.azure_exceptions import CloudError
from haikunator import Haikunator

subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
)

""" Start a VM by denoting its name
@param: rgName ---- The resource group name
        vmName ---- The name of the vm to start
"""
def startVM(rgName, vmName):
    print('\nStart VM ' + vmName + " in resource group " + rgName)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    async_vm_start = compute_client.virtual_machines.start(rgName, vmName)
    async_vm_start.wait()

""" Start a VM by denoting its name
@param: rgName ---- The resource group name
        vmName ---- The name of the vm to start
"""
def stopVM(rgName, vmName):
    # Stop the VM
    print('\nStop VM')
    compute_client = ComputeManagementClient(credentials, subscription_id)
    async_vm_stop = compute_client.virtual_machines.power_off(rgName, vmName)
    async_vm_stop.wait()

""" List all VMs in a resource group
@param: rgName ---- The resource group name to list all VMs
"""
def listVMs(rgName, prefix=""):
    # List VM in resource group
    print('\nList VMs in resource group ' + rgName)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)

    all_vms = []
    for vm in compute_client.virtual_machines.list(rgName):
        if prefix in vm.name:
            try:
                vm_ip = network_client.public_ip_addresses.get(rgName, vm.name + "-ip").ip_address
                # print(vm_ip)
                all_vms.append({"name": vm.name, "location": vm.location, "ip": vm_ip, "type": vm.type})
            except:
                all_vms.append({"name":vm.name, "location":vm.location, "type":vm.type})

    return all_vms