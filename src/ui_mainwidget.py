# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created: Wed Oct 10 09:59:37 2012
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
        MainWidget.resize(260, 541)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWidget.sizePolicy().hasHeightForWidth())
        MainWidget.setSizePolicy(sizePolicy)
        MainWidget.setMinimumSize(QtCore.QSize(260, 0))
        MainWidget.setMaximumSize(QtCore.QSize(260, 12222))
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainWidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.headImage = QtGui.QLabel(MainWidget)
        self.headImage.setMinimumSize(QtCore.QSize(0, 140))
        self.headImage.setMaximumSize(QtCore.QSize(16777215, 140))
        self.headImage.setText(_fromUtf8(""))
        self.headImage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.headImage.setMargin(6)
        self.headImage.setObjectName(_fromUtf8("headImage"))
        self.verticalLayout_2.addWidget(self.headImage)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.userName = QtGui.QComboBox(MainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userName.sizePolicy().hasHeightForWidth())
        self.userName.setSizePolicy(sizePolicy)
        self.userName.setMinimumSize(QtCore.QSize(240, 0))
        self.userName.setToolTip(_fromUtf8(""))
        self.userName.setEditable(True)
        self.userName.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.userName.setObjectName(_fromUtf8("userName"))
        self.verticalLayout.addWidget(self.userName)
        self.password = QtGui.QLineEdit(MainWidget)
        self.password.setMinimumSize(QtCore.QSize(240, 0))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.verticalLayout.addWidget(self.password)
        self.networkInterface = QtGui.QComboBox(MainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networkInterface.sizePolicy().hasHeightForWidth())
        self.networkInterface.setSizePolicy(sizePolicy)
        self.networkInterface.setMinimumSize(QtCore.QSize(240, 0))
        self.networkInterface.setObjectName(_fromUtf8("networkInterface"))
        self.verticalLayout.addWidget(self.networkInterface)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.logButton = QtGui.QPushButton(MainWidget)
        self.logButton.setMinimumSize(QtCore.QSize(240, 0))
        self.logButton.setAutoDefault(True)
        self.logButton.setDefault(True)
        self.logButton.setObjectName(_fromUtf8("logButton"))
        self.verticalLayout_2.addWidget(self.logButton)
        self.status = QtGui.QTextBrowser(MainWidget)
        self.status.setMinimumSize(QtCore.QSize(240, 0))
        self.status.setMaximumSize(QtCore.QSize(240, 16777215))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.status.setFont(font)
        self.status.setObjectName(_fromUtf8("status"))
        self.verticalLayout_2.addWidget(self.status)
        self.expandButton = QtGui.QPushButton(MainWidget)
        self.expandButton.setMinimumSize(QtCore.QSize(240, 0))
        self.expandButton.setObjectName(_fromUtf8("expandButton"))
        self.verticalLayout_2.addWidget(self.expandButton)
        self.author = QtGui.QLabel(MainWidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.author.setFont(font)
        self.author.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.author.setObjectName(_fromUtf8("author"))
        self.verticalLayout_2.addWidget(self.author)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "qYaH3C", None, QtGui.QApplication.UnicodeUTF8))
        self.password.setPlaceholderText(QtGui.QApplication.translate("MainWidget", "密码", None, QtGui.QApplication.UnicodeUTF8))
        self.logButton.setText(QtGui.QApplication.translate("MainWidget", "登录", None, QtGui.QApplication.UnicodeUTF8))
        self.expandButton.setText(QtGui.QApplication.translate("MainWidget", "详情", None, QtGui.QApplication.UnicodeUTF8))
        self.author.setText(QtGui.QApplication.translate("MainWidget", "By Zonyitoo", None, QtGui.QApplication.UnicodeUTF8))

