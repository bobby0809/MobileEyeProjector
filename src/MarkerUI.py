#!/usr/bin/env python
# Enter application, select UI To set-up and launch

import sys, BluetoothThread, gobject

#import cv

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass

try:
    import gtk
    import gtk.glade
    import Image
    import StringIO
except:
    sys.exit(1)

class MarkerUI:
    
    def __init__(self, blank_window, rotationAmount):
        self.gladefile = "./ui/MobileEyeMarkerUI.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        
        self.window = self.wTree.get_widget("RootWindow")
        self.markerImg = self.wTree.get_widget("MarkerImg")
        
        pilImg = Image.open("./ui/res/images/markers.png")
        
        # Reset rotation amount to as not using hardware
        rotationAmount = 0;
        
        pilImg = pilImg.rotate(rotationAmount, Image.NEAREST, True)
        pixbufImg = self.image2pixbuf(pilImg)
        
        self.markerImg.set_from_pixbuf(pixbufImg)
        
        self.window.fullscreen()
        self.isFullscreen = True
        self.window.connect('key_press_event', self.on_RootWindow_key_press_event)
        
        self.window.show()
        
        self.blank_window = blank_window
        
        if self.window:
            self.window.connect("destroy", self.window_destroy)
        
    def hide(self):
        self.window.hide()
    
    def on_RootWindow_key_press_event(self, widget, event):
        
        if event.keyval == 65307:
            #Escape Key Pressed
            print "MarkerUI: Escape Key Pressed"
            self.close_program()
        elif event.keyval == 102:
            if self.isFullscreen == True:
                self.window.unfullscreen()
                self.isFullscreen = False
            else:
                self.window.fullscreen()
                self.isFullscreen = True
    
    def window_destroy(self, widget):
        self.close_program()
    
    def close_program(self):
        self.window.hide()
        self.blank_window.close_program()
    
    def image2pixbuf(self, img):
        fileOut = StringIO.StringIO()
        img.save(fileOut, "png")
        contents = fileOut.getvalue()
        fileOut.close()
        loader = gtk.gdk.PixbufLoader("png")
        loader.write(contents, len(contents))
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf
    
    def change_marker(self, cornerCoords):
        
        imageID = int(cornerCoords[0])
        
        #if(imageID == -1):
        #    im = cv.LoadImage("./ui/res/images/products/-1.png", cv.CV_LOAD_IMAGE_UNCHANGED)
        #    #pilImg = Image.open("./ui/res/images/products/-1.png")
        #elif(imageID == 0):
        #    im = cv.LoadImage("./ui/res/images/products/0.png", 1)
        #    #pilImg = Image.open("./ui/res/images/products/0.png")
        #elif(imageID == 1):
        #    im = cv.LoadImage("./ui/res/images/products/1.png", 1)
        #    #pilImg = Image.open("./ui/res/images/products/1.png")
        #elif(imageID == 2):
        #    im = cv.LoadImage("./ui/res/images/products/2.png", 1)
        #    #pilImg = Image.open("./ui/res/images/products/2.png")
        #elif(imageID == 3):
        #    im = cv.LoadImage("./ui/res/images/products/3.png", 1)
        #    #pilImg = Image.open("./ui/res/images/products/3.png")
        #elif(imageID == 4):
        #    im = cv.LoadImage("./ui/res/images/products/4.png", 1)
        #    #pilImg = Image.open("./ui/res/images/products/4.png")
        
        #x1 = 0;
        #y1 = 0;
        #x2 = 400;
        #y2 = 0;
        #x3 = 400;
        #y3 = 400;
        #x4 = 0;
        #y4 = 400;
        
        #a_array = [int(cornerCoords[1]), int(cornerCoords[2]), 1, 0, 0, 0, -(int(cornerCoords[1])*x1), -(int(cornerCoords[2])*x1), -x1,
        #           0, 0, 0, int(cornerCoords[1]), int(cornerCoords[2]), 1, -(int(cornerCoords[1])*y1), -(int(cornerCoords[2])*y1), -y1,
        #           int(cornerCoords[3]), int(cornerCoords[4]), 1, 0, 0, 0, -(int(cornerCoords[3])*x2), -(int(cornerCoords[4])*x2), -x2,
        #           0, 0, 0, int(cornerCoords[3]), int(cornerCoords[4]), 1, -(int(cornerCoords[3])*y2), -(int(cornerCoords[4])*y2), -y2,
        #           int(cornerCoords[5]), int(cornerCoords[6]), 1, 0, 0, 0, -(int(cornerCoords[5])*x3), -(int(cornerCoords[6])*x3), -x3,
        #           0, 0, 0, int(cornerCoords[5]), int(cornerCoords[6]), 1, -(int(cornerCoords[5])*y3), -(int(cornerCoords[6])*y3), -y3,
        #           int(cornerCoords[7]), int(cornerCoords[8]), 1, 0, 0, 0, -(int(cornerCoords[7])*x4), -(int(cornerCoords[8])*x4), -x4,
        #           0, 0, 0, int(cornerCoords[7]), int(cornerCoords[8]), 1, -(int(cornerCoords[7])*y4), -(int(cornerCoords[8])*y4), -y4
        #           ]
        
        #w_max = 400
        #h_max = 400
        
        # 399 because array entry of 400 is 400-1
        #src = [(0,0), (399,0), (399,399), (0,399) ]
        #dst = [(int(cornerCoords[1]),int(cornerCoords[2])), (int(cornerCoords[3]),int(cornerCoords[4])), (int(cornerCoords[5]),int(cornerCoords[6])), (int(cornerCoords[7]),int(cornerCoords[8])) ]
        #trans = cv.CreateMat(3, 3, cv.CV_32FC1)
        #cv.GetPerspectiveTransform(src,dst, trans)
        
        #dst = cv.CloneImage(im)
        #0 - Top Left 1 - Bottom Left
        #dst.origin = 0
        
        #SetZero cv.SetZero(dst)
        
        #p_src = pt_array(*((p.x, p.y) for p in calib_points)) 
        #p_dst = pt_array(*((0,0), (0,h_max), (w_max,h_max), (w_max,0))) 
        #p_mat = cvCreateMat(3, 3, CV_32F) 
        
        #cvGetPerspectiveTransform(p_src, p_dst, p_mat) 
        
        #cv.SaveImage("./ui/res/images/products/out.png", im)
        #pilImg = Image.open("./ui/res/images/products/out.png")
        
        #cvGetSize(im)
        #im.toString()
        
        #pilImg = Image.fromstring("L", cv.GetSize(im), im.tostring())
        
        #pixbufImg = self.image2pixbuf(pilImg)
        #self.markerImg.set_from_pixbuf(pixbufImg)
        
        #########################################################
        #
        # No keystoning
        #
        #########################################################
        
        
        if(imageID == -1):
            pilImg = Image.open("./ui/res/images/products/-1.png")
        elif(imageID == 0):
            pilImg = Image.open("./ui/res/images/products/0.png")
        elif(imageID == 1):
            pilImg = Image.open("./ui/res/images/products/1.png")
        elif(imageID == 2):
            pilImg = Image.open("./ui/res/images/products/2.png")
        elif(imageID == 3):
            pilImg = Image.open("./ui/res/images/products/3.png")
        elif(imageID == 4):
            pilImg = Image.open("./ui/res/images/products/4.png")
            
        pixbufImg = self.image2pixbuf(pilImg)
        self.markerImg.set_from_pixbuf(pixbufImg)
        
        self.blank_window.send_bluetooth_msg("<MarkersDisplayed></MarkersDisplayed>")
    
if __name__ == "__main__":
    mobileEye = MarkerUI()
    
    gtk.gdk.threads_init()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
