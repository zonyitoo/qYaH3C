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
import eapshow

isLogoff = False

class MainDialog(QDialog):
    showStatusSignal = pyqtSignal(str)
    changeLoginButtonState = pyqtSignal(bool)
    changeLogoffButtonState = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        
        mainDialogUi = Ui_MainDialog()
        mainDialogUi.setupUi(self)

        self.userName = mainDialogUi.userName
        self.password = mainDialogUi.password
        self.showStatus = mainDialogUi.showStatus
        self.networkInterface = mainDialogUi.networkInterface
        
        self.buttonLogin = mainDialogUi.buttonLogin
        self.buttonLogoff = mainDialogUi.buttonLogoff
        self.buttonCancel = mainDialogUi.buttonCancel
        
        self.process = None
        self.thread = None
        
        self.isLogined = False

        self.exist_userNameList = QStringList()
        um = usermanager.UserManager()
        self.users_info = um.get_users_info()
        for i in range(len(self.users_info)):
            self.exist_userNameList.append(unicode(self.users_info[i][0]))
        mainDialogUi.userName.addItems(self.exist_userNameList)
        
        if len(self.users_info) != 0:
            first_user = um.get_user_info(0)
            self.password.setText(unicode(first_user[1]))
            self.networkInterface.setText(unicode(first_user[2]))
        
        QtCore.QMetaType.type("QString")
        
        self.showStatusSignal.connect(self.onTextBrowserUpdate)
        self.changeLoginButtonState.connect(self.onChangeLoginButtonState)
        self.changeLogoffButtonState.connect(self.onChangeLogoffButtonState)
        
        self.connect(self.buttonLogin, SIGNAL('clicked()'), self.onLoginClicked)
        self.connect(self.userName, SIGNAL('editTextChanged(QString)'), self.onEditTextChanged)
        self.connect(self.buttonCancel, SIGNAL('clicked()'), self.onCancelClicked)
        self.connect(self.buttonLogoff, SIGNAL('clicked()'), self.onLogoffClicked)
        self.connect(self, SIGNAL('finished(int)'), self.onFinish)
        
    def onChangeLoginButtonState(self, state):
        self.buttonLogin.enabledChange(state)
    def onChangeLogoffButtonState(self, state):
        self.buttonLogoff.enabledChange(state)
        
    def onLoginClicked(self):
        um = usermanager.UserManager()
        user_info = um.get_user_info(self.userName.currentIndex())
        
        eapShow = eapshow.EAPShow(self.showStatusSignal)
        self.yah3c = eapauth.EAPAuth(user_info, eapShow)
        self.yah3c.set_listener(MainListener())
        
        eapShow_noprompt = eapshow.EAPShow()
        self.yah3c_noprompt = eapauth.EAPAuth(user_info, eapShow_noprompt)
        self.yah3c_noprompt.set_listener(MainListener())
        
        self.thread = threading.Thread(target=self.doLogin)
        self.thread.start()
        
    def onLogoffClicked(self):
        self.yah3c.send_logoff()
        if self.process.is_alive():
            self.process.terminate()

    def onEditTextChanged(self, text):
        print text
        index = self.exist_userNameList.indexOf(text)
        
        if index != -1:
            um = usermanager.UserManager()
            user_info = um.get_user_info(index)
            self.password.setText(unicode(user_info[1]))
            self.networkInterface.setText(unicode(user_info[2]))
        else:
            self.password.setText("")
            self.networkInterface.setText("")

    def onCancelClicked(self):
        self.done(0)
    
    def onFinish(self, result):
        if self.process and self.process.is_alive():
            self.process.terminate()
    
    def doLogin(self):
        self.yah3c.send_start()
        
        if not self.serve(self.yah3c): return

        while not self.yah3c.has_sent_logoff:
            self.process = multiprocessing.Process(target=self.serve, args=(self.yah3c_noprompt, ))
            self.process.start()
            self.process.join(1800)
            if self.process.is_alive():
                self.process.terminate()
                
    def serve(self, yah3c):
        try:
            while True:
                eap_packet = yah3c.client.recv(1600)
                # strip the ethernet_header and handle
                
                if yah3c.EAP_handler(eap_packet[14:]): break
        except KeyboardInterrupt:
            print 'Interrupted by user'
            yah3c.send_logoff()
        except socket.error, msg:
            yah3c.show.message("Connection Error")
            yah3c.listener.onFailed()
            return False
        return True
                
    def onTextBrowserUpdate(self, string):
        self.showStatus.append(string)
        self.showStatus.moveCursor(QTextCursor.End)
        
class MainListener(eapauth.EAPListener):
    def onLoginSucceed(self):
        print "MainListener onLoginSucceed"
        
    def onLogoffSucceed(self):
        print "MainListener onLogoffSucceed"
        pass
    def onFailed(self):
        pass

def main():
    app = QApplication(sys.argv)
    
    mainDialog = MainDialog()
    
    mainDialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
