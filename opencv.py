import cv2
import cv2.cv as cv
import numpy
import zbar

class test():
    def __init__(self):
        cv.NamedWindow("w1", cv.CV_WINDOW_NORMAL)

#        self.capture = cv.CaptureFromCAM(camera_index) #for some reason, this doesn't work
        self.capture = cv.CreateCameraCapture(-1)
        self.vid_contour_selection()



    def vid_contour_selection(self):


      while True:

          self.frame = cv.QueryFrame(self.capture)


          aframe = numpy.asarray(self.frame[:,:])
          g = cv.fromarray(aframe)


          g = numpy.asarray(g)

          imgray = cv2.cvtColor(g,cv2.COLOR_BGR2GRAY)

          raw = str(imgray.data)
          scanner = zbar.ImageScanner()


          scanner.parse_config('enable')

          imageZbar = zbar.Image( self.frame.width, self.frame.height,'Y800', raw)
          scanner.scan(imageZbar)

          for symbol in imageZbar:

              print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data


          cv2.imshow("w1", aframe)

          c = cv.WaitKey(5)

      if c == 110: #pressing the 'n' key will cause the program to exit
        exit()
#
p = test()