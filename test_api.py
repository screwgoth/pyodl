#!/usr/bin/python
"""
"""
"""
Globals
"""

import getopt
import sys
import time

from requests.auth import HTTPBasicAuth
from tabulate import tabulate

from api import API
from odl import ODL


user = 'admin'
password = 'admin'
domain = 'localhost'
port = '8080'
sport = '8443'
headers = ["Test Name", "Output", "Comment"]


def fill_report(statusCode, individualTest):
    if (statusCode == 200):
        individualTest.append("Success")
        individualTest.append("Got")
    elif (statusCode == 201):
        individualTest.append("Success")
        individualTest.append("Added")
    elif (statusCode == 204):
        individualTest.append("Success")
        individualTest.append("Deleted")
    elif (statusCode == 400):
        individualTest.append("Failed")
        individualTest.append("Invalid Parameter or configuration")
    elif (statusCode == 401):
        individualTest.append("Failed")
        individualTest.append("User not authorized to perform this operation")
    elif (statusCode == 404):
        individualTest.append("Failed")
        individualTest.append("The Container or Resource was not found")
    elif (statusCode == 406):
        individualTest.append("Failed")
        individualTest.append("Cannot operate on Default Container when \
            other Containers are active")
    elif (statusCode == 409):
        individualTest.append("Failed")
        individualTest.append("Failed to Add due to conflicting Name")
    elif (statusCode == 500):
        individualTest.append("Failed")
        individualTest.append("Failed to Add")
    elif (statusCode == 503):
        individualTest.append("Failed")
        individualTest.append("One or more of Controller services are \
            unavailable")
    else:
        individualTest.append("Failed")
        individualTest.append("Unknown Error")


def prepare_report(statusCode, reportList, individualTest):
    fill_report(statusCode, individualTest)
    reportList.append(individualTest)
    print tabulate(reportList, headers, tablefmt="grid")


def test_topology_all(api, reportList):
    """
    test topology_api
    """
    """
    Retrieve Topology
    """
    individualTest = []
    individualTest.append("Retreive Topology")
    response = api.retrieve_the_topology()
    prepare_report(response.status_code, reportList, individualTest)

    """
    Retrieve UserLinks
    """
    individualTest = []
    response = api.retrieve_user_links()
    individualTest.append("Retrieve UserLinks")
    prepare_report(response.status_code, reportList, individualTest)

    """
    Add User Link
    """
    #topologyUserLinkConfig
    individualTest = []
    individualTest.append("Add User Link")
    print('adding link named link1')
    link1 = {
        'status': 'Success',
        'name': 'link1',
        'srcNodeConnector': 'OF|2@OF|00:00:00:00:00:00:00:01',
        'dstNodeConnector': 'OF|2@OF|00:00:00:00:00:00:00:03'
    }
    response = api.add_user_link(topologyUserLinkConfig=link1)
    prepare_report(response.status_code, reportList, individualTest)
    time.sleep(1)
#     response = api.retrieve_user_links()
#     time.sleep(1)

    """
    Delete User Link
    """
    print('deleting link link1')
    individualTest = []
    individualTest.append("Delete User Link")
    response = api.del_user_link(linkName='link1')
    prepare_report(response.status_code, reportList, individualTest)


def test_flow_programmer_all(api, reportList):
    """
    test flow_programmer_api
    """
    individualTest = []
    individualTest.append("Retrieve Flows")
    response = api.retrieve_flows()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve Node Flow by ID")
    response = api.retrieve_node_flows(nodeId='00:00:00:00:00:00:00:01')
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve Flow by Name and ID")
    response = api.retrieve_flow_by_name(nodeId='00:00:00:00:00:00:00:01',
                                         flowName='NORMAL')
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Add a Flow")
    flow1 = {
        'installInHw': 'true',
        'name': 'flow1',
        'node': {
            'id': '00:00:00:00:00:00:00:01',
            'type': 'OF'
        },
        'ingressPort': '1',
        'priority': '5',
        'etherType': '0x800',
        'actions': [
            'DROP'
        ]
    }
    response = api.add_or_modify_flow(flowConfig=flow1)
    prepare_report(response.status_code, reportList, individualTest)

    time.sleep(1)
    api.retrieve_node_flows(nodeId='00:00:00:00:00:00:00:01')

    individualTest = []
    individualTest.append("Toggle a Flow Configuration")
    #print('toggle a flow')
    response = api.toggle_flow_by_name(nodeId='00:00:00:00:00:00:00:01',
                                       flowName='flow1', nodeType='OF')
    prepare_report(response.status_code, reportList, individualTest)

    time.sleep(1)

    individualTest = []
    individualTest.append("Delete a Flow")
    response = api.del_flow_by_name(nodeId='00:00:00:00:00:00:00:01',
                                    flowName='flow1', nodeType='OF')
    prepare_report(response.status_code, reportList, individualTest)

    response = api.retrieve_node_flows(nodeId='00:00:00:00:00:00:00:01')


def test_host_tracker_all(api, reportList):
    """
    test host_tracker_api
    """
    #print('host_tracker_api')
    individualTest = []
    individualTest.append("Retrieve all Active Hosts")
    response = api.retrieve_active_hosts()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve all Inactive Hosts")
    response = api.retrieve_inactive_hosts()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve Host by IP Address")
    response = api.retrieve_host_by_address(networkAddress='10.0.0.1')
    prepare_report(response.status_code, reportList, individualTest)

    #hostConfig
    host1 = {
        'dataLayerAddress': '00:00:00:00:00:00:10:01',
        'nodeType': 'OF',
        'nodeId': '00:00:00:00:00:00:00:01',
        'nodeConnectorId': '39',
        'vlan': '1',
        'staticHost': 'true',
        'networkAddress': '10.0.1.1'
    }
    #I may add a nodeConnector to a switch, and then to add a host1
    individualTest = []
    individualTest.append("Add a Host")
    response = api.add_host(hostConfig=host1)
    prepare_report(response.status_code, reportList, individualTest)
    time.sleep(3)

    individualTest = []
    individualTest.append("Delete a Host by IP Address")
    response = api.del_host(networkAddress='10.0.1.1')
    prepare_report(response.status_code, reportList, individualTest)


