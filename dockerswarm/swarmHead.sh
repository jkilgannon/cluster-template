#!/bin/bash

set -x

echo "swarmHead.sh"

# preseed
export DEBIAN_FRONTEND=noninteractive
sudo sh -c 'echo "libssl1.1 libraries/restart-without-asking boolean true" | debconf-set-selections'
sudo sh -c 'echo "libssl1.1:amd64 libraries/restart-without-asking boolean true" | debconf-set-selections'

# Install docker swarm

#sudo apt-get update -y && sudo apt-get upgrade -y 
## Now reboot!
#sudo apt-get install apt-transport-https software-properties-common ca-certificates curl -y 
#wget https://download.docker.com/linux/ubuntu/gpg && sudo apt-key add gpg
#sudo sh -c 'echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" >> /etc/apt/sources.list'
#sudo apt-get update -y
#sudo apt-get install docker-ce -y
#sudo systemctl start docker && sudo systemctl enable docker
####sudo groupadd docker && sudo usermod -aG docker dockeruser


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

#Firewall
sudo ufw allow 2376/tcp && sudo ufw allow 7946/udp && sudo ufw allow 7946/tcp && sudo ufw allow 80/tcp && sudo ufw allow 2377/tcp && sudo ufw allow 4789/udp
#sudo ufw reload && sudo ufw enable
sudo systemctl restart docker

# Install Docker Machine
sudo echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" | sudo tee -a /etc/apt/sources.list
sudo apt-get update -y
curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine 
sudo chmod +x /tmp/docker-machine
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
scripts=( docker-machine-prompt.bash docker-machine-wrapper.bash docker-machine.bash ); for i in "${scripts[@]}"; do sudo wget https://raw.githubusercontent.com/docker/machine/v0.13.0/contrib/completion/bash/${i} -P /etc/bash_completion.d; done

# Create docker swarm cluster
sudo mkdir /software/configs
#LOCAL_DOCKER_IP=$(ip route get 192.168.1.0 | sed -n '/src/{s/.*src *\([^ ]*\).*/\1/p;q}')
LOCAL_DOCKER_IP=$(ip route get $1.0 | sed -n '/src/{s/.*src *\([^ ]*\).*/\1/p;q}')
sudo docker swarm init --advertise-addr $LOCAL_DOCKER_IP | awk '/docker swarm join --token/ {print}' > /software/configs/joinSwarm.sh
sudo chmod 755 /software/configs/joinSwarm.sh

#sudo docker swarm init --advertise-addr 192.168.1.1 | awk '/docker swarm join --token/ {print}' > /software/mungedata/swarmKey.txt

echo 'Done swarmHead.sh'
