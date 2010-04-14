from bluetooth import *
import threading, Queue, time, gobject

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class BluetoothThread(threading.Thread):

    def __init__(self, label_update_cb, show_markers_cb):
        threading.Thread.__init__(self)
        
        self.label_update_cb = label_update_cb
        self.show_markers_cb = show_markers_cb
        self.killThread = False
        self.server_sock=BluetoothSocket(RFCOMM)
        self.client_sock=BluetoothSocket(RFCOMM)
        print("Bluetooth init complete")
    
    # On run we try to connect to bluetooth and set up UI
    def run(self):
        
        self.update_label("Opening Bluetooth Connection")
        
        # Set the Server Timeout to 0.5 Secounds (Means Waiting to Accept a
        # connection doesn't block
        self.server_sock.settimeout(10)
        # Bind local adapter and port
        self.server_sock.bind(("",PORT_ANY))
        # The number of connections to be made
        self.server_sock.listen(1)
        
        port = self.server_sock.getsockname()[1]
        
        uuid = "00001101-0000-1000-8000-00805F9B34FB"
        
        self.update_label("Server Socket Set-Up")
        
        advertise_service(
                self.server_sock,
                "GauntFaceServer",
                service_id = uuid,
                service_classes = [uuid, SERIAL_PORT_CLASS],
                profiles = [SERIAL_PORT_PROFILE]
            )
        
        connectionOnPrevLoop = True
        
        while self.killThread == False:
            try:
                if(connectionOnPrevLoop == True):
                    self.update_label("Waiting for connection on RFCOMM channel " + str(port))
                    print("Waiting for connection")
                    connectionOnPrevLoop = False
                
                self.client_sock, client_info = self.server_sock.accept()
                
                self.update_label("Accepted Connection from " + client_info[0])
                print("Accepted Connection")
                connectionOnPrevLoop = True
                
                try:
                    while self.killThread == False:
                        data = self.client_sock.recv(1024)
                        print "Received [%s]" % data
                        
                        if len(data) == 0:
                            break
                        elif(data == "<ConnectionConfirm></ConnectionConfirm>"):
                            self.client_sock.send("<ConnectionConfirm></ConnectionConfirm>")
                            print("Sent <ConnectionConfirm></ConnectionConfirm>")
                            self.show_marker_ui()
                except IOError:
                    print("Connection broke")
                    pass
                
            except IOError:
                pass
        
        if self.run == False:
            self.server_sock.close()
        
    def update_label(self, msg):
        gobject.idle_add(self.label_update_cb, msg)
        #gtk.gdk.threads_enter()
        #self.msgLabel.set_text(msg)
        #gtk.gdk.threads_leave()
    
    def signal_kill_thread(self):
        self.killThread = True
        self.client_sock.shutdown(2)
    
    def show_marker_ui(self):
        gobject.idle_add(self.show_markers_cb)
