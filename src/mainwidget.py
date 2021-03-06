# -*- coding:utf-8 -*-
import ui_mainwidget
import eapauth, usermgr
from eappacket import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import threading, netifaces, socket, pynotify, time

class MainWidget(QWidget, ui_mainwidget.Ui_MainWidget):
    statusUpdateSignal = pyqtSignal(str)
    loginSucceedSignal = pyqtSignal()
    logoffSucceedSignal = pyqtSignal()
    eapfailureSignal = pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setupUi(self)
        
        self.hasLogin = False
        
        self.yah3c = None
        self.login_info = None
        self.thread = None
        self.status.hide()
        
        self.editedName = None
        self.userName.lineEdit().setPlaceholderText(u"用户名")
        
        self.trayIcon = QSystemTrayIcon(QIcon("/usr/share/qYaH3C/image/systray.png"), self)
        #self.trayIcon.show()
        self.trayIcon.activated.connect(self.onSystrayClicked)
        
        headPixmap = QPixmap("/usr/share/qYaH3C/image/icon.png")
        self.headImage.setPixmap(headPixmap)
        
        self.exist_userlist = QStringList()
        self.um = usermgr.UserMgr()
        
        self.phyiface_list = QStringList()
        for iface in netifaces.interfaces():
            self.phyiface_list.append(unicode(iface))
        self.networkInterface.addItems(self.phyiface_list)
        
        self.refreshUserInfo()
        
        # default show the first user
        if (len(self.users_info) != 0):
            self.login_info = self.users_info[0]
            self.password.setText(unicode(self.login_info['password']))
            self.networkInterface.setCurrentIndex(self.phyiface_list.indexOf(self.login_info['ethernet_interface']))
            self.userName.setCurrentIndex(0)
            
        self.connect(self.userName, SIGNAL('editTextChanged(QString)'), self.onEditTextChanged)
        self.connect(self.logButton, SIGNAL('clicked()'), self.onLogButtonClicked)
        self.connect(self.expandButton, SIGNAL('clicked()'), self.onExpandButtonClicked)
        self.statusUpdateSignal.connect(self.onStateUpdate)
        self.loginSucceedSignal.connect(self.onLoginSucceed)
        self.logoffSucceedSignal.connect(self.onLogoffSucceed)
        self.eapfailureSignal.connect(self.onEAPFailure)
        
        self.loginSucNotify = pynotify.Notification("qYaH3C", "登录成功", "/usr/share/qYaH3C/image/icon.png")
        
    def closeEvent(self, event):
        if self.hasLogin:
            self.hide()
            self.trayIcon.show()
            event.ignore()
        else:
            event.accept()

    def refreshUserInfo(self):
        self.exist_userlist.clear()
        self.users_info = self.um.get_all_users_info()
        for i in range(len(self.users_info)):
            self.exist_userlist.append(unicode(self.users_info[i]['username']))
        self.userName.clear()
        self.userName.addItems(self.exist_userlist)
        
        #if len(users_info) != 0:
        #    self.login_info = self.um.get_user_info(setindex)
        #    self.password.setText(unicode(self.login_info[1]))
        #    self.networkInterface.setCurrentIndex(self.phyiface_list.indexOf(self.login_info[2]))
        #    self.userName.setCurrentIndex(setindex)
    
    def onSystrayClicked(self):
        self.show()
        self.trayIcon.hide()
            
    def onEditTextChanged(self, string):
        self.editedName = string
        
        index = self.exist_userlist.indexOf(string)
        if index != -1:
            user_info = self.um.get_user_info(index)
            self.password.setText(user_info[1])
        else:
            self.password.setText("")
            
    def onLogButtonClicked(self):
        if self.hasLogin:
            self.hasLogin = False
            self.yah3c.send_logoff()
            self.logButton.setText(u"正在下线")
            if self.thread and not self.thread.isAlive():
                self.onEAPFailure()
        else:
            name = None
            if (self.userName.lineEdit().isModified()):
                name = self.editedName
            else:
                name = self.userName.currentText().simplified()
            
            password = str(self.password.text().simplified())
            iface = str(self.networkInterface.currentText())
            
            if not name or not password:
                return
            
            index = self.exist_userlist.indexOf(name)
            if index != -1:
                self.login_info = self.um.get_user_info(str(name))
                if self.password.isModified() or iface != self.login_info['ethernet_interface']:
                    self.login_info = {'username': self.login_info['username'], 'password': password, 'ethernet_interface': iface}
                    self.um.update_user_info(self.login_info)
            else:
                self.login_info = {'username': str(name), 'password': password, 'ethernet_interface': iface}
                self.um.add_user(self.login_info)
                self.refreshUserInfo()
                # show the new user
                self.login_info = self.um.get_user_info(str(name))
                self.password.setText(unicode(self.login_info['password']))
                self.networkInterface.setCurrentIndex(self.phyiface_list.indexOf(self.login_info['ethernet_interface']))
                self.userName.setCurrentIndex(self.exist_userlist.indexOf(name))
            
            self.yah3c = eapauth.EAPAuth(self.login_info)
            self.thread = threading.Thread(target=self.serve_forever, args=(self.yah3c, ))
            self.thread.start()
            
            self.userName.setEnabled(False)
            self.password.setEnabled(False)
            self.networkInterface.setEnabled(False)
            self.logButton.setText(u"正在登录")
            
        self.logButton.setEnabled(False)
        self.status.show()
        self.expandButton.setText(u"收起")
        
    def onExpandButtonClicked(self):
        if self.status.isHidden():
            self.status.show()
            self.expandButton.setText(u"收起")
        else:
            self.status.hide()
            self.expandButton.setText(u"详情")
        
    def onStateUpdate(self, text):
        self.status.append(text)
        self.status.moveCursor(QTextCursor.End)
        
    def onLoginSucceed(self):
        self.logButton.setEnabled(True)
        self.hasLogin = True
        self.logButton.setText(u"下线")
        self.hide()
        self.trayIcon.show()
        self.loginSucNotify.show()
        self.status.hide()
        self.expandButton.setText(u"详情")
    
    def onLogoffSucceed(self):
        self.logButton.setEnabled(True)
        self.userName.setEnabled(True)
        self.password.setEnabled(True)
        self.networkInterface.setEnabled(True)
        self.hasLogin = False
        self.logButton.setText(u"登录")
        
    def onEAPFailure(self):
        self.userName.setEnabled(True)
        self.password.setEnabled(True)
        self.networkInterface.setEnabled(True)
        self.hasLogin = False
        self.logButton.setEnabled(True)
        self.logButton.setText(u"登录")
        self.status.show()
        self.expandButton.setText(u"收起")
        
    def display_prompt(self, string):
        #print string
        self.statusUpdateSignal.emit(string)
    
    def display_login_message(self, msg):
        """
            display the messages received form the radius server,
            including the error meaasge after logging failed or 
            other meaasge from networking centre
        """
        try:
            decoded = msg.decode('gbk')
            #print decoded
            self.statusUpdateSignal.emit(decoded)
        except UnicodeDecodeError:
            #print msg
            self.statusUpdateSignal.emit(msg)
        
        
    def EAP_handler(self, eap_packet, yah3c):
        vers, type, eapol_len  = unpack("!BBH",eap_packet[:4])
        if type != EAPOL_EAPPACKET:
            self.display_prompt('Got unknown EAPOL type %i' % type)

        # EAPOL_EAPPACKET type
        code, id, eap_len = unpack("!BBH", eap_packet[4:8])
        if code == EAP_SUCCESS:
            self.display_prompt('Got EAP Success')
            self.loginSucceedSignal.emit()
            
        elif code == EAP_FAILURE:
            if (yah3c.has_sent_logoff):
                self.display_prompt('Logoff Successfully!')
                self.display_login_message(eap_packet[10:])
                self.logoffSucceedSignal.emit()
                exit(1)
            else:
                self.display_prompt('Got EAP Failure')

                self.display_login_message(eap_packet[10:])
                if self.hasLogin:
                    raise socket.error()
                else:
                    self.eapfailureSignal.emit()
                    exit(1)
        elif code == EAP_RESPONSE:
            self.display_prompt('Got Unknown EAP Response')
        elif code == EAP_REQUEST:
            reqtype = unpack("!B", eap_packet[8:9])[0]
            reqdata = eap_packet[9:4 + eap_len]
            if reqtype == EAP_TYPE_ID:
                self.display_prompt('Got EAP Request for identity')
                yah3c.send_response_id(id)
                self.display_prompt('Sending EAP response with identity = [%s]' % self.login_info['username'])
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
        
    def serve_forever(self, yah3c):
        retry_num = 1
        
        while retry_num <= 8:
            try:
                yah3c.send_start()
                while True:
                    eap_packet = yah3c.client.recv(1600)
                    # strip the ethernet_header and handle
                    self.EAP_handler(eap_packet[14:], yah3c)
                    retry_num = 1
            except socket.error, msg:
                self.display_prompt("Connection error! retry %d" % retry_num)
                time.sleep(retry_num * 2)
                retry_num += 1
            except KeyboardInterrupt:
                self.display_prompt('Interrupted by user')
                yah3c.send_logoff()
                exit(1)
        else:
            self.eapfailureSignal.emit()
            self.display_prompt('Connection Closed')
            exit(-1)
