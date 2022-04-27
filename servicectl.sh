#!/bin/bash
# This script is for a convienent way of controlling the pyservice

# get root permission
if [ $EUID != 0 ]; then
    sudo -H "$0" "$@"
    exit $?
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

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
tail-log)
  sudo journalctl -u pyController.service -n 10 -f
  ;;
tail-debuglog)
  tail -f "$SCRIPT_DIR/pyController/logs/app.log"
  ;;
*)
  echo "Arguments:
  start         - Start service
  stop          - Stop service
  restart       - Restart service
  status        - Status of service
  recent        - Displays recent logs within the last 5 minutes 
  log           - Shows last 70 journal logs
  tail-log      - Tail service output
  tail-debuglog - Tail debug log"
esac
