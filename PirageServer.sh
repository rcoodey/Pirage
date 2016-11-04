#!/bin/sh

COMMAND="python3 /home/chip/Pirage/PirageServer.py"
LOGFILE="/home/chip/Pirage/PirageServerRestart.log"

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
}

writelog "Starting"
while true ; do
  $COMMAND
  writelog "Exited with status $?"
  writelog "Restarting"
done
