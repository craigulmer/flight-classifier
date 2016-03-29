#!/bin/bash

# Simple script to unpack example data and retrieve 
# FAA registration data.


ROOT_DIR=$(cd `dirname "${BASH_SOURCE[0]}"`/.. && pwd)
DATA_DIR="$ROOT_DIR/data"


# FAA Downloadable database.. it gets updated at regular intervals
# so you need to plug in its name here. See their site here:
# http://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download/
FAA_ZIP="AR032016.zip"


if [ ! -e "$DATA_DIR/superbowl_nc.txt" ]; then
    unxz -k data/superbowl_nc.txt.xz
fi

if [ ! -e "$DATA_DIR/MASTER.txt" ]; then

    if [ ! -e "$DATA_DIR/$FAA_ZIP" ]; then
        wget "http://registry.faa.gov/database/$FAA_ZIP" -O "$DATA_DIR/$FAA_ZIP"
    fi 
    if [ ! -e "$DATA_DIR/MASTER.txt" ]; then
        cd $DATA_DIR && unzip $FAA_ZIP MASTER.txt
    fi
fi
