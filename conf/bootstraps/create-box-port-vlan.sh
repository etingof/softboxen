#!/bin/bash
#
# Example Softboxen REST API server bootstrapping
#
ENDPOINT=http://localhost:5000/softboxen/v1

path="`dirname \"$0\"`"

. $path/functions.sh

# Create a network device (admin operation)
req='{
  "vendor": "example",
  "model": "switch",
  "version": "1",
  "description": "Example Switch",
  "hostname": "backbone-sw-01",
  "mgmt_address": "10.0.0.12"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Create login credentials at the switch (admin operation)
req='{
  "user": "admin",
  "password": "secret"
}'

credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Create privileged credentials at the switch (admin operation)
req='{
  "user": "<enable>",
  "password": "secret"
}'

credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Create a physical port at the network device (admin operation)
req='{
  "name": "1/16",
  "description": "Physical port #1",
  "shutdown": false,
  "speed": "1G",
  "auto_negotiation": true,
  "mtu": 1495
}'

port_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

# VLAN port on top of physical port (CLI operation)
req='{
  "vlan_num": 1,
  "name": "1/1/16",
  "description": "VLAN access port #1",
  "role": "access",
  "shutdown": false,
  "mtu": 1495,
  "access_group_in": "",
  "access_group_out": "",
  "ip_redirect": false,
  "ip_proxy_arp": false,
  "unicast_reverse_path_forwarding": false,
  "load_interval": 100,
  "mpls_ip": "10.1.1.12"
}'

vlan_port_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports/$port_id/vlan/access)

# Create network route
req='{
  "dst": "0.0.0.0",
  "gw": "10.0.0.1",
  "metric": 2
}'

route_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/routes)
