# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainDialog.ui'
#
# Created: Tue Sep 18 00:06:09 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainDialog(object):
    def setupUi(self, MainDialog):
        MainDialog.setObjectName(_fromUtf8("MainDialog"))
        MainDialog.resize(320, 200)
        MainDialog.setMinimumSize(QtCore.QSize(320, 200))
        MainDialog.setMaximumSize(QtCore.QSize(320, 200))
        self.layoutWidget = QtGui.QWidget(MainDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 301, 183))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.userName = QtGui.QComboBox(self.layoutWidget)
        self.userName.setEditable(True)
        self.userName.setObjectName(_fromUtf8("userName"))
        self.verticalLayout.addWidget(self.userName)
        self.password = QtGui.QLineEdit(self.layoutWidget)
        self.password.setObjectName(_fromUtf8("password"))
        self.verticalLayout.addWidget(self.password)
        self.networkInterface = QtGui.QLineEdit(self.layoutWidget)
        self.networkInterface.setObjectName(_fromUtf8("networkInterface"))
        self.verticalLayout.addWidget(self.networkInterface)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.showStatus = QtGui.QTextBrowser(self.layoutWidget)
        self.showStatus.setObjectName(_fromUtf8("showStatus"))
        self.verticalLayout_2.addWidget(self.showStatus)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.buttonLogin = QtGui.QPushButton(self.layoutWidget)
        self.buttonLogin.setObjectName(_fromUtf8("buttonLogin"))
        self.verticalLayout_3.addWidget(self.buttonLogin)
        self.buttonLogoff = QtGui.QPushButton(self.layoutWidget)
        self.buttonLogoff.setEnabled(False)
        self.buttonLogoff.setAutoDefault(True)
        self.buttonLogoff.setObjectName(_fromUtf8("buttonLogoff"))
        self.verticalLayout_3.addWidget(self.buttonLogoff)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.buttonCancel = QtGui.QPushButton(self.layoutWidget)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.verticalLayout_3.addWidget(self.buttonCancel)
        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        MainDialog.setWindowTitle(QtGui.QApplication.translate("MainDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonLogin.setText(QtGui.QApplication.translate("MainDialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonLogoff.setText(QtGui.QApplication.translate("MainDialog", "Logoff", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("MainDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

