#!/bin/sh
#
# author XAKR xakr@teknologisk.dk
# version 1
#
# Script to backup the robot's /programs folder. Based on UR's own backup script.
#
# Backups will be saved to a "backup" directory of the USB-stick.


############################### general settings ###############################
LOGGER="/usr/bin/logger"
SERIALNO_FILE="/root/ur-serial"
ROBOT_SRC_DIR='/programs'
TAG="-t '$(basename $0)'"
BACKUP_DIR="$1/backup"

############################# functions ########################################

# for doc, see detailed functions script
display_msg_while_bg_process(){
  PID=$1
  MSG=$2
  COL=$3
  while kill -0 $PID 2> /dev/null; do
    echo "$MSG" | DISPLAY=:0 aosd_cat -R "$COL" -x 50 -y -50 -n "Arial Black 30" -f 1000 -u 1000 -o 1000
  done
}

# for doc, see detailed functions script
display_msg(){
  TIME=$1
  MSG=$2
  COL=$3
  echo "$MSG" | DISPLAY=:0 aosd_cat -R "$COL" -x 50 -y -50 -n "Arial Black 30" -u $TIME
}


################# initial setup ################################################

# check USB mountpoint
if [ "$1" = "" ] ; then
    $LOGGER -p user.info "$0: no mountpoint supplied, exiting."
    display_msg 15000 "$0: no mountpoint supplied, exiting. Remove USB after this message disappears." "red"
    exit 1 ; fi

# Find the serial number of the robot
if [ -e "$SERIALNO_FILE" ]; then
    SERIALNO=`head -n1 $SERIALNO_FILE`
    if [ -z $SERIALNO ]; then
        SERIALNO="no-serial-found"
    fi
else
  SERIALNO="no-serial-found"
fi


display_msg 2000 "DTI Magic file running. Do not remove USB!" "red"


####################################### backup #################################

DATADIR="$SERIALNO"
DATAPATH="$BACKUP_DIR/$DATADIR"

# Find a name for the library on the USB key (based on the serial number) to copy the data to
CNT=0
while [ -e "$DATAPATH" ]; do
  DATAPATH="${BACKUP_DIR}/${DATADIR}_${CNT}"
  let CNT+=1
done
mkdir -p $DATAPATH
$LOGGER -p user.info "$0: using datapath: $DATAPATH"

# tmpfile for list of copied files
list=$(mktemp)

# copy files
cd $ROBOT_SRC_DIR
find . | grep -E '\.(urp|script|installation|variables|vars|pvars|txt)$' | cpio -vdump --quiet $DATAPATH &> $list &
display_msg_while_bg_process $! "Backing up robot state..." "green"

# Log copied files
$LOGGER -p user.info $TAG -f $list
$LOGGER -p user.info $TAG "$0: ...copy done."

# Make sure data is written to the USB key
sync
sync


# Notify user Backup is done
display_msg 1000 "Backup done." "green"


############################## finish ##########################################
display_msg 3000 "DTI Magic file done. Remove USB." "red"
