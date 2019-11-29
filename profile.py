# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

pc.defineParameter( "n", "Number of worker nodes, a number from 2 to 5", portal.ParameterType.INTEGER, 2 )
params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

if params.n < 2 or params.n > 5:
  portal.context.reportError( portal.ParameterError( "You must choose at least 2 and no more than 5 worker nodes." ) )

# Lists for the nodes and such
nodeList = []

tourDescription = \
"""
This profile provides a Docker-based Slurm and Open MPI cluster installed on Ubuntu 18.04.
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

prefixForIP = "192.168.1."

beegfnNum = params.n + 1
slurmNum = params.n + 2

link = request.LAN("lan")

for i in range(0,params.n + 3):
  if i == 0:
    node = request.XenVM("nfs")
  elif i == beegfnNum:
    node = request.XenVM("pfs")
  elif i == slurmNum:
    node = request.XenVM("head")
  else:
    #node = request.DockerContainer("worker-" + str(i))
    node = request.XenVM("worker-" + str(i))
  node.cores = 4
  node.ram = 4096
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
  #node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//docker-ubuntu18-std"
  
  iface = node.addInterface("if" + str(i+1))
  iface.component_id = "eth"+ str(i+1)
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  
  if i == slurmNum:
    node.routable_control_ip = "true" 
  
  link.addInterface(iface)  
  
  # Set scripts in the repository executable and readable.
  node.addService(pg.Execute(shell="sh", command="sudo find /local/repository/ -type f -iname \"*.sh\" -exec chmod 755 {} \;"))
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/beegfs/beegfs-deb8.list")) 
  
  #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/docker/install_docker.sh"))
  
  if i == 0:
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs/startNfsHead.sh " + str(params.n) + " " + str(slurmNum)))
    #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/docker/install_docker.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/clientBeeGFS.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless/addpasswordless.sh " + str(params.n)))
  elif i == beegfnNum:
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/serverBeeGFS.sh " + str(params.n)))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/dockerswarm/swarmWorker.sh"))
  elif i == slurmNum:
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/ldap/installLdapClient.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nfs/installNfsClient.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/clientBeeGFS.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/slurm/slurmHead.sh " + str(params.n)))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mpi/install_mpi.sh " + str(params.n)))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/dockerswarm/swarmWorker.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless/addpasswordless.sh " + str(params.n)))
  else:
    #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/docker/install_docker.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/nodeWorker.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/clientBeeGFS.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/slurm/slurmClient.sh " + str(params.n)))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/beegfs/dockerswarm/swarmWorker.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless/addpasswordless.sh " + str(params.n)))
  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
