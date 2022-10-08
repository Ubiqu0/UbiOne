#!/bin/bash
mac="70:20:84:50:43:A8"

if bluetoothctl info "$mac" | grep -q 'Connected: yes'; then
    echo "already connected  $mac"
else
    echo -e "connect ${mac} \n" | bluetoothctl
fi
