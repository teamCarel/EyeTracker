from PyQt5 import QtCore, QtGui, QtWidgets
import glob

class Ui_RunWindow():
    def setupUi(self, RunWindow, row, column, pictures, pictureSource, screen):
        
        self.pictureSource=pictureSource
        self.row=row
        self.column=column
        RunWindow.setObjectName("RunWindow")
        self.centralwidget = QtWidgets.QWidget(RunWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")

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
                
                if pixmap.width() > (screen.width()/column) or pixmap.height() > (screen.height()/row):
                    if pixmap.width()>pixmap.height():
                        scale = (screen.width()/column)/pixmap.width()
                    else:
                        scale = (screen.height()/row)/pixmap.height()
                    pixmap = pixmap.scaled( pixmap.width()*scale,pixmap.height()*scale,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
                
                label = QtWidgets.QLabel(self.centralwidget)

                label.setText("")
                label.setPixmap(pixmap)
                label.setObjectName("Pic")
                label.setContentsMargins(10, 10, 10, 10)
                self.field[len(self.field)-1] = label
                self.gridLayout.addWidget(label, i, j, 1, 1, QtCore.Qt.AlignCenter)
        

        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(10, 10, 50, 20))
        self.Run.setObjectName("Run eye detection")
        self.Run.setText("Run")
        
        self.Exit = QtWidgets.QPushButton(self.centralwidget)
        self.Exit.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.Exit.setObjectName("ExitWindow")
        self.Exit.setText("Exit")


        self.ExitAll = QtWidgets.QPushButton(self.centralwidget)
        self.ExitAll.setGeometry(QtCore.QRect(10, 50, 50, 20))
        self.ExitAll.setObjectName("Exit All")
        self.ExitAll.setText("Exit All")

        RunWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(RunWindow)

    def highlightPic(self, row, col):
        self.field[col+row*self.column].setStyleSheet("background-color: green")
    def unHighlightPic(self, row, col):
        self.field[col+row*self.column].setStyleSheet("background-color: transparent")
