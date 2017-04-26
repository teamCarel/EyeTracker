# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyWidget.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import glob

class Ui_MainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(471, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Exit = QtWidgets.QPushButton(self.centralwidget)
        self.Exit.setGeometry(QtCore.QRect(10, 600, 111, 31))
        self.Exit.setObjectName("Exit")
        self.Exit.clicked.connect(QtWidgets.QApplication.closeAllWindows)

        self.ShowGrid = QtWidgets.QPushButton(self.centralwidget)
        self.ShowGrid.setGeometry(QtCore.QRect(170, 600, 131, 31))
        self.ShowGrid.setObjectName("ShowGrid")

        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(340, 600, 111, 31))
        self.Run.setObjectName("Run")
   

        self.cameraSettings = QtWidgets.QPushButton(self.centralwidget)
        self.cameraSettings.setGeometry(QtCore.QRect(170, 20, 131, 31))
        self.cameraSettings.setObjectName("cameraSettings")

        self.calibration = QtWidgets.QPushButton(self.centralwidget)
        self.calibration.setGeometry(QtCore.QRect(170, 60, 131, 31))
        self.calibration.setObjectName("calibration")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 100, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 100, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.selected = QtWidgets.QLabel(self.centralwidget)
        self.selected.setGeometry(QtCore.QRect(90, 140, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selected.setFont(font)
        self.selected.setObjectName("selected")

        self.addPictures = QtWidgets.QPushButton(self.centralwidget)
        self.addPictures.setGeometry(QtCore.QRect(330, 140, 131, 31))
        self.addPictures.setObjectName("addPictures")

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

        i = 0
        self.fieldPics = []
        self.fieldChecks = []
        countfiles = len(glob.glob('pics/*'))
        for filename in glob.glob("pics/*.png"):
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
            check =  QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            self.fieldChecks[i]=check
            self.gridLayout.addWidget( self.fieldChecks[i], i%3, i/3, 1, 1, QtCore.Qt.AlignBottom)

            i=i+1
        
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Exit.setText(_translate("MainWindow", "Exit"))
        self.ShowGrid.setText(_translate("MainWindow", "Show Grid"))
        self.Run.setText(_translate("MainWindow", "Run"))
        self.cameraSettings.setText(_translate("MainWindow", "Camera Settings"))
        self.calibration.setText(_translate("MainWindow", "Calibration"))
        self.label.setText(_translate("MainWindow", "Grid:"))
        self.comboBox.setItemText(1, _translate("MainWindow", "3x3"))
        self.comboBox.setItemText(2, _translate("MainWindow", "4x3"))
        self.comboBox.setItemText(2, _translate("MainWindow", "4x4"))
        self.comboBox.setItemText(0, _translate("MainWindow", "1x2"))
        self.label_2.setText(_translate("MainWindow", "Selected:"))
        self.selected.setText(_translate("MainWindow", "0/9"))
        self.addPictures.setText(_translate("MainWindow", "Add pictures"))

