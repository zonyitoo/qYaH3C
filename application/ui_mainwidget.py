# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created: Wed Sep 19 10:05:25 2012
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWidget.sizePolicy().hasHeightForWidth())
        MainWidget.setSizePolicy(sizePolicy)
        MainWidget.setMinimumSize(QtCore.QSize(300, 0))
        MainWidget.setMaximumSize(QtCore.QSize(400, 300))
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainWidget)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.userName = QtGui.QComboBox(MainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userName.sizePolicy().hasHeightForWidth())
        self.userName.setSizePolicy(sizePolicy)
        self.userName.setEditable(True)
        self.userName.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.userName.setObjectName(_fromUtf8("userName"))
        self.verticalLayout.addWidget(self.userName)
        self.password = QtGui.QLineEdit(MainWidget)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.verticalLayout.addWidget(self.password)
        self.networkInterface = QtGui.QComboBox(MainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networkInterface.sizePolicy().hasHeightForWidth())
        self.networkInterface.setSizePolicy(sizePolicy)
        self.networkInterface.setObjectName(_fromUtf8("networkInterface"))
        self.verticalLayout.addWidget(self.networkInterface)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.loginButton = QtGui.QPushButton(MainWidget)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.verticalLayout_3.addWidget(self.loginButton)
        self.logoffButton = QtGui.QPushButton(MainWidget)
        self.logoffButton.setEnabled(False)
        self.logoffButton.setObjectName(_fromUtf8("logoffButton"))
        self.verticalLayout_3.addWidget(self.logoffButton)
        self.expandButton = QtGui.QPushButton(MainWidget)
        self.expandButton.setObjectName(_fromUtf8("expandButton"))
        self.verticalLayout_3.addWidget(self.expandButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.status = QtGui.QTextBrowser(MainWidget)
        self.status.setObjectName(_fromUtf8("status"))
        self.verticalLayout_2.addWidget(self.status)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "qYaH3C", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("MainWidget", "登录", None, QtGui.QApplication.UnicodeUTF8))
        self.logoffButton.setText(QtGui.QApplication.translate("MainWidget", "下线", None, QtGui.QApplication.UnicodeUTF8))
        self.expandButton.setText(QtGui.QApplication.translate("MainWidget", "详情", None, QtGui.QApplication.UnicodeUTF8))

