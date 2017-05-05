from PyQt5 import QtCore, QtGui, QtWidgets
import glob, os

class Ui_MainWindow():
    def setupUi(self, MainWindow, pictureSource):
        self.pictureSource=pictureSource
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(471, 640)
        MainWindow.setWindowTitle("Eye Tracker")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.Help = QtWidgets.QPushButton(self.centralwidget)
        self.Help.setGeometry(QtCore.QRect(430, 10, 30, 30))
        self.Help.setStyleSheet("border-radius: 15px;")
        self.Help.setObjectName("Help")
        self.Help.setText("?")

        self.Exit = QtWidgets.QPushButton(self.centralwidget)
        self.Exit.setGeometry(QtCore.QRect(10, 600, 111, 31))
        self.Exit.setObjectName("Exit")
        self.Exit.setText("Exit")
        self.Exit.clicked.connect(QtWidgets.QApplication.closeAllWindows)

        self.showGrid = QtWidgets.QPushButton(self.centralwidget)
        self.showGrid.setGeometry(QtCore.QRect(170, 600, 131, 31))
        self.showGrid.setObjectName("ShowGrid")
        self.showGrid.setText("Show Grid")

        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(340, 600, 111, 31))
        self.Run.setObjectName("Run")
        self.Run.setText("Run")
   
        self.cameraSettings = QtWidgets.QPushButton(self.centralwidget)
        self.cameraSettings.setGeometry(QtCore.QRect(170, 20, 131, 31))
        self.cameraSettings.setObjectName("cameraSettings")
        self.cameraSettings.setText("Camera Settings")

        self.calibration = QtWidgets.QPushButton(self.centralwidget)
        self.calibration.setGeometry(QtCore.QRect(170, 60, 131, 31))
        self.calibration.setObjectName("calibration")
        self.calibration.setText("Calibration")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 100, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Grid:")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 100, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("2x2")
        self.comboBox.addItem("3x3")
        self.comboBox.addItem("4x3")
        self.comboBox.addItem("4x4")
        self.comboBox.currentIndexChanged.connect(self.countSelected)  

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Selected:")
        self.selected = QtWidgets.QLabel(self.centralwidget)
        self.selected.setGeometry(QtCore.QRect(90, 142, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selected.setFont(font)
        self.selected.setObjectName("selected")
        

        self.addPictures = QtWidgets.QPushButton(self.centralwidget)
        self.addPictures.setGeometry(QtCore.QRect(330, 140, 131, 31))
        self.addPictures.setObjectName("addPictures")
        self.addPictures.setText("Add pictures")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 180, 451, 405))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 3418, 422))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")

        self.galery()
        
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def galery(self):
        i = 0
        self.fieldPics = []
        self.fieldChecks = []

        source = []
        print(os.getcwd())
        source = source + glob.glob(self.pictureSource+"*.png")
        source = source + glob.glob(self.pictureSource+"*.jpg")
        source = source + glob.glob(self.pictureSource+"*.bmp")
        countfiles = len(source)
        for filename in source:
            self.fieldPics.append(countfiles) 
            self.fieldChecks.append(countfiles)

            pixmap = QtGui.QPixmap(filename)
            pixmap = pixmap.scaled(120,120,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
            label = QtWidgets.QLabel(self.scrollAreaWidgetContents)

            label.setText("")
            label.setPixmap(pixmap)
            label.setObjectName("Pic")
            self.fieldPics[i]=label
            self.gridLayout.addWidget(self.fieldPics[i], i%3, i/3, 1, 1)
            self.check =  QtWidgets.QCheckBox(self.scrollAreaWidgetContents)

            self.fieldChecks[i]=self.check
            self.gridLayout.addWidget( self.fieldChecks[i], i%3, i/3, 1, 1, QtCore.Qt.AlignBottom)

            i=i+1


    def countSelected(self):
        resolution = (str(self.comboBox.currentText())).partition('x')
        row = int(resolution[0])
        column = int(resolution[2])
        count=0
        for i in range(len(self.fieldChecks)) :
            if self.fieldChecks[i].isChecked():
                count=count+1

        self.selected.setText(str(count)+"/"+str(row*column))

