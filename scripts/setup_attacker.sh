#!/usr/bin/env bash
set -e
response=""
echo "This script installs required dependencies (python3, python3-requests) required for victim exploitation."
read -p "Do you want to continue? (y/n) " response
if [ $response != "y" ] ; then 
    echo "Exiting..."
    exit 0
fi
# Python and python dependencies installation
apt install python3 -y
apt install python3-requests -y

echo "Required dependencies were installed."
echo "Begin exploitation by executing simulate_attacker_traffic.py python script."