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
from PyQt5.QtWidgets import QMessageBox
from random import randint
from shutil import copyfile
from eyetracker import Eyetracker
from time import sleep
from multiprocessing import Process
from threading import Thread
import os
from PyQt5.Qt import QDir
from PyQt5.QtCore import Qt

class MyWindow():


    def __init__(self,eyetracker_obj):
        self.eyetracker_obj = eyetracker_obj
        #self.app = QtWidgets.QApplication(sys.argv)
        
    def startGui(self):
        global MainWindow
        global ui
        global isCalibrated
        global pictures
        self.runWin = True
        if getattr(sys, 'frozen', False):
            self.pictureSource  = os.path.dirname(sys.executable)+ "/pics/"
        else:
            self.pictureSource = os.path.dirname(os.path.abspath(__file__))+ "/pics/"
        #runWin = False
        pictures = []
        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        if getattr(sys, 'frozen', False):
           isCalibrated = os.path.dirname(sys.executable).rsplit('src', 1)[0]+"eyetracker_settings/user_calibration_data"
        else:
            isCalibrated = os.path.isfile(os.path.dirname(os.path.abspath(__file__)).rsplit('src', 1)[0]+"eyetracker_settings/user_calibration_data")
        #isCalibrated = False
        ui.setupUi(MainWindow, self.pictureSource)
        run = ui.Run.clicked.connect(self.runRun)
        MainWindow.show()
        #Exiting the app
        ui.Exit.clicked.connect(self.eyetracker_obj.closeAll)
        self.app.aboutToQuit.connect(self.eyetracker_obj.closeAll)
        #calibration
        ui.calibration.clicked.connect(self.runCalibration)
        ui.countSelected()
        ui.addPictures.clicked.connect(self.runAddPictures)
        ui.Help.clicked.connect(self.runHelp)
        ui.cameraSettings.clicked.connect(self.runCameraSettings)
        ui.showGrid.clicked.connect(self.runShowGrid)
        self.ui = ui
        for i in range(len(ui.fieldChecks)):
            ui.fieldChecks[i].stateChanged.connect(self.countSelected)
        sys.exit(self.app.exec_())

    def runHelp(self):
        global alert
        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("Help")
        alert.setText("Guick guide\n"
                        + "1) Set camera for your eye\n"
                        + "2) Run calibration\n"
                        + "3) Choose parameters, which suits you best\n"
                        + "4) Select grid and apropriate amount of pictures\n"
                        + "5) Click Run button for showing fullscreen grid, detection begins automaticly\n"
                        + "6) For exit push Esc on your keyboard\n"
                        + "\nIf camera doesn't show your eye or calibration doesn't start reconect EyeTracker.\n"
                        + "If there is still problem after reconnecting, please restart your computer and hope for the best.")
        alert.open()

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
        #print(row," ",col)
        column = int(resolution[2])
        Thread(target=self.runTileProcess,name="tileDetect",args=(row,column)).start()
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
                    screen = QtWidgets.QDesktopWidget().screenGeometry()
                    run_ui = Ui_RunWindow()
                    run_ui.setupUi(RunWindow, row, column, pictures, self.pictureSource, screen) ##rows, cols, field
                    RunWindow.keyPressEvent=self.runExit
                    
                    
                    #Process(target=RunWindow.showFullScreen,name="window",).start()
                    RunWindow.showFullScreen()
                    
                    Thread(target=self.runTileProcess,name="tileDetect",args=(row,column)).start()
                    
                    #RunWindow.repaint()
                else:
                    global alert
                    alert = QMessageBox()
                    alert.setWindowTitle("Wrong number of pictures.")
                    alert.setText("Number of selected pictures does not fit the selected grid. Please change grid size or select correct amount.")
                    alert.setIcon(QMessageBox.Critical)
                    alert.exec()
            else:
                alert = QMessageBox()
                alert.setWindowTitle("Not calibrated")
                alert.setText("Camera was not calibrated, please run Calibration.")
                alert.setIcon(QMessageBox.Warning)
                alert.exec()
            
            
    
    def runTileProcess(self,rows,cols):
        self.runWin = True
        while self.runWin:
            tile = self.eyetracker_obj.tileDetection(rows,cols,self.ui.time.value(),self.ui.percent.value(),self.ui.conf.value())
            if tile == None:
                self.runWin = False
                print("failed")
            else:
                #Thread(target=self.highlight,name="highlightTile",args=(tile['x'], tile['y'])).start()
                self.highlight(tile['x'], tile['y'])
            #sleep(0.01)

    #def runUiRunExitAll(self):
     #   self.runWin = False
      #  self.eyetracker_obj.closeAll()
       # RunWindow.close()
        #MainWindow.close()

    def runUiShowGridExit(self):
        global MainWindow
        MainWindow.show()
        ShowGridWindow.close()

    def highlight(self, x, y):
        global RunWindow
        #if(self.runWin):
        global run_ui
        #Thread(target=run_ui.highlightPic,args=(x, y, RunWindow)).start()
        run_ui.highlightPic(x, y)
        #RunWindow.repaint()
        #Thread(target=RunWindow.repaint).start()
        sleep(2)
        run_ui.unHighlightPic(x, y)
        #RunWindow.repaint()
        #Thread(target=run_ui.unHighlightPic,args=(x, y, RunWindow)).start()


    def runAddPictures(self):
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.ExistingFiles)
            dlg.setWindowTitle("Add pictures")
            src = str(dlg.getOpenFileName()[0])
            if len(src)!=0:
                suffix = src.rsplit('.', 1)[1]
                formats = ['png', 'jpg', 'bmp', 'jpeg']
                if suffix in formats:
                    filename = src.split("/")
                    dst = os.path.dirname(os.path.abspath(__file__))+ "/pics/"+filename[len(filename)-1]
                    copyfile(src, dst)
                    ui.galery()
                    for i in range(len(ui.fieldChecks)):
                        ui.fieldChecks[i].stateChanged.connect(self.countSelected)
                        ui.countSelected()
            

    def runCalibration(self):     
        global isCalibrated
        isCalibrated = self.eyetracker_obj.calibrate()
        if not isCalibrated:
            alert = QMessageBox()
            alert.setWindowTitle("Calibration failed")
            alert.setText("Camera was not calibrated successfully, please try reconnecting your headset and run Calibration again.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec()
            

    def runCameraSettings(self):
        self.eyetracker_obj.showEyeCam()
        
    def runExit(self, event):
        if event.key() == Qt.Key_Escape:
            self.runWin = False
            global RunWindow
            RunWindow.close()
            RunWindow = None

        

    def savePictures(self):
        global pictures
        pictures = show_grid_ui.pictures
        global alert
        alert = QMessageBox()
        alert.setWindowTitle("Picture positions saved.")
        alert.setText("Picture positions saved.")
        alert.setIcon(QMessageBox.Information)
        alert.exec()

    def closeGridEvent(self, event):
        self.runUiShowGridExit()
            
    def runShowGrid(self):
        global ShowGridWindow
        global show_grid_ui
        ShowGridWindow = QtWidgets.QMainWindow()
        show_grid_ui = Ui_ShowGridWindow()
        resolution = self.getResolution()
        ShowGridWindow.closeEvent = self.closeGridEvent
    
        if((int(resolution[0])*int(resolution[2])) == len(pictures)):
            show_grid_ui.setupUi(ShowGridWindow, int(resolution[0]), int(resolution[2]), pictures, self.pictureSource) ##rows, cols, field
            show_grid_ui.Exit.clicked.connect(self.runUiShowGridExit)
            show_grid_ui.Save.clicked.connect(self.savePictures)
            ShowGridWindow.show()
            global MainWindow
            MainWindow.hide()
        else:
            alert = QMessageBox()
            alert.setWindowTitle("Wrong number of pictures.")
            alert.setText("Number of selected pictures does not fit the selected grid. Please change grid size or select correct amount.")
            alert.setIcon(QMessageBox.Critical)
            alert.exec()
