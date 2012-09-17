""" EAP authentication handler

This module sents EAPOL begin/logoff packet
and parses received EAP packet 

"""

__all__ = ["EAPAuth"]

import socket
import os, sys, pwd

from colorama import Fore, Style, init
# init() # required in Windows
from eappacket import *

from PyQt4.QtCore import *
import multiprocessing

def display_packet(packet):
    # print ethernet_header infomation
    print 'Ethernet Header Info: '
    print '\tFrom: ' + repr(packet[0:6])
    print '\tTo: ' + repr(packet[6:12])
    print '\tType: ' + repr(packet[12:14])

class EAPAuth:
    
    AUTH_SUCCESS = 0
    LOGOFF_SUCCESS = 1
    AUTH_FAIL = -1
    AUTH_CONTINUE = 2
    
    def __init__(self, login_info, signal, ui_prompt = True):
        # bind the h3c client to the EAP protocal 
        self.client = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETHERTYPE_PAE))
        self.client.bind((login_info[2], ETHERTYPE_PAE))
        # get local ethernet card address
        self.mac_addr = self.client.getsockname()[4]
        self.ethernet_header = get_ethernet_header(self.mac_addr, PAE_GROUP_ADDR, ETHERTYPE_PAE)
        self.loaded_plugins = []
        self.loading_plugin_names = []
        self.has_sent_logoff = False
        self.login_info = login_info
        
        self.showStatusSignal = signal
        self.ui_prompt = ui_prompt
        

    def load_plugins(self):
        homedir = os.path.expanduser('~'+os.getenv('SUDO_USER')) 
        sys.path.insert(0, homedir + '/.yah3c/plugins')
        self.load_plugins = map(__import__, self.loading_plugin_names)
        #for loading_plugin_name in self.loading_plugin_names:
            #loaded_plugin = __import__('plugins.' + loading_plugin_name)
            #self.loaded_plugins.append(getattr(loaded_plugin, loading_plugin_name))

    def invoke_plugins(self, func_name):
        for plugin in self.loaded_plugins:
            pid = os.fork()
            if pid == 0:
                if hasattr(plugin, 'root_privilege') and plugin.root_privilege == True:
                    pass
                else:
                    uid = pwd.getpwnam(os.getenv('SUDO_USER'))[2]
                    os.setuid(uid)
                getattr(plugin, func_name)(self)
                exit(0)

    def send_start(self):
        # invoke plugins 
        #self.invoke_plugins('before_auth')

        # sent eapol start packet
        eap_start_packet = self.ethernet_header + get_EAPOL(EAPOL_START)
        self.client.send(eap_start_packet)

        self.display_prompt(Fore.GREEN, 'Sending EAPOL start')

    def send_logoff(self):
        # invoke plugins 
        #self.invoke_plugins('after_logoff')

        # sent eapol logoff packet
        eap_logoff_packet = self.ethernet_header + get_EAPOL(EAPOL_LOGOFF)
        self.client.send(eap_logoff_packet)
        self.has_sent_logoff = True

        self.display_prompt(Fore.GREEN, 'Sending EAPOL logoff')

    def send_response_id(self, packet_id):
        self.client.send(self.ethernet_header + 
                get_EAPOL(EAPOL_EAPPACKET,
                    get_EAP(EAP_RESPONSE,
                        packet_id,
                        EAP_TYPE_ID,
                        "\x06\x07bjQ7SE8BZ3MqHhs3clMregcDY3Y=\x20\x20"+ self.login_info[0])))

    def send_response_md5(self, packet_id, md5data):
        md5 = self.login_info[1][0:16]
        if len(md5) < 16:
            md5 = md5 + '\x00' * (16 - len (md5))
        chap = []
        for i in xrange(0, 16):
            chap.append(chr(ord(md5[i]) ^ ord(md5data[i])))
        resp = chr(len(chap)) + ''.join(chap) + self.login_info[0]
        eap_packet = self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_RESPONSE, packet_id, EAP_TYPE_MD5, resp))
        self.client.send(eap_packet)
  

    def send_response_h3c(self, packet_id):
        resp=chr(len(self.login_info[1]))+self.login_info[1]+self.login_info[0]
        eap_packet = self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_RESPONSE, packet_id, EAP_TYPE_H3C, resp))
        self.client.send(eap_packet)

    def display_prompt(self, color, string):
        prompt = color + Style.BRIGHT + '==> ' + Style.RESET_ALL
        prompt += Style.BRIGHT + string + Style.RESET_ALL
        
        if self.ui_prompt:
            self.showStatusSignal.emit(string)
        
        print prompt

    def display_login_message(self, msg):
        """
            display the messages received form the radius server,
            including the error meaasge after logging failed or 
            other meaasge from networking centre
        """
        try:
            decodedmsg = msg.decode('gbk')
            if self.ui_prompt:
                self.showStatusSignal.emit(decodedmsg)
            
            print decodedmsg
        except UnicodeDecodeError:
            if self.ui_prompt:
                self.showStatusSignal.emit(msg)
                
            print msg

    def display_failed_message(self, msg):
        try:
            decodedmsg = msg.decode('gbk')
            self.showStatusSignal.emit(decodedmsg)
            
            print decodedmsg
        except UnicodeDecodeError:
            self.showStatusSignal.emit(msg)
            print msg


    def EAP_handler(self, eap_packet):
        vers, type, eapol_len  = unpack("!BBH",eap_packet[:4])
        if type == EAPOL_EAPPACKET:
            code, id, eap_len = unpack("!BBH", eap_packet[4:8])
            if code == EAP_SUCCESS:
                self.display_prompt(Fore.YELLOW, 'Got EAP Success')
                # invoke plugins 
                #self.invoke_plugins('after_auth_succ')
                
                #daemonize(self.login_info, self.showStatusSignal)
            elif code == EAP_FAILURE:
                if (self.has_sent_logoff):
                    self.display_prompt(Fore.YELLOW, 'Logoff Successfully!')
                    # invoke plugins 
                    #self.invoke_plugins('after_logoff')
                    self.display_login_message(eap_packet[10:])
                    
                else:
                    self.display_prompt(Fore.YELLOW, 'Got EAP Failure')
                    # invoke plugins 
                    #self.invoke_plugins('after_auth_fail')
                    self.display_failed_message(eap_packet[10:])
                    
                #exit(-1)
            elif code == EAP_RESPONSE:
                self.display_prompt(Fore.YELLOW, 'Got Unknown EAP Response')
            elif code == EAP_REQUEST:
                reqtype = unpack("!B", eap_packet[8:9])[0]
                reqdata = eap_packet[9:4 + eap_len]
                if reqtype == EAP_TYPE_ID:
                    self.display_prompt(Fore.YELLOW, 'Got EAP Request for identity')
                    self.send_response_id(id)
                    self.display_prompt(Fore.GREEN, 'Sending EAP response with identity = [%s]' % self.login_info[0])
                elif reqtype == EAP_TYPE_H3C:
                    self.display_prompt(Fore.YELLOW, 'Got EAP Request for Allocation')
                    self.send_response_h3c(id)
                    self.display_prompt(Fore.GREEN, 'Sending EAP response with password')
                elif reqtype == EAP_TYPE_MD5:
                    data_len = unpack("!B", reqdata[0:1])[0]
                    md5data = reqdata[1:1 + data_len]
                    self.display_prompt(Fore.YELLOW, 'Got EAP Request for MD5-Challenge')
                    self.send_response_md5(id, md5data)
                    self.display_prompt(Fore.GREEN, 'Sending EAP response with password')
                else:
                    self.display_prompt(Fore.YELLOW, 'Got unknown Request type (%i)' % reqtype)
            elif code==10 and id==5:
                self.display_login_message(eap_packet[12:])
            else:
                self.display_prompt(Fore.YELLOW, 'Got unknown EAP code (%i)' % code)
            
            return code
        else:
            self.display_prompt(Fore.YELLOW, 'Got unknown EAPOL type %i' % type)
        
        return -1
            
    def serve_forever(self):
        try:
            #print self.login_info
            #self.load_plugins()
            self.send_start()
            while True:
                eap_packet = self.client.recv(1600)
                # strip the ethernet_header and handle
                
                code = self.EAP_handler(eap_packet[14:])
                if code == EAP_SUCCESS:
                    return True
                elif code == EAP_FAILURE:
                    return False
        except KeyboardInterrupt:
            print Fore.RED + Style.BRIGHT + 'Interrupted by user' + Style.RESET_ALL
            self.send_logoff()
        except socket.error, msg:
            self.display_failed_message("Connection Error")
            return False

def daemonize (login_info, signal):
    
    yah3c_noprompt = EAPAuth(login_info, signal, ui_prompt = False)
    process = multiprocessing.Process(target=yah3c_noprompt.serve_forever)
    process.start()
    exit(1)
