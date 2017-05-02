# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyWidget.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import glob

class Ui_RunWindow():
    def setupUi(self, RunWindow, row, column, pictures):
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
        source = glob.glob("pics/*.png")
        self.field = []
        for i in range(row):
            for j in range(column):
                self.field.append(row*column)
                pixmap = QtGui.QPixmap(source[pictures[i*column+j]])
                label = QtWidgets.QLabel(self.centralwidget)

                label.setText("")
                label.setPixmap(pixmap)
                label.setObjectName("Pic")
                label.setContentsMargins(10, 10, 10, 10)
                self.field[len(self.field)-1] = label
                self.gridLayout.addWidget(label, i, j, 1, 1, QtCore.Qt.AlignCenter)
        

        
        
        self.Exit = QtWidgets.QPushButton(self.centralwidget)
        self.Exit.setGeometry(QtCore.QRect(10, 10, 50, 20))
        self.Exit.setObjectName("Exit Window")

        self.ExitAll = QtWidgets.QPushButton(self.centralwidget)
        self.ExitAll.setGeometry(QtCore.QRect(10, 30, 50, 20))
        self.ExitAll.setObjectName("Exit All")

        RunWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RunWindow)
        QtCore.QMetaObject.connectSlotsByName(RunWindow)

    def highlightPic(self, row, col):
        self.field[col+row*self.column].setStyleSheet("background-color: green")
    def unHighlightPic(self, row, col):
        self.field[col+row*self.column].setStyleSheet("background-color: transparent")

    def retranslateUi(self, RunWindow):
        _translate = QtCore.QCoreApplication.translate
        RunWindow.setWindowTitle(_translate("RunWindow", "RunWindow"))        
        self.Exit.setText(_translate("MainWindow", "Exit"))
        self.ExitAll.setText(_translate("MainWindow", "Exit All"))