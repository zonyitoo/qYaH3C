#!/bin/sh

APP_PATH='usr/share/applications'
ICON_PATH='usr/share/pixmaps'
SRC_PATH='usr/share/qYaH3C'

rm -rf ./pkg/
mkdir -p ./pkg/$APP_PATH
mkdir -p ./pkg/$ICON_PATH
mkdir -p ./pkg/$SRC_PATH
cp -rf ./DEBIAN ./pkg/
cp -f ./src/*.py ./pkg/$SRC_PATH/
cp -rf ./src/image/ ./pkg/$SRC_PATH/
cp -f ./src/image/icon.png ./pkg/$ICON_PATH/qYaH3C.png
cp -f ./src/qYaH3C.desktop ./pkg/$APP_PATH/

dpkg -b ./pkg qyah3c_0.6.1_all.deb
