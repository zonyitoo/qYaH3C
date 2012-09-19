#!/bin/sh

INSTALL_PATH="/usr/share/qYaH3C"
ICON_PATH="/usr/share/pixmaps"
APP_PATH="/usr/share/applications"
BIN_PATH="/usr/bin"

mkdir -p $INSTALL_PATH
cp -rf application/* $INSTALL_PATH
ln -s $INSTALL_PATH/qyah3c.py $BIN_PATH/qyah3c
cp -f qYaH3C.desktop $APP_PATH
cp -f application/image/icon.png $ICON_PATH/qYaH3C.png

echo "Done."
echo 'Execute \"sudo qyah3c\" and have fun'
