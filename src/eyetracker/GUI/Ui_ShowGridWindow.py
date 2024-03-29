from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import time
import copy

"""
clickable label over pictures
"""
class clicableLabel(QtWidgets.QLabel):
    """
    cklicked pictures counter
    """
    clicked=0
    """
    constructor
    """
    def __init__(self, widget, window):
        super().__init__()  # parent constructor
        self.index = -1
        self.clicked = False
        self.window = window
    
    """
    sets variable index
    """
    def setIndex(self, index):
        self.index = index
    
    """
    disables all borders around selected picture
    """
    def disColor(self):
        if(self.clicked):
            self.setStyleSheet("background-color: transparent")
            clicableLabel.clicked-=1
            self.clicked=False
    
    """
    on click event
    sets or unsets yellow border
    if two borders are yellow, pictures switch
    """
    def mousePressEvent(self, event):
        if(self.clicked):
            self.setStyleSheet("background-color: transparent")
            clicableLabel.clicked-=1
            self.clicked=False
        else:
            self.setStyleSheet("background-color: yellow")
            self.clicked=True
            clicableLabel.clicked+=1
            if(clicableLabel.clicked == 2):
                self.window.switch()


""""
Template for window where user setts picture position in grid
setting all components
"""
class Ui_ShowGridWindow():
    def setupUi(self, ShowGridWindow, row, column, pictures, pictureSource):
        """
        window setting
        """
        self.ShowGridWindow = ShowGridWindow
        self.row=row
        self.column=column
        self.pictures = copy.deepcopy(pictures)
        self.pictureSource = pictureSource
        ShowGridWindow.setObjectName("ShowGridWindow")
        self.centralwidget = QtWidgets.QWidget(ShowGridWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(5, 30, 5, 5)
        self.gridLayout.setObjectName("gridLayout")

        self.loadPics()

        """
        Exit without saving button
        """
        self.Exit = QtWidgets.QPushButton(self.centralwidget)
        self.Exit.setGeometry(QtCore.QRect(60, 10, 50, 20))
        self.Exit.setObjectName("ExitWindow")
        self.Exit.setText("Exit")

        """
        save current position button
        """
        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(10, 10, 50, 20))
        self.Save.setObjectName("Save")
        self.Save.setText("Save")

        ShowGridWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(ShowGridWindow)
    
    """
    loads selected pictures from source and shows them in labels in grid
    """
    def loadPics(self):
        i = 0
        j = 0
        source = glob.glob(self.pictureSource+"*.png") + glob.glob(self.pictureSource+"*.jpg") 
        self.field = []
        for i in range(self.row):
            for j in range(self.column):
                self.field.append(self.row*self.column)
                pixmap = QtGui.QPixmap(source[self.pictures[i*self.column+j]])
                pixmap = pixmap.scaled(120,120,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
                self.label = clicableLabel(self.centralwidget, self)

                self.label.setText("")
                self.label.setIndex(i*self.column+j)
                self.label.setPixmap(pixmap)
                self.label.setObjectName("Pic")
                self.label.setContentsMargins(10, 10, 10, 10)
                self.field[len(self.field)-1] = self.label
                self.gridLayout.addWidget(self.label, i, j, 1, 1, QtCore.Qt.AlignCenter)

    
    """
    switch two pictures whitch are selected in array and disables yellow borders
    """
    def switch(self):
        pics= []
        for i in range(self.row*self.column):            
            pic = self.field[i]
            if(pic.clicked):
                pics.append(self.row*self.column)
                pics[len(pics)-1] = pic.index
        temp = self.pictures[pics[0]]
        self.pictures[pics[0]]=self.pictures[pics[1]]
        self.pictures[pics[1]]=temp
        self.field[pics[0]].disColor()
        self.field[pics[1]].disColor()
        self.loadPics()
        self.ShowGridWindow.repaint()