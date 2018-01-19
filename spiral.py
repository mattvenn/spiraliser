from math import cos, sin, radians, sqrt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget , QButtonGroup, QFileDialog
from PyQt5.QtGui import QPainter, QImage, QPainterPath
from PyQt5.QtGui import QPixmap, QColor, QPen, qGray, QPolygon
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import Qt, QSize, QRect, QPoint, pyqtSlot, pyqtSignal
import time

def remap(OldValue, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

# maybe some good stuff here; https://github.com/baoboa/pyqt5/blob/master/examples/painting/svgviewer/svgviewer.py
# also intertesting pixelator example here: http://doc.qt.io/qt-5/qtwidgets-itemviews-pixelator-example.html
# svg generator example: http://doc.qt.io/qt-5/qtsvg-svggenerator-example.html
class Spiraler(QtWidgets.QLabel):

    status_update_signal = pyqtSignal(str)

    def __init__(self, parent, main):
        super(Spiraler, self).__init__(parent=parent)
        self.status_update_signal.connect(main.updateStatus)
        self.pixmap = None
        self.showImage = True
        self.showSpiral = True

    def paintEvent(self, event):
        qp = QPainter(self)
        self.paint(qp)
        qp.end()

    def updatePixmap(self, pixmap):
        self.setGeometry(QtCore.QRect(0, 0, pixmap.size().width(), pixmap.size().height()))
        self.pixmap = pixmap
        self.update()

    # slider update methods - really have to repeat all this?
    def updateDensity(self, value):
        self.density = value

    def updateAmpScale(self, value):
        self.ampScale = value

    def updateDist(self, value):
        self.dist = value

    def updateShowImage(self, value):
        self.showImage = value
        self.update()

    def updateShowSpiral(self, value):
        self.showSpiral = value
        self.update()

    @pyqtSlot(int)
    def get_slider_value(self, val):
        self.density = val
        print("update density to %d" % val)

    # this code is translated from java to python from https://github.com/krummrey/SpiralFromImage
    def paint(self, qp):
        
        if self.pixmap is None:
            self.status_update_signal.emit("no image loaded")
            return

        if self.showImage:
            qp.drawPixmap(0, 0, self.pixmap) 
        
        if not self.showSpiral:
            return

        image = self.pixmap.toImage() # convert to image

        density = self.density
        dist = self.dist
        ampScale = self.ampScale
        start_time = time.time()

        radius = 1 # variable for the radius 
        alpha = 0 # angle of current point
        aradius = 0
        qp.setRenderHint(QPainter.Antialiasing)

        # Calculates the first point
        # currently just the center
        # TODO: create button to set center with mouse
        k = density/radius 
        alpha += k
        radius += dist/(360/k)
        x =  aradius*cos(radians(alpha))+image.width()/2
        y = -aradius*sin(radians(alpha))+image.height()/2
        samples = 0

        # when have we reached the far corner of the image?
        # TODO: this will have to change if not centered
        endRadius = sqrt(pow((image.width()/2), 2)+pow((image.height()/2), 2))

        shapeOn = False
        points = QPolygon()

        # Have we reached the far corner of the image?
        while radius < endRadius:
            k = (density/2)/radius 
            alpha += k
            radius += dist/(360/k)

            x =  radius*cos(radians(alpha))+image.width()/2
            y = -radius*sin(radians(alpha))+image.height()/2

            # Are we within the the image?
            # If so check if the shape is open. If not, open it
            if ((x>=0) and (x<image.width()-1) and (y>0) and (y<image.height())):
                samples += 1
                # Get the color and brightness of the sampled pixel
                c = image.pixel(int(x), int(y))
                b = qGray(c)
                b = remap(b, 0, 255, dist*ampScale, 0)

                # Move up according to sampled brightness
                aradius = radius+(b/dist)
                xa =  aradius*cos(radians(alpha))+image.width()/2
                ya = -aradius*sin(radians(alpha))+image.height()/2

                # Move around depending on density
                k = (density/2)/radius 
                alpha += k
                radius += dist/(360/k)

                # Move down according to sampled brightness
                bradius = radius-(b/dist)
                xb =  bradius*cos(radians(alpha))+image.width()/2
                yb = -bradius*sin(radians(alpha))+image.height()/2

                # Add vertices to shape
                if (shapeOn == False) :
                    shapeOn = True
                
                points.append(QPoint(xa, ya))
                points.append(QPoint(xb, yb))

            else:
                # We are outside of the image so close the shape if it is open
                if shapeOn == True:
                    qp.drawPolyline(points)
                    points.clear()
                    shapeOn = False
            
          
        if shapeOn:
            qp.drawPolyline(points)
            points.clear()

        process_time = time.time() - start_time
        self.status_update_signal.emit("finished in %f secs, took %d samples" % (process_time, samples))

