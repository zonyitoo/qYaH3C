#!/bin/sh

pyuic4 mainwidget.ui -o ui_mainwidget.py
sudo python main.py -style=gtk
