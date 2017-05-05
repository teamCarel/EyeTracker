import sys
import imp
from .Ui_MainWindow import Ui_MainWindow
from .Ui_RunWindow import Ui_RunWindow
from .Ui_ShowGridWindow import Ui_ShowGridWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QErrorMessage
from random import randint
from shutil import copyfile
from eyetracker import Eyetracker
from time import sleep
from multiprocessing import Process
import os

class MyWindow():


    def __init__(self,eyetracker_obj):
        self.eyetracker_obj = eyetracker_obj
        #self.app = QtWidgets.QApplication(sys.argv)
        
    def startGui(self):
        global MainWindow
        global ui
        global isCalibrated
        global pictures
        global runWin
        runWin = False
        pictures = []
        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        isCalibrated = False
        ui.setupUi(MainWindow)
        run = ui.Run.clicked.connect(self.runRun)
        MainWindow.show()
        ui.countSelected()
        ui.addPictures.clicked.connect(self.runAddPictures)
        ui.calibration.clicked.connect(self.runCalibration)
        ui.cameraSettings.clicked.connect(self.runCameraSettings)
        ui.showGrid.clicked.connect(self.runShowGrid)
        for i in range(len(ui.fieldChecks)):
            ui.fieldChecks[i].stateChanged.connect(self.countSelected)
        sys.exit(self.app.exec_())

    def countSelected(self):
        global pictures
        del pictures[:]
        resolution = self.getResolution()
        row = int(resolution[0])
        column = int(resolution[2])
        count=0
        for i in range(len(ui.fieldChecks)) :
            if ui.fieldChecks[i].isChecked():
                count=count+1
                pictures.append(len(ui.fieldChecks))
                pictures[len(pictures)-1]=i

        ui.selected.setText(str(count)+"/"+str(row*column))

    def getResolution(self):
        resolution = (ui.comboBox.currentText()).partition('x')
        return resolution
    
    def runEyeDetection(self):
        resolution = self.getResolution()
        row = int(resolution[0])
        print(row," ",col)
        column = int(resolution[2])
        Process(target=self.runTileProcess(row,column),name="tileDetect",).start()
        #self.runTileProcess(row,column)
            
    def runRun(self):
            if isCalibrated==True:
                global RunWindow
                global run_ui
                resolution = self.getResolution()
                row = int(resolution[0])
                column = int(resolution[2])
                i=0

                if((row*column) == len(pictures)):
                    RunWindow = QtWidgets.QMainWindow()
                    #RunWindow = self.app.QMainWindow()

                    run_ui = Ui_RunWindow()
                    run_ui.setupUi(RunWindow, row, column, pictures) ##rows, cols, field
                    run_ui.Run.clicked.connect(self.runEyeDetection)
                    run_ui.Exit.clicked.connect(self.runUiRunExit)
                    run_ui.ExitAll.clicked.connect(self.runUiRunExitAll)
                    #Process(target=RunWindow.showFullScreen,name="window",).start()
                    RunWindow.showFullScreen()
                    RunWindow.repaint()
                else:
                    global alert
                    alert = QErrorMessage()
                    alert.showMessage("Wrong number of pictures"+str(len(pictures)))
            else:
                alert = QErrorMessage()
                alert.showMessage("Camera was not calibrated, please run Calibration.")
    
    def runTileProcess(self,rows,cols):
        runWin = True
        while runWin:#TODO get should close
            tile = self.eyetracker_obj.tileDetection(rows,cols)
            self.highlight(tile['x'], tile['y'])

    def runUiRunExit(self):
            runWin = False
            RunWindow.close()

    def runUiRunExitAll(self):
        self.eyetracker_obj.closeAll()
        runWin = False
        RunWindow.close()
        MainWindow.close()

    def runUiShowGridExit(self):
            ShowGridWindow.close()

    def highlight(self, x, y):
        print(x," ",y)
        run_ui.highlightPic(x, y)
        RunWindow.repaint()
        sleep(5)
        run_ui.unHighlightPic(x, y)

    def runAddPictures(self):
            dlg = QFileDialog()
            src = str(dlg.getOpenFileName()[0])
            if len(src)!=0:
                filename = src.split("/")
                dst = os.path.dirname(os.path.abspath(__file__))+ "/pics/"+filename[len(filename)-1]
                copyfile(src, dst)
                ui.galery()
                MainWindow.repaint()

    def runCalibration(self):     
        global isCalibrated
        isCalibrated = self.eyetracker_obj.calibrate()

    def runCameraSettings(self):
        self.eyetracker_obj.showEyeCam()

    def savePictures(self):
        global pictures
        pictures = show_grid_ui.pictures
        global alert
        alert = QErrorMessage()
        alert.showMessage("Picture position saved.")

    def runShowGrid(self):
        global ShowGridWindow
        global show_grid_ui
        ShowGridWindow = QtWidgets.QMainWindow()
        show_grid_ui = Ui_ShowGridWindow()
        resolution = self.getResolution()
    
        if((int(resolution[0])*int(resolution[2])) == len(pictures)):
            show_grid_ui.setupUi(ShowGridWindow, int(resolution[0]), int(resolution[2]), pictures) ##rows, cols, field
            show_grid_ui.Exit.clicked.connect(self.runUiShowGridExit)
            show_grid_ui.Save.clicked.connect(self.savePictures)
            ShowGridWindow.show()
        else:
            alert = QErrorMessage()
            alert.showMessage("Wrong number of pictures")
