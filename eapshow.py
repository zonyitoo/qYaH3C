class EAPShow:
    def __init__(self, signal = None):
        self.signal = signal
    
    def prompt(self, string):
        if self.signal:
            self.signal.emit(string)
        
        print string
        
    def message(self, msg):
        try:
            decodedmsg = msg.decode('gbk')
            if self.signal:
                self.signal.emit(decodedmsg)
            
            print decodedmsg
        except UnicodeDecodeError:
            if self.signal:
                self.signal.emit(msg)
                
            print msg
