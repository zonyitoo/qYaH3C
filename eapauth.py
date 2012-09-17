""" EAP authentication handler

This module sents EAPOL begin/logoff packet
and parses received EAP packet 

"""

__all__ = ["EAPAuth", "EAPListener"]

import socket
import os, sys, pwd

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
    def __init__(self, login_info, show):
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
        
        self.show = show
        self.listener = None
        
    def set_listener(self, listener):
        self.listener = listener
        listener.eapAuth = self

    def send_start(self):
        # sent eapol start packet
        eap_start_packet = self.ethernet_header + get_EAPOL(EAPOL_START)
        self.client.send(eap_start_packet)

        self.show.prompt('Sending EAPOL start')

    def send_logoff(self):
        # sent eapol logoff packet
        eap_logoff_packet = self.ethernet_header + get_EAPOL(EAPOL_LOGOFF)
        self.client.send(eap_logoff_packet)
        self.has_sent_logoff = True

        self.show.prompt('Sending EAPOL logoff')

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

    def EAP_handler(self, eap_packet):
        vers, type, eapol_len  = unpack("!BBH",eap_packet[:4])
        if type == EAPOL_EAPPACKET:
            code, id, eap_len = unpack("!BBH", eap_packet[4:8])
            if code == EAP_SUCCESS:
                self.show.prompt('Got EAP Success')
                
                self.listener.onLoginSucceed()
                return True
                
                #daemonize(self.login_info, self.showStatusSignal)
            elif code == EAP_FAILURE:
                if (self.has_sent_logoff):
                    self.show.prompt('Logoff Successfully!')
                    self.show.message(eap_packet[10:])
                    self.listener.onLogoffSucceed()
                else:
                    self.show.prompt('Got EAP Failure')
                    self.show.message(eap_packet[10:])
                    
                    self.listener.onFailed()
                    return True
            elif code == EAP_RESPONSE:
                self.show.prompt('Got Unknown EAP Response')
            elif code == EAP_REQUEST:
                reqtype = unpack("!B", eap_packet[8:9])[0]
                reqdata = eap_packet[9:4 + eap_len]
                if reqtype == EAP_TYPE_ID:
                    self.show.prompt('Got EAP Request for identity')
                    self.send_response_id(id)
                    self.show.prompt('Sending EAP response with identity = [%s]' % self.login_info[0])
                elif reqtype == EAP_TYPE_H3C:
                    self.show.prompt('Got EAP Request for Allocation')
                    self.send_response_h3c(id)
                    self.show.prompt('Sending EAP response with password')
                elif reqtype == EAP_TYPE_MD5:
                    data_len = unpack("!B", reqdata[0:1])[0]
                    md5data = reqdata[1:1 + data_len]
                    self.show.prompt('Got EAP Request for MD5-Challenge')
                    self.send_response_md5(id, md5data)
                    self.show.prompt('Sending EAP response with password')
                else:
                    self.show.prompt('Got unknown Request type (%i)' % reqtype)
            elif code==10 and id==5:
                self.show.message(eap_packet[12:])
            else:
                self.show.prompt('Got unknown EAP code (%i)' % code)
            
        else:
            self.show.prompt('Got unknown EAPOL type %i' % type)
            
        return False
        
class EAPListener:
    eapAuth = None
    
    def onLoginSucceed(self):
        pass
    def onLogoffSucceed(self):
        pass
    def onFailed(self):
        pass

def daemonize ():

    # Do first fork.
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0)   # Exit first parent.
    except OSError, e: 
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/") 
    os.umask(0) 
    os.setsid() 

    # Do second fork.
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0)   # Exit second parent.
    except OSError, e: 
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Now I am a daemon!
    
