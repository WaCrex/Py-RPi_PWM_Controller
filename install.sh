#!/bin/bash

SOURCE_PATH=https://raw.githubusercontent.com/WaCrex/Python_RPi_PWM_Controller/master
INSTALL_PATH=/opt/fan_ctrl
SCRIPT=$INSTALL_PATH/fan_ctrl.py

# Check if root
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi

# Download Python script
sudo mkdir $INSTALL_PATH
wget -O $SCRIPT "$SOURCE_PATH/fan_ctrl.py"
wget -O ${SCRIPT%.py}.json "$SOURCE_PATH/fan_ctrl.json"

# Install python3-pip if not already installed
apt update -y
apt install python3-pip -y

# Install the RPi.GPIO package of not already installed
python3 -m pip install RPi.GPIO

# Run Python script on start-up
RC=/etc/rc.local
if grep -q "sudo python $SCRIPT &" "$RC";
	then
		echo "File $RC already configured. Doing nothing."
	else
		sed -i -e "s/^exit 0/sudo python ${SCRIPT//\//\\/} \&\n&/g" "$RC"
		echo "File /etc/rc.local configured."
fi
