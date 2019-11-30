FROM ubuntu:18.04

ADD worker /code/repository
COPY /local/repository /local/repository

# Install 
RUN \
  apt-get update -y && \
  /local/repository/ldap/installLdapClient.sh && \
  /local/repository/nfs/installNfsClient.sh && \
  /local/repository/mpi/install_mpi_client.sh && \
  cp /local/repository/beegfs/beegfs-deb8.list /etc/apt/sources.list.d/beegfs-deb8.list && \
  wget -q https://www.beegfs.io/release/latest-stable/gpg/DEB-GPG-KEY-beegfs -O- | sudo apt-key add -  && \
  apt-get update -y && \
  apt-get install -y beegfs-helperd beegfs-utils && \
  apt-get install -y beegfs-client && \
  /opt/beegfs/sbin/beegfs-setup-client -m pfs && \
  systemctl start beegfs-helperd && \
  systemctl start beegfs-client && \
  ln -s /mnt/beegfs /scratch && \
  mkdir /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}') && \
  cp /local/repository/source/* /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}') || true && \
  chmod 755 /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}')/* && \
  cp /local/repository/source/* /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}') || true && \
  cp /local/repository/beegfs/beegfs-deb8.list /etc/apt/sources.list.d/beegfs-deb8.list && \
  wget -q https://www.beegfs.io/release/latest-stable/gpg/DEB-GPG-KEY-beegfs -O- | sudo apt-key add - && \
  apt-get update -y && \
  apt-get install -y beegfs-helperd beegfs-utils && \
  apt-get install -y beegfs-client && \
  /opt/beegfs/sbin/beegfs-setup-client -m pfs && \
  systemctl start beegfs-helperd && \
  systemctl start beegfs-client && \
  ln -s /mnt/beegfs /scratch && \
  mkdir /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}') && \
  cp /local/repository/source/* /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}') || true && \
  chmod 755 /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}')/* && \
  cp /local/repository/source/* /scratch/$(echo $HOSTNAME | awk -F'.' '{print $1}') || true && \
  apt-get update -y && \
  apt-get install -y libmunge-dev libmunge2 munge && \
  while [ ! -d /software/mungedata ]; do && \
      sleep 60 && \
  done && \
  while [ ! -f /software/mungedata/munge.key ]; do && \
      sleep 60 && \
  done && \
  cp /software/mungedata/munge.key /etc/munge/ && \
  chown munge:munge /etc/munge/munge.key && \
  chmod 400 /etc/munge/munge.key && \
  systemctl enable munge && \
  systemctl restart munge && \
  dpkg -i /software/slurm-17.11.12_1.0_amd64.deb && \
  mkdir /etc/slurm && \
  SLURMMACHINELIST=worker-[1-$(($NUMBER_OF_WORKERS))] && \
  sed -i "s/NodeName=linux1/NodeName=$SLURMMACHINELIST/g" /local/repository/slurm/slurm.conf && \
  cp /local/repository/slurm/slurm.conf /etc/slurm/ && \
  cp /local/repository/slurm/gres.conf /etc/slurm/ && \
  cp /local/repository/slurm/cgroup.conf /etc/slurm/ && \
  cp /local/repository/slurm/cgroup_allowed_devices_file.conf /etc/slurm/ && \
  cp /local/repository/slurm/slurmd.service /etc/systemd/system/ && \
  chown root:root /etc/slurm/slurm.conf && \
  chown root:root /etc/slurm/gres.conf && \
  chown root:root /etc/slurm/cgroup.conf && \
  chown root:root /etc/slurm/cgroup_allowed_devices_file.conf && \
  chown root:root /etc/slurm/slurmd.service && \
  chmod 644 /etc/slurm/slurm.conf && \
  chmod 644 /etc/slurm/gres.conf && \
  chmod 644 /etc/slurm/cgroup.conf && \
  chmod 644 /etc/slurm/cgroup_allowed_devices_file.conf && \
  chmod 644 /etc/slurm/slurmd.service && \
  mkdir -p /var/spool/slurm/d && \
  systemctl enable slurmd && \
  systemctl start slurmd && \
  USERNAMELIST=$(getent passwd {1000..60000} | sed 's/:.*//') && \
  apt-get update && \
  apt-get install -y nfs-common && \
  mkdir /mpishare && \
  mkdir /opt/shared && \
  mkdir /software && \
  mount 192.168.1.1:/software /software || true && \
  while [ ! -d /software/flagdir ]; do && \
    mount 192.168.1.1:/software /software || true && \
    sleep 60 && \
  done && \
  mount 192.168.1.1:/home /home && \
  mount 192.168.1.1:/mpishare /mpishare && \
  mount 192.168.1.1:/opt /opt/shared && \
  '192.168.1.1:/home /home nfs' | sudo tee -a /etc/fstab && \
  '192.168.1.1:/mpishare /mpishare nfs' | sudo tee -a /etc/fstab && \
  '192.168.1.1:/opt /opt/shared nfs' | sudo tee -a /etc/fstab && \
  '192.168.1.1:/software /software nfs' | sudo tee -a /etc/fstab && \
  for i in $USERNAMELIST  && \
  do && \
    usermod -d /home/$i $i && \
  done && \
  SSHDIR=/software/geni-key && \
  PRIVKEYNAME=geni-key.key && \
  if [ ! -d $SSHDIR ]; then && \
    sudo mkdir $SSHDIR && \
    sudo chmod 755 $SSHDIR && \
    PRIVKEY="${SSHDIR}/${PRIVKEYNAME}" && \
    geni-get key > ${PRIVKEY} && \
    if [ ! $? -eq 0 -o ! -s ${PRIVKEY} ]; then && \
        echo "ERROR: Failed to retrieve per-experiment key.  SSH auto-connect will not work!" && \
        exit 1 && \
    fi && \
  fi && \
  for u in $USERNAMELIST  && \
  do && \
    sudo usermod -a -G root $u && \
    sudo usermod -aG docker $u && \
    sudo -H -u $u bash -c "/local/repository/passwordless/passwordless.sh $NUMBER_OF_WORKERS" && \
  done 
  
  
