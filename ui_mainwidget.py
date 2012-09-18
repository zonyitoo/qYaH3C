# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created: Tue Sep 18 21:16:02 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName(_fromUtf8("MainWidget"))
        MainWidget.resize(400, 300)
        self.widget = QtGui.QWidget(MainWidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 258, 281))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.userName = QtGui.QComboBox(self.widget)
        self.userName.setEditable(True)
        self.userName.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.userName.setObjectName(_fromUtf8("userName"))
        self.verticalLayout.addWidget(self.userName)
        self.password = QtGui.QLineEdit(self.widget)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.verticalLayout.addWidget(self.password)
        self.networkInterface = QtGui.QComboBox(self.widget)
        self.networkInterface.setObjectName(_fromUtf8("networkInterface"))
        self.verticalLayout.addWidget(self.networkInterface)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.status = QtGui.QTextBrowser(self.widget)
        self.status.setObjectName(_fromUtf8("status"))
        self.verticalLayout_2.addWidget(self.status)
        self.widget1 = QtGui.QWidget(MainWidget)
        self.widget1.setGeometry(QtCore.QRect(279, 10, 111, 281))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.loginButton = QtGui.QPushButton(self.widget1)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.verticalLayout_3.addWidget(self.loginButton)
        self.logoffButton = QtGui.QPushButton(self.widget1)
        self.logoffButton.setEnabled(False)
        self.logoffButton.setObjectName(_fromUtf8("logoffButton"))
        self.verticalLayout_3.addWidget(self.logoffButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.expandButton = QtGui.QPushButton(self.widget1)
        self.expandButton.setObjectName(_fromUtf8("expandButton"))
        self.verticalLayout_3.addWidget(self.expandButton)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("MainWidget", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.logoffButton.setText(QtGui.QApplication.translate("MainWidget", "Logoff", None, QtGui.QApplication.UnicodeUTF8))
        self.expandButton.setText(QtGui.QApplication.translate("MainWidget", "Expand", None, QtGui.QApplication.UnicodeUTF8))

