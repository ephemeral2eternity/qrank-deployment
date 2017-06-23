from azurevmmanagement import vmcontrol
from json_utils import *
import os

""" Start all monitoring agents in resource group "monitoring"
"""
def startMonitoringAgents():
    rgGroup = "monitoring"
    monitoring_agents = vmcontrol.listVMs(rgGroup, "agent-")
    print(monitoring_agents)

    ## Start all monitoring agents
    for monitoring_agent in monitoring_agents:
       vmcontrol.startVM(rgGroup, monitoring_agent["name"])

""" Stop all monitoring agents in resource group "monitoring"
"""
def stopMonitoringAgents():
    rgGroup = "monitoring"
    monitoring_agents = vmcontrol.listVMs(rgGroup, "agent-")
    print(monitoring_agents)

    ## Start all monitoring agents
    for monitoring_agent in monitoring_agents:
       vmcontrol.stopVM(rgGroup, monitoring_agent["name"])


""" Dump the name, ip, location and type info for all monitoring agents into vminfo/monitoring-agents.json/csv
"""
def dumpMonitoringAgentsIps():
    rgGroup = "monitoring"
    monitoring_agents = vmcontrol.listVMs(rgGroup, "agent-")

    vminfo_folder = "vminfo"
    vminfo_json_filename = rgGroup + "-agents.json"
    vminfo_csv_filename = rgGroup + "-agents.csv"
    dumpJson(monitoring_agents, os.path.join(os.path.dirname(__file__), "vminfo", vminfo_json_filename))
    json2csv(monitoring_agents, os.path.join(os.path.dirname(__file__), "vminfo", vminfo_csv_filename), ["name", "ip", "location", "type"])


""" Dump the name, ip, location and type info for all qrank clients into vminfo/monitoring-agents.json/csv
"""
def dumpQRankClientIps():
    rgGroup = "qrank"
    qrank_clients = vmcontrol.listVMs(rgGroup, "client-")

    vminfo_folder = "vminfo"
    vminfo_json_filename = rgGroup + "-clients.json"
    vminfo_csv_filename = rgGroup + "-clients.csv"
    dumpJson(qrank_clients, os.path.join(os.path.dirname(__file__), "vminfo", vminfo_json_filename))
    json2csv(qrank_clients, os.path.join(os.path.dirname(__file__), "vminfo", vminfo_csv_filename), ["name", "ip", "location", "type"])

"""
Control scripts for QRank Clients and monitoring agents on microsoft Azure.
"""
if __name__ == '__main__':
    # stopMonitoringAgents()
    dumpQRankClientIps()
