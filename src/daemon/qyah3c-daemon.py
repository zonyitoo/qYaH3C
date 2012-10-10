import gobject
import dbus, dbus.service
import dbus.mainloop.glib

class YaH3CDaemon(dbus.service.Object):
    def __init__(self, objpath):
        dbus.service.Object__init__(self, dbus.SessionBus(), objpath)
        self.eapauth = None

    @dbus.service.method(dbus_interface = 'com.yah3c', in_signature = 'a{ss}')
    def InitYah3c(self, login_info):
        self.eapauth = EAPAuth(login_info)

    @dbus.service.method(dbus_interface = 'com.yah3c')
    def SendStart(self):
        eapauth.send_start()

    @dbus.service.method(dbus_interface = 'com.yah3c')
    def SendLogoff(self):
        eapauth.send_logoff()

    @dbus.service.method(dbus_interface = 'com.yah3c')
    def SendResponseId(self)
