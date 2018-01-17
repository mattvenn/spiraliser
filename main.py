
from mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget , QButtonGroup, QFileDialog
from PyQt5.QtGui import QPainter, QImage, QPainterPath
from PyQt5.QtGui import QPixmap, QColor, QPen
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtCore import Qt, QSize, QRect
import time

class Spiraler(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Spiraler, self).__init__(parent=parent)

    # maybe some good stuff here; https://github.com/baoboa/pyqt5/blob/master/examples/painting/svgviewer/svgviewer.py
    def paintEvent(self, event):
        qp = QPainter(self)
        self.paint(qp)
        qp.end()

    def paint(self, qp):
        qp.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.moveTo(30, 30)
        path.cubicTo(30, 30, 200, 350, 350, 30)
        qp.drawPath(path)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.spiraler = Spiraler(self.tab_2)
        self.spiraler.setGeometry(QtCore.QRect(0, 0, 781, 431))
        self.spiralLabel.setObjectName("spiraler")

        #hook menus
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.saveFileDialog)

        # load the image without having to faff with menus
        self.image = QPixmap("./image.jpg")
        self.imageLabel.setPixmap(self.image)
        self.imageLabel.setFixedSize(self.image.size());

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
