#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainwidget import *


def main():
    app = QApplication(sys.argv)
    
    mainWidget = MainWidget()
    mainWidget.show()

    exit(app.exec_())


if __name__ == '__main__':
    main()
