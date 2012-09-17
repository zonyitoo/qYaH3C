#!/bin/sh

pyuic4 Ui_MainDialog.ui -o Ui_MainDialog.py
sudo python main.py -style=gtk
