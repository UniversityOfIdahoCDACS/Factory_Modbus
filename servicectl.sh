#!/bin/bash
# This script is for a convienent way of controlling the pyservice

# get root permission
if [ $EUID != 0 ]; then
    sudo -H "$0" "$@"
    exit $?
fi

case $1 in
start)
  sudo systemctl start pyController.service
  sudo systemctl status pyController.service
  ;;
stop)
  sudo systemctl stop pyController.service
  ;;
restart)
  sudo systemctl restart pyController.service
  ;;
status)
  sudo systemctl status pyController.service
  ;;
recent)
  sudo journalctl -u pyController.service --since "5 minutes ago" -n 70
  ;;
log)
  sudo journalctl -u pyController.service -n 70
  ;;
*)
  echo "Arguments start|stop|restart|status|recent|log"
esac
