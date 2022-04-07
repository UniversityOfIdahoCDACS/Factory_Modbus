#!/bin/bash

# get root permission
if [ $EUID != 0 ]; then
    sudo -H "$0" "$@"
    exit $?
fi

echo -e "\nSetting up system service"

SERVICE_NAME=pyController.service
SERVICE_PATH="/lib/systemd/system/$SERVICE_NAME"
# check if a service file already exists and delete if so.
if [ -f $SERVICE_PATH ]; then
  echo -e "\n Removing $SERVICE_NAME and replacing with new service"
  sudo rm -v $SERVICE_PATH
fi

sudo cp -v $SERVICE_NAME $SERVICE_PATH       # copy service to systemd directory
sudo chmod 644 $SERVICE_PATH
chmod +x $SERVICE_PATH

echo -e "\nsystemd reload"
sudo systemctl daemon-reload
echo -e "\nsystemd enable"
sudo systemctl enable $SERVICE_NAME
echo -e "\nsystemd start"
sudo systemctl restart $SERVICE_NAME

echo -e "\n$SERVICE_NAME setup done"
echo      "----------------------"
