#!/bin/bash
#
# This script will grab a screenshot on first run
# and then map the PrtSc (print screen) key to let
# the user grab additional screenshots.  
#
# Written by Anders Dubgaard <and@universal-robots.com>

set -e

# Screengrab delay
DELAY=0.2

if [[ -z $DISPLAY ]]; then
  export DISPLAY=:0
fi

# Change working directory
wd="$(dirname $0)"
cd "$wd"

BINDIR="${HOME}/.urmagic"

IMPORT="$BINDIR/import"
XBINDKEYS="$BINDIR/xbindkeys"
XBINDKEYSRC="$BINDIR/xbindkeysrc"

copy_binaries() {
  if [[ ! -d "$BINDIR" ]]; then
    mkdir "$BINDIR"
  fi
  
  if [[ ! -x "$IMPORT" ]]; then
    cp urmagic_bin/import "$IMPORT"
    chmod a+x "$IMPORT"
  fi
  
  if [[ ! -x "$XBINDKEYS" ]]; then
    cp urmagic_bin/xbindkeys "$XBINDKEYS"
    chmod a+x "$XBINDKEYS"
  fi
}

do_screenshot() {
  OUTPUT_DIR="$wd/screenshots"

  if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir "$OUTPUT_DIR"
  fi
  
  # Change to screenshots directory
  cd "$OUTPUT_DIR"

  LASTFILE="$(ls screenshot_????.png 2> /dev/null | tail -1)"

  if [[ -z $LASTFILE ]]; then
    NEW="screenshot_0000.png"
  else
    NEW="$(echo $LASTFILE | sed 's/screenshot_\(....\)\.png/\1/' | awk '{printf "screenshot_%04d.png", $1+1; exit}')"
  fi

  sleep $DELAY
  "$IMPORT" -window root "$NEW"

  sync
  sync

  echo "$(basename $NEW)" | aosd_cat -n 'Lucida Sans 32' -f 70 -u 2000 -o 200
}

setup_xbindkeys() {
  pkill xbindkeys || true

  cat > "$XBINDKEYSRC" << EOF
# map PrtScr to grab screenshot using urmagic_screenshot.sh
"/bin/bash $wd/urmagic_screenshot.sh grab"
    Print
EOF

  "$XBINDKEYS" -f "$XBINDKEYSRC"
}

if [[ "$1" = "grab" ]]; then
  do_screenshot
else
  # Warn user not to remove USB key
  echo '! USB !' | aosd_cat -R red -x 230 -y -210 -n 'Arial Black 80'

  copy_binaries
  do_screenshot
  setup_xbindkeys

  # Notify user it is ok to remove USB key
  echo '<- USB' |  aosd_cat -x 200 -y -210 -n 'Arial Black 80'
fi

exit 0
