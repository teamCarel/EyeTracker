from PyQt5 import QtCore, QtGui, QtWidgets
import glob
"""
Template for fullscreen screen with grid
setting all components
"""
class Ui_RunWindow():
    """
    event filtr whitch catches ESC button and closes the window
    """
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
        return super(MyMainWindow, self).eventFilter(obj, event)

    """"
    setting content 
    """
    def setupUi(self, RunWindow, row, column, pictures, pictureSource, screen):
        self.pictureSource=pictureSource
        self.row=row
        self.column=column
        RunWindow.setObjectName("RunWindow")
        self.centralwidget = QtWidgets.QWidget(RunWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        """
        grid with pictures
        """
        i = 0
        j = 0
        source = []
        source = source + glob.glob(self.pictureSource+"*.png")
        source = source + glob.glob(self.pictureSource+"*.jpg")
        source = source + glob.glob(self.pictureSource+"*.bmp")
        self.field = []
        for i in range(row):
            for j in range(column):
                self.field.append(row*column)
                pixmap = QtGui.QPixmap(source[pictures[i*column+j]])
                


                scalex = (screen.width()/column)/(pixmap.width()+30)
                scaley = (screen.height()/row)/(pixmap.height()+30)
                pixmap = pixmap.scaled(pixmap.width()*scalex,pixmap.height()*scaley,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
                
                label = QtWidgets.QLabel(self.centralwidget)

                label.setText("")
                label.setPixmap(pixmap)
                label.setObjectName("Pic")
                label.setMargin(10)
                self.field[len(self.field)-1] = label
                self.gridLayout.addWidget(label, i, j, 1, 1, QtCore.Qt.AlignCenter)
        
        RunWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(RunWindow)

    """
    creates green border around selected picture
    """
    def highlightPic(self, col, row):
        try:
            self.field[col+row*self.column].setStyleSheet("background-color: green")
        except RuntimeError:
            pass
    """
    disables all borders around selected picture
    """
    def unHighlightPic(self, col, row):
        try:
            self.field[col+row*self.column].setStyleSheet("background-color: transparent")
        except RuntimeError:
            pass
