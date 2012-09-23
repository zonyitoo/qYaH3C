#!/usr/bin/env python
# -*- coding:utf-8 -*-

__version__ = "0.6.1"

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainwidget import *
import pynotify


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("gtk"))
    
    pynotify.init('qYaH3C')
    
    mainWidget = MainWidget()
    mainWidget.show()

    exit(app.exec_())


if __name__ == '__main__':
    main()
