
import ui_mainwidget
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWidget(QWidget, ui_mainwidget.Ui_MainWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setupUi(self)
