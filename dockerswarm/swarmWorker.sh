#!/bin/bash

set -x

echo "swarmWorker.sh"

while [ ! -f /software/configs/joinSwarm.sh ]; do
    sleep 60
done

source /software/configs/joinSwarm.sh

echo 'Done swarmWorker.sh'
