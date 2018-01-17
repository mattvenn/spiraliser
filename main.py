from math import cos, sin, radians, sqrt
from mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget , QButtonGroup, QFileDialog
from PyQt5.QtGui import QPainter, QImage, QPainterPath
from PyQt5.QtGui import QPixmap, QColor, QPen, qGray, QPolygon
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
import time

class Spiraler(QtWidgets.QLabel):

    def __init__(self, parent, image):
        super(Spiraler, self).__init__(parent=parent)
        self.image = image.toImage() # convert to image

    # maybe some good stuff here; https://github.com/baoboa/pyqt5/blob/master/examples/painting/svgviewer/svgviewer.py
    # also intertesting pixelator example here: http://doc.qt.io/qt-5/qtwidgets-itemviews-pixelator-example.html

    # svg generator example: http://doc.qt.io/qt-5/qtsvg-svggenerator-example.html
    def paintEvent(self, event):
        qp = QPainter(self)
        self.paint(qp)
        qp.end()

    def updateImage(self, image):
        self.image = image.toImage() # convert to image

    def paint(self, qp):


        # get these from sliders
        density = 150
        radius = 100
        alpha = 5
        dist = 10
        

        aradius = 0
        mask = QColor(255,255,255) # don't draw white
        qp.setRenderHint(QPainter.Antialiasing)
        """
        path = QPainterPath()
        path.moveTo(30, 30)
        path.cubicTo(30, 30, 200, 350, 350, 30)
        qp.drawPath(path)
        """

        # Calculates the first point
        # currently just the center
        # TODO: create button to set center with mouse
        k = density/radius 
        alpha += k
        radius += dist/(360/k)
        x =  aradius*cos(radians(alpha))+self.image.width()/2
        y = -aradius*sin(radians(alpha))+self.image.height()/2

        # when have we reached the far corner of the image?
        # TODO: this will have to change if not centered
        endRadius = sqrt(pow((self.image.width()/2), 2)+pow((self.image.height()/2), 2))

        shapeOn = False
        points = QPolygon()

        # Have we reached the far corner of the image?
        while radius < endRadius:
            k = (density/2)/radius 
            alpha += k
            radius += dist/(360/k)
            x =  radius*cos(radians(alpha))+self.image.width()/2
            y = -radius*sin(radians(alpha))+self.image.height()/2

            # Are we within the the image?
            # If so check if the shape is open. If not, open it
            if ((x>=0) and (x<self.image.width()) and (y>00) and (y<self.image.height())):

                # Get the color and brightness of the sampled pixel
                c = self.image.pixel (int(x), int(y))
                b = qGray(c)
                b /= 50
                # TODO b = map (b, 0, 255, dist*ampScale, 0)

                # Move up according to sampled brightness
                aradius = radius+(b/dist)
                xa =  aradius*cos(radians(alpha))+self.image.width()/2
                ya = -aradius*sin(radians(alpha))+self.image.height()/2

                # Move down according to sampled brightness
                k = (density/2)/radius 
                alpha += k
                radius += dist/(360/k)
                bradius = radius-(b/dist)
                xb =  bradius*cos(radians(alpha))+self.image.width()/2
                yb = -bradius*sin(radians(alpha))+self.image.height()/2

                # If the sampled color is the mask color do not write to the shape
                if mask == c:
                    if shapeOn:
                        qp.drawPolyline(points)
                        points.clear()

                        print("<!-- Mask -->")
                   
                        shapeOn = False
                else:
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
                    print("<!-- Out of bounds -->")
                    shapeOn = False
            
          
        if shapeOn:
            qp.drawPolyline(points)
            points.clear()
        print("finished")

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # load the image without having to faff with menus
        self.image = QPixmap("./fade.jpg")
        self.imageLabel.setPixmap(self.image)
        self.imageLabel.setFixedSize(self.image.size());

        self.spiraler = Spiraler(self.tab_2, self.image)
        self.spiraler.setGeometry(QtCore.QRect(0, 0, 781, 431))
        self.spiralLabel.setObjectName("spiraler")

        #hook menus
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.saveFileDialog)

        self.saveSvg()
     

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Image Files (*.jpg)", options=options)
        if fileName:
            self.image = QPixmap(fileName)
            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            # can't get scaling to work - oh well.
            #self.image = self.image.scaledToWidth(self.tab_2.width())
            #image = image.scaled(self.tab_2.width(), self.tab_2.height())
            self.imageLabel.setPixmap(self.image)
            self.imageLabel.setFixedSize(self.image.size());

            self.spiraler.updateImage(self.image)
            #self.process_image()
            #self.imageLabel.setScaledContents(True)


    def saveSvg(self):

        path = "save.svg"

        generator = QSvgGenerator()
        generator.setFileName(path)
        generator.setSize(QSize(200, 200))
        generator.setViewBox(QRect(0, 0, 200, 200))
        generator.setTitle("SVG Generator Example Drawing")
        generator.setDescription("An SVG drawing created by the SVG Generator")
        qp = QPainter(generator)
        self.spiraler.paint(qp)
        qp.end()

    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def resizeEvent(self, event):
        #self.image = self.image.scaledToWidth(self.imageLabel.width())
        print("resize")

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
