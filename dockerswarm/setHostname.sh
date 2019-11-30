#!/bin/bash

# Be sure to source this script so $HOSTNAME changes.

echo "setHostname.sh"

#set -x

# Set shorter host name, and correct the env var.
sudo hostnamectl set-hostname $(echo $HOSTNAME | awk -F'.' '{print $1}')
HOSTNAME=$(hostname)
