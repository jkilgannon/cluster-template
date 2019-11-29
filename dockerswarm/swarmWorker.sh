#!/bin/bash

echo "swarmWorker.sh"

set -x

# Install mainline Docker
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update -y
sudo apt-get install -y docker-ce
sudo systemctl enable docker
sudo groupadd docker

while [ ! -f /software/configs/joinSwarm.sh ]; do
    sleep 60
done

source /software/configs/joinSwarm.sh

echo 'Done swarmWorker.sh'
