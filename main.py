#!/usr/bin/env python

from mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget , QButtonGroup, QFileDialog
from PyQt5.QtGui import QPainter, QImage, QPainterPath
from PyQt5.QtGui import QPixmap, QColor, QPen, qGray, QPolygon
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import Qt, QSize, QRect, QPoint, pyqtSignal
import time
from spiral import Spiraler


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # custom widget to show the spiral
        self.spiraler = Spiraler(self)

        # hook menus
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.saveFileDialog)

        # slots
        self.densitySlider.valueChanged.connect(self.spiraler.updateDensity)
        self.sensSlider.valueChanged.connect(self.spiraler.updateAmpScale)
        self.distSlider.valueChanged.connect(self.spiraler.updateDist)

        self.densitySlider.sliderReleased.connect(self.update)
        self.sensSlider.sliderReleased.connect(self.update)
        self.distSlider.sliderReleased.connect(self.update)

        self.densitySlider.setValue(100)
        self.sensSlider.setValue(20)
        self.distSlider.setValue(30)

        self.exportSVG.clicked.connect(self.saveSvg)

        self.showSpiral.clicked.connect(self.spiraler.updateShow)
        self.showImage.clicked.connect(self.updateShow)

        # load the image without having to faff with menus
        image = QPixmap("./fade.jpg")
        self.updateImage(image)

   
    def updateShow(self, value):
        if value:
            self.imageLabel.setPixmap(self.image)
        else:
            self.imageLabel.clear()
        
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Image Files (*.jpg)", options=options)
        if fileName:
            image = QPixmap(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.updateImage(image)
    
    def updateImage(self, image):
        self.image = image

        # can't get scaling to work - oh well.
        #self.image = self.image.scaledToWidth(self.tab_2.width())
        #image = image.scaled(self.tab_2.width(), self.tab_2.height())

        #self.imageLabel.setScaledContents(True)

        self.imageLabel.setPixmap(self.image)

        self.spiraler.setGeometry(QtCore.QRect(0, 0, self.image.size().width(), self.image.size().height()))

        self.spiraler.updateImage(self.image)


    def saveSvg(self):

        path = "save.svg"

        generator = QSvgGenerator()
        generator.setFileName(path)
        w = self.image.size().width()
        h = self.image.size().height()
        generator.setSize(QSize(w, h))
        generator.setViewBox(QRect(0, 0, w, h))
        generator.setTitle("Spiraliser!")
        qp = QPainter(generator)
        self.spiraler.paint(qp)
        qp.end()
        self.statusBar.showMessage("SVG exported to %s" % (path), 1000)

    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
        print("resize")
            print(fileName)

    def resizeEvent(self, event):
        #self.image = self.image.scaledToWidth(self.imageLabel.width())
        pass

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
