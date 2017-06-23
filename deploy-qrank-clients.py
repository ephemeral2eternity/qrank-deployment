import os.path
import sys
from json_utils import *
from azurevmdeployment.deployer import Deployer

# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret

my_subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID', '330f37c7-1ce6-4b35-8012-68123e0bd2a9')   # your Azure Subscription Id
my_resource_group = 'qrank'            # the resource group for deployment
if sys.platform == 'win32':
    my_pub_ssh_key_path = os.path.expanduser('C://Users/Chen Wang/.ssh/chenw-theone.pub')   # the path to your rsa public key file
else:
    my_pub_ssh_key_path = os.path.expanduser('~/.ssh/chenw-theone.pub')   # the path to your rsa public key file

msg = "\nInitializing the Deployer class with subscription id: {}, resource group: {}" \
    "\nand public key located at: {}...\n\n"
msg = msg.format(my_subscription_id, my_resource_group, my_pub_ssh_key_path)
print(msg)

# Initialize the deployer class
deployer = Deployer(my_subscription_id, my_resource_group, my_pub_ssh_key_path)

print("Beginning the deployment... \n\n")
# Deploy the template
rgregion = "eastus"
vmname_prefix = "client-"

vm_available_zones_file = os.path.join(os.path.dirname(__file__), "azure-locations.json")
vm_locations = loadJson(vm_available_zones_file)

vmID = 10
vm_locations_left = vm_locations[9:]
for vmregion in vm_locations_left:
    vmname = vmname_prefix + str(vmID).zfill(2)
    print("Start deploying Ubuntu VM " + vmname + " in region " + vmregion)
    my_deployment = deployer.deploy(rgregion, vmregion, vmname)
    print("Done deploying!!\n\nYou can connect via: `ssh chenw@{}.westus.cloudapp.azure.com`".format(deployer.dns_label_prefix))
    vmID += 1