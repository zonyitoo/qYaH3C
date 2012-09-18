
import ui_mainwidget
import eapauth, usermanager
from eappacket import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import threading
import netifaces
import socket

class MainWidget(QWidget, ui_mainwidget.Ui_MainWidget):
    statusUpdateSignal = pyqtSignal(str)
    loginSucceedSignal = pyqtSignal()
    logoffSucceedSignal = pyqtSignal()
    eapfailureSignal = pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setupUi(self)
        
        self.yah3c = None
        self.login_info = None
        self.status.hide()
        
        self.exist_userlist = QStringList()
        self.um = usermanager.UserManager()
        
        self.phyiface_list = QStringList()
        for iface in netifaces.interfaces():
            self.phyiface_list.append(unicode(iface))
        self.networkInterface.addItems(self.phyiface_list)
        
        self.setExistedUserInfo()
            
        self.connect(self.userName, SIGNAL('editTextChanged(QString)'), self.onEditTextChanged)
        self.connect(self.loginButton, SIGNAL('clicked()'), self.onLoginButtonClicked)
        self.connect(self.logoffButton, SIGNAL('clicked()'), self.onLogoffButtonClicked)
        self.connect(self.expandButton, SIGNAL('clicked()'), self.onExpandButtonClicked)
        self.statusUpdateSignal.connect(self.onStateUpdate)
        self.loginSucceedSignal.connect(self.onLoginSucceed)
        self.logoffSucceedSignal.connect(self.onLogoffSucceed)
        self.eapfailureSignal.connect(self.onEAPFailure)
        
    def setExistedUserInfo(self):
        self.exist_userlist.clear()
        users_info = self.um.get_users_info()
        for i in range(len(users_info)):
            self.exist_userlist.append(unicode(users_info[i][0]))
        self.userName.clear()
        self.userName.addItems(self.exist_userlist)
        
        if len(users_info) != 0:
            self.login_info = self.um.get_user_info(0)
            self.password.setText(unicode(self.login_info[1]))
            self.networkInterface.setCurrentIndex(self.phyiface_list.indexOf(self.login_info[2]))
            
    def onEditTextChanged(self, string):
        print string
        index = self.exist_userlist.indexOf(string)
        if index != -1:
            user_info = self.um.get_user_info(index)
            self.password.setText(user_info[1])
        else:
            self.password.setText("")
            
    def onLoginButtonClicked(self):
        name = self.userName.currentText().simplified()
        password = self.password.text().simplified()
        iface = self.networkInterface.currentText().simplified()
        
        index = self.exist_userlist.indexOf(name)
        if index != -1:
            self.login_info = self.um.get_user_info(index)
            if self.password.isModified() or iface != self.login_info[2]:
                self.login_info = (login_info[0], password, iface)
                self.um.update_user_info(self.login_info)
        else:
            self.login_info = (name, password, iface)
            self.um.create_user(self.login_info)
            self.setExistedUserInfo()
                
        self.yah3c = eapauth.EAPAuth(self.login_info)
        thread = threading.Thread(target=self.serve_forever, args=(self.yah3c, ))
        thread.start()
        
        self.loginButton.setEnabled(False)
        self.userName.setEnabled(False)
        self.password.setEnabled(False)
        self.networkInterface.setEnabled(False)
        
    def onLogoffButtonClicked(self):
        self.yah3c.send_logoff()
        
        self.logoffButton.setEnabled(False)
        
    def onExpandButtonClicked(self):
        if self.status.isHidden():
            self.status.show()
        else:
            self.status.hide()
        
    def onStateUpdate(self, text):
        self.status.append(text)
        self.status.moveCursor(QTextCursor.End)
        
    def onLoginSucceed(self):
        self.logoffButton.setEnabled(True)
    
    def onLogoffSucceed(self):
        self.loginButton.setEnabled(True)
        self.userName.setEnabled(True)
        self.password.setEnabled(True)
        self.networkInterface.setEnabled(True)
        
    def onEAPFailure(self):
        self.logoffButton.setEnabled(False)
        self.loginButton.setEnabled(True)
        self.userName.setEnabled(True)
        self.password.setEnabled(True)
        self.networkInterface.setEnabled(True)
        
    def display_prompt(self, string):
        print string
        self.statusUpdateSignal.emit(string)
    
    def display_login_message(self, msg):
        """
            display the messages received form the radius server,
            including the error meaasge after logging failed or 
            other meaasge from networking centre
        """
        try:
            decoded = msg.decode('gbk')
            print decoded
            self.statusUpdateSignal.emit(decoded)
        except UnicodeDecodeError:
            print msg
            self.statusUpdateSignal.emit(msg)
        
    def EAP_handler(self, eap_packet, yah3c):
        vers, type, eapol_len  = unpack("!BBH",eap_packet[:4])
        if type == EAPOL_EAPPACKET:
            code, id, eap_len = unpack("!BBH", eap_packet[4:8])
            if code == EAP_SUCCESS:
                self.display_prompt('Got EAP Success')
                # invoke plugins 
                #self.invoke_plugins('after_auth_succ')
                self.loginSucceedSignal.emit()
                
            elif code == EAP_FAILURE:
                if (yah3c.has_sent_logoff):
                    self.display_prompt('Logoff Successfully!')
                    # invoke plugins 
                    #self.invoke_plugins('after_logoff')
                    self.display_login_message(eap_packet[10:])
                    self.logoffSucceedSignal.emit()
                else:
                    self.display_prompt('Got EAP Failure')
                    # invoke plugins 
                    #self.invoke_plugins('after_auth_fail')
                    self.display_login_message(eap_packet[10:])
                    self.eapfailureSignal.emit()
                exit(-1)
            elif code == EAP_RESPONSE:
                self.display_prompt('Got Unknown EAP Response')
            elif code == EAP_REQUEST:
                reqtype = unpack("!B", eap_packet[8:9])[0]
                reqdata = eap_packet[9:4 + eap_len]
                if reqtype == EAP_TYPE_ID:
                    self.display_prompt('Got EAP Request for identity')
                    yah3c.send_response_id(id)
                    self.display_prompt('Sending EAP response with identity = [%s]' % self.login_info[0])
                elif reqtype == EAP_TYPE_H3C:
                    self.display_prompt('Got EAP Request for Allocation')
                    yah3c.send_response_h3c(id)
                    self.display_prompt('Sending EAP response with password')
                elif reqtype == EAP_TYPE_MD5:
                    data_len = unpack("!B", reqdata[0:1])[0]
                    md5data = reqdata[1:1 + data_len]
                    self.display_prompt('Got EAP Request for MD5-Challenge')
                    yah3c.send_response_md5(id, md5data)
                    self.display_prompt('Sending EAP response with password')
                else:
                    self.display_prompt('Got unknown Request type (%i)' % reqtype)
            elif code==10 and id==5:
                self.display_login_message(eap_packet[12:])
            else:
                self.display_prompt('Got unknown EAP code (%i)' % code)
        else:
            self.display_prompt('Got unknown EAPOL type %i' % type)
        
    def serve_forever(self, yah3c):
        retry_num = 3
        while retry_num:
            try:
                yah3c.send_start()
                retry_num = 3
                break
            except socket.error, msg:
                display_prompt("Connection error! retry %d" % retry_num)
                retry_num -= 1
            except KeyboardInterrupt:
                display_prompt('Interrupted by user')
                yah3c.send_logoff()
                retry_num = 3
                break
        else:
            yah3c.send_logoff()
            display_prompt('Connection Closed')
            exit(-1)
        
        eap_packet = None
        while True:
            while retry_num:
                try:
                    eap_packet = yah3c.client.recv(1600)
                    retry_num = 3
                    break
                except socket.error, msg:
                    display_prompt("Connection error! retry %d" % retry_num)
                    retry_num -= 1
                except KeyboardInterrupt:
                    display_prompt('Interrupted by user')
                    yah3c.send_logoff()
                    retry_num = 3
                    break
            else:
                yah3c.send_logoff()
                display_prompt('Connection Closed')
                exit(-1)
            
            # strip the ethernet_header and handle
            while retry_num:
                try:
                    self.EAP_handler(eap_packet[14:], yah3c)
                    retry_num = 3
                    break
                except socket.error, msg:
                    display_prompt("Connection error! retry %d" % retry_num)
                    retry_num -= 1
                except KeyboardInterrupt:
                    display_prompt('Interrupted by user')
                    yah3c.send_logoff()
                    retry_num = 3
                    break
            else:
                yah3c.send_logoff()
                display_prompt('Connection Closed')
                exit(-1)
