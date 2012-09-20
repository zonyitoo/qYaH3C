#!/bin/sh

APP_PATH='/usr/share/applications'
ICON_PATH='/usr/share/pixmaps'
SRC_PATH='/usr/share/qYaH3C'
BIN_PATH='/usr/bin'

mkdir -p ./pkg/$SRC_PATH

cp -f ./src/*.py $SRC_PATH/
cp -rf ./src/image/ $SRC_PATH/
cp -f ./src/image/icon.png $ICON_PATH/qYaH3C.png
cp -f ./src/qYaH3C.desktop $APP_PATH/
ln -s $SRC_PATH/qyah3c.py $BIN_PATH/qyah3c

echo "Done."
echo 'Execute \"sudo qyah3c\" and have fun'
