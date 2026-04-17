#!/usr/bin/env bash
set -e
response=""
filter="tcp port 8080"
interface=""
packet_amount=
file_amount=

read -p "Listen for local traffic? (y/n) " response
if [ $response == "y" ] ; then
    interface="lo"
elif [ $response == "n" ] ; then
    interface="eth0"
else 
    echo "Invalid choice"
    echo "Exiting..."
    exit 0
fi

read -p "Amount of packets per file (digit)? " packet_amount
read -p "Amount of files (digit)? " file_amount

tshark -i $interface -f "$filter" -a files:$file_amount -b "packets:$packet_amount" -w "../data/$(date +%F).pcapng"