def test_static_route_all(api, reportList):
    """
    test static_route_api
    """
    individualTest = []
    individualTest.append("Retrieve all Static Routes")
    response = api.retrieve_all_static_routes()
    prepare_report(response.status_code, reportList, individualTest)

    route1 = {
        'name': 'route1',
        'prefix': '10.0.1.0/24',
        'nextHop': '10.0.0.1'
    }

    individualTest = []
    individualTest.append("Retrieve Static Route by Name")
    response = api.retrieve_static_route_by_name(route='test-route1')
    prepare_report(response.status_code, reportList, individualTest)

    print('add route1')
    individualTest = []
    individualTest.append("Add Static Route")
    response = api.add_static_route(staticRoute=route1)
    prepare_report(response.status_code, reportList, individualTest)
    time.sleep(1)

    individualTest = []
    individualTest.append("Delete Static Route")
    response = api.del_static_route(route='route1')
    prepare_report(response.status_code, reportList, individualTest)


def test_statistics_all(api, reportList):
    """
    test statistics_api
    """
    individualTest = []
    individualTest.append("Retrieve All Statistics")
    response = api.retrieve_all_statistics_flow()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve all Statisics Ports")
    response = api.retrieve_all_statistics_port()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve all Statistics Tables")
    response = api.retrieve_all_statistics_table()
    prepare_report(response.status_code, reportList, individualTest)


def test_subnets_all(api, reportList):
    """
    test subnets_api Not Tested Now!!!
    """
    individualTest = []
    individualTest.append("Retrieve all Subnets")
    response = api.retrieve_all_subnets()
    prepare_report(response.status_code, reportList, individualTest)


def test_switch_manager_all(api, reportList):
    """
    test switch_manager_api
    """
    individualTest = []
    individualTest.append("Retrieve all Nodes")
    response = api.retrieve_all_nodes()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Save Node Configuration")
    response = api.save_nodes_config()  # save failed ???
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve Node Connectors by NodeID")
    response = api.retrieve_node_connectors_by_node(nodeId=
                                                    '00:00:00:00:00:00:00:01')
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Add Node Property")
    response = api.add_node_property(nodeId='00:00:00:00:00:00:00:01',
                                     propertyName='description',
                                     propertyValue='switch1')
    prepare_report(response.status_code, reportList, individualTest)
    time.sleep(1)

    individualTest = []
    individualTest.append("Delete Node Property")
    response = api.del_node_property(nodeId='00:00:00:00:00:00:00:01',
                                     propertyName='description')
    prepare_report(response.status_code, reportList, individualTest)


def test_user_manager_all(api, reportList):
    """
    test user_manager_api
    """
    """
    userConfig1 = {
        'user': 'testdpf',
        'password': 'testdpf',
        'roles': ['Network-Admin']
    }
    print('add_user')
    response = api.add_user(userConfig1)
    time.sleep(1)
    print('del_user')
    response = api.del_user('testdpf')
    """


def test_container_manager_all(api, reportList):
    """
    ContainerManager api
    """
    individualTest = []
    individualTest.append("Retrieve all Containers")
    response = api.retrieve_all_containers()
    prepare_report(response.status_code, reportList, individualTest)

    individualTest = []
    individualTest.append("Retrieve Controller Configuration")
    response = api.retrieve_container_config()  # can't get 'default'
    prepare_report(response.status_code, reportList, individualTest)


def test_connection_manager_all(api, reportList):
    """
    ConnectionManager api
    """
    individualTest = []
    individualTest.append("Retrieve all Controller Nodes")
    response = api.retrieve_all_nodes_of_controller('127.0.0.1')
    prepare_report(response.status_code, reportList, individualTest)


def usage():
    print 'test-api.py [-h] [-u <username>] [-p <password>] [-d <domain>] \
    [-P <port>] [-s <secure_port>]'


def main(argv):
    """Main function of the Test script"""
    try:
        opts, args = getopt.getopt(argv, "hu:p:d:P:s:",
                                   ["username=", "password=",
                                    "domain=", "port=",
                                    "secure-port="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt in ("-u", "--username"):
            global user
            user = arg
            print "Username = ", user
        elif opt in ("-p", "--password"):
            global password
            password = arg
            print "Password = ", password
        elif opt in ("-d", "--domain"):
            global domain
            domain = arg
            print "Domain = ", domain
        elif opt in ("-P", "--port"):
            global port
            port = arg
            print "Port = ", port
        elif opt in ("-s", "--secure-port"):
            global sport
            sport = arg
            print "Secure port = ", sport

    myodl = ODL(auth=HTTPBasicAuth(user, password),
                domain=domain, port=port, sec_port=sport)
    api = API(odl=myodl, format='json')
    reportList = []
    test_topology_all(api, reportList)
    test_flow_programmer_all(api, reportList)
    test_host_tracker_all(api, reportList)
    test_static_route_all(api, reportList)
    test_statistics_all(api, reportList)
    test_connection_manager_all(api, reportList)
    test_container_manager_all(api, reportList)
    test_switch_manager_all(api, reportList)
    test_subnets_all(api, reportList)
    test_user_manager_all(api, reportList)
    print tabulate(reportList, headers, tablefmt="grid")
    print 'Completed Testing'

if __name__ == '__main__':
    main(sys.argv[1:])
