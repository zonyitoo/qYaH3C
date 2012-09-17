#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_MainDialog import *

import multiprocessing, threading
import time

import usermanager
import eapauth

class MainDialog(QDialog):
    showStatusSignal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        
        mainDialogUi = Ui_MainDialog()
        mainDialogUi.setupUi(self)

        self.userName = mainDialogUi.userName
        self.password = mainDialogUi.password
        self.showStatus = mainDialogUi.showStatus
        
        self.buttonLogin = mainDialogUi.buttonLogin
        self.buttonLogoff = mainDialogUi.buttonLogoff
        self.buttonCancel = mainDialogUi.buttonCancel

        exist_userlist = QStringList()
        self.users_info = get_usersinfo()
        for i in range(len(self.users_info)):
            exist_userlist.append(unicode(self.users_info[i][0]))
        mainDialogUi.userName.addItems(exist_userlist)
        
        QtCore.QMetaType.type("QString")
        
        self.showStatusSignal.connect(self.showStatus.append)
        self.connect(self.buttonLogin, SIGNAL('clicked()'), self.onLoginClicked)
        self.connect(self.userName, SIGNAL('editTextChanged(PyQt_PyObject)'), self.onEditTextChanged)
        self.connect(self.userName, SIGNAL('currentIndexChanged(PyQt_PyObject)'), self.onCurrentIndexChanged)
        self.connect(self.buttonCancel, SIGNAL('clicked()'), self.onCancelClicked)
        self.connect(self.buttonLogoff, SIGNAL('clicked()'), self.onLogoffClicked)
        
        self.isLogoff = True

    def onLoginClicked(self):
        print self.userName.currentIndex()
        um = usermanager.UserManager()
        user_info = um.get_user_info(self.userName.currentIndex())
        
        yah3c = eapauth.EAPAuth(user_info, self.showStatusSignal)
        
        sub_thread = threading.Thread(target=self.doLogin, args=(user_info, ))
        sub_thread.start()
        
    def onLogoffClicked(self):
        print "cancel"
        self.isLogoff = True

    def onEditTextChanged(self, text):
        print text

    def onCurrentIndexChanged(self, index):
        print index

    def onCancelClicked(self):
        self.done(0)
    
    def doLogin(self, user_info):
		self.isLogoff = False
		self.noprompt_yah3c = eapauth.EAPAuth(user_info, self.showStatusSignal, ui_prompt = False)
		
		while not self.isLogoff and self.noprompt_yah3c.serve_forever():
			self.sub_process = multiprocessing.Process(target=self.noprompt_yah3c.serve_forever)
			self.sub_process.start()
			self.sub_process = multiprocessing.Process(target=self.noprompt_yah3c.serve_forever)
			self.sub_process.start()

def get_usersinfo():
    login_info = []
    um = usermanager.UserManager()
    users_info = um.get_users_info()
    return users_info

def main():
    app = QApplication(sys.argv)
    
    mainDialog = MainDialog()
    
    mainDialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
