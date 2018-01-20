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

        self.spiraler = Spiraler(self.imageFrame, self)

        # hook menus
        self.actionOpen.triggered.connect(self.openFileDialog)

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

        self.exportSVG.clicked.connect(self.spiraler.saveSvg)
        self.showSpiral.clicked.connect(self.spiraler.updateShowSpiral)
        self.showImage.clicked.connect(self.spiraler.updateShowImage)

        # load the image without having to faff with menus
        pixmap = QPixmap("./alan.jpg")
        self.updatePixmap(pixmap)

    @QtCore.pyqtSlot(str)
    def updateStatus(self, value):
        self.statusBar.showMessage(value, 1000)
   
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Choose image", "","Image Files (*.jpg)", options=options)
        if fileName:
            pixmap = QPixmap(fileName)
            if pixmap.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.updatePixmap(pixmap)
    
    def updatePixmap(self, pixmap):
        self.spiraler.updatePixmap(pixmap)


    def saveHPGL(self):
        # maybe this should popup in another window and show the output of the command in a scrolling text box
        """
        ./src/pstoedit -xscale 1.39 -yscale 1.39  -yshift -600 -xshift -1100 -centered -f hpgl  ~/work/vec/turing.eps drawing.hpgl
        """

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
